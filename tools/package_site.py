"""Create a portable, dependency-free GitHub Pages source bundle."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
import argparse

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=ROOT.parent/'orbital-archive-v10.zip')
args = parser.parse_args()
files = [ROOT/name for name in ['index.html','home.html','profile.html','contact.html','project.html',
    'archive.css','archive-v3.css','archive-v4.css','archive-v7.css','archive-v8.css','archive-v9.css','archive.js','.nojekyll','README.md','assets/mark.svg','assets/resume.pdf','assets/wechat-qr-source.png']]
for folder in ['projects','data','tools','assets/source-png','assets/layers']:
    files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
source_images = json.loads((ROOT/'data/source-images.json').read_text(encoding='utf-8-sig'))
files.extend(ROOT/f'assets/full/slide-{page:02d}.jpg' for page in range(1,61) if str(page) not in source_images)
args.output.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(args.output,'w',compression=ZIP_DEFLATED,compresslevel=6) as archive:
    for source in sorted(set(files)):
        archive.write(source,source.relative_to(ROOT).as_posix())
print(f'{args.output.resolve()} / {len(set(files))} files / {args.output.stat().st_size/1024/1024:.1f} MiB')
