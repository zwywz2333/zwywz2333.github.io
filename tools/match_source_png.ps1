param(
  [string]$Source = 'D:\zpj2\zpj-y',
  [string]$Slides = (Join-Path (Split-Path $PSScriptRoot -Parent) 'assets\portfolio-slides'),
  [string]$Output = (Join-Path $PSScriptRoot 'source-png-match.csv')
)
Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @'
using System;
using System.Drawing;
public class Fingerprint {
 public static byte[] Read(string path) {
   using (var bitmap = new Bitmap(path)) {
     var values = new byte[24*14*3]; int j=0;
     for(int y=0;y<14;y++) for(int x=0;x<24;x++) {
       var color=bitmap.GetPixel(Math.Min(bitmap.Width-1,(int)((x+.5)*bitmap.Width/24)),Math.Min(bitmap.Height-1,(int)((y+.5)*bitmap.Height/14)));
       values[j++]=color.R; values[j++]=color.G; values[j++]=color.B;
     }
     return values;
   }
 }
 public static double Distance(byte[] a, byte[] b) {
   double error=0;
   for(int i=0;i<a.Length;i++){double d=a[i]-b[i];error+=d*d;}
   return Math.Sqrt(error/a.Length);
 }
}
'@
$references = @(Get-ChildItem -LiteralPath $Slides -Filter 'slide-*.jpg' -File | ForEach-Object {
  [pscustomobject]@{Page=[int]($_.BaseName -replace '^slide-',''); Pixels=[Fingerprint]::Read($_.FullName)}
})
$matches = foreach($file in Get-ChildItem -LiteralPath $Source -Filter '*.png' -File) {
  if ($file.BaseName -notmatch '^\d+$') { continue }
  $pixels=[Fingerprint]::Read($file.FullName)
  $best=$references | ForEach-Object { [pscustomobject]@{Page=$_.Page; Distance=[Fingerprint]::Distance($pixels,$_.Pixels)} } | Sort-Object Distance | Select-Object -First 2
  [pscustomobject]@{Source=$file.FullName; Page=$best[0].Page; Distance=[math]::Round($best[0].Distance,2); NextPage=$best[1].Page; NextDistance=[math]::Round($best[1].Distance,2)}
}
$matches | Sort-Object {[int]([IO.Path]::GetFileNameWithoutExtension($_.Source))} | Export-Csv -LiteralPath $Output -NoTypeInformation -Encoding utf8
$matches | Sort-Object {[int]([IO.Path]::GetFileNameWithoutExtension($_.Source))} | Format-Table -AutoSize
