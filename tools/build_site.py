"""Build the static portfolio from the original PDF page map. Python stdlib only."""
from pathlib import Path
from html import escape as e
import json

ROOT = Path(__file__).resolve().parents[1]
FILES = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))
SOURCE_IMAGES = json.loads((ROOT / 'data/source-images.json').read_text(encoding='utf-8-sig'))
EXTRA = [
    ('#aec4e1', 'SYSTEMS / PRODUCT', '设计秩序的建立', '01 / DESIGN SYSTEM', [
        ('差异从哪里来？', '从页面样本中的平台、主题和状态差异，追踪资产难以复用的原因。', 1),
        ('系统如何组织？', '将基础规则、页面模式与通用组件联系起来，保留成熟产品的使用语境。', 5),
        ('规则如何被使用？', '沿 AI 工作流和设计验证，查看设计资产如何成为可调用的依据。', 6)]),
    ('#c0ba91', 'CULTURE / EXPERIENCE', '在行走中发现文化', '02 / FIELD RESEARCH', [
        ('谁在探索？', '从不同用户的探索动机出发，理解亲子、年轻人与文化爱好者的需求。', 2),
        ('线索如何连接？', '查看线下打卡、AR 互动与卡牌收集如何构成服务路径。', 4),
        ('地图如何讲故事？', '沿地图、文化地点与卡牌属性，阅读场域如何转化为交互内容。', 7)]),
    ('#a6d0c8', 'SERVICE / WELLBEING', '把日常还给松弛', '03 / SERVICE DESIGN', [
        ('压力发生在哪里？', '从需求聚类中定位效率、隐私和设施体验的主要问题。', 2),
        ('情绪如何变化？', '跟随洗澡前、中、后的行为与情绪，找到服务的设计机会。', 3),
        ('体验如何闭环？', '从进行中的引导到订单与反馈，查看一次服务如何完整结束。', 5)]),
    ('#c8b7cd', 'CHARACTER / ILLUSTRATION', '想象的两种尺度', '04 / VISUAL STUDIES', [
        ('角色如何成立？', '在角色设定、比例和材质之间，寻找形象与性格的联系。', 0),
        ('形象如何延展？', '从角色场景与周边应用，观察同一个视觉设定如何进入不同媒介。', 0),
        ('自然如何被描绘？', '在自然史主题插画中，观察标本、植物与宇宙线索的视觉组织。', 1)])
]
for f, extra in zip(FILES, EXTRA):
    f['accent'], f['category'], f['tagline'], f['index_label'], f['clues'] = extra

def img(page, base='', **attrs):
    attr=' '.join(f'{k.replace("_", "-")}="{e(str(v))}"' for k,v in attrs.items())
    source=SOURCE_IMAGES.get(str(page), f'assets/full/slide-{page:02d}.jpg')
    width=1920 if str(page) in SOURCE_IMAGES else 2560
    return f'<img src="{base}{source}" width="{width}" height="{width*9//16}" alt="作品集第 {page:02d} 页" {attr}>'

def plate(page, base='', title='', cls='', eager=False):
    source=SOURCE_IMAGES.get(str(page), f'assets/full/slide-{page:02d}.jpg')
    return f'''<figure class="plate {cls}" data-reveal data-depth="{(page%3+1)*3}">
      <a class="image-open" href="{base}{source}" data-page="{page}" data-title="{e(title)}" aria-label="放大查看：{e(title)}，第 {page} 页">
      {img(page,base,loading='eager' if eager else 'lazy',decoding='async')}<span class="inspect">＋ 放大查看</span></a>
      <figcaption><span>FIG. {page:02d} / {e(title)}</span><span>原始档案 · {page:02d}</span></figcaption></figure>'''

LOGO='<svg viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="12"/><ellipse cx="22" cy="22" rx="21" ry="7" transform="rotate(-40 22 22)"/><path d="M22 1v9m0 24v9M1 22h9m24 0h9"/><circle cx="22" cy="22" r="2" fill="currentColor"/></svg>'

def header(base='', current=''):
    back = '<a class="index-return" href="index.html" aria-label="返回入口"><span aria-hidden="true">↖</span><span>返回入口</span></a>' if current == 'home' else ''
    if current == 'contact':
        back = '<button class="contact-back" type="button" data-return-previous>← 返回上一页</button>'
    return f'''<header class="site-header"><div class="header-left"><a class="brand" href="{base}home.html" aria-label="ZHANGWENYAN，返回作品目录"><span>ZHANGWENYAN</span></a>{back}</div>
      <span class="header-status">PORTFOLIO / 2026</span>
      <nav aria-label="主导航"><a href="{base}home.html" {'aria-current="page"' if current=='home' else ''}>作品索引 <sup>04</sup></a><a href="{base}profile.html" {'aria-current="page"' if current=='profile' else ''}>关于我</a><a href="{base}contact.html" {'aria-current="page"' if current=='contact' else ''}>建立联系</a><button class="menu-trigger" aria-label="打开全站导航" aria-expanded="false" aria-controls="site-menu">MENU <span>＋</span></button></nav></header>'''

def utilities(base=''):
    links=''.join(f'<a class="menu-link menu-link-{f["id"]}" href="{base}projects/{f["id"]}.html"><small>{f["code"]}</small><span>{e(f["title"])}</span><b>↗</b></a>' for f in FILES)
    return f'''<dialog id="site-menu" class="menu-dialog"><div class="menu-top"><span class="mono">NAVIGATION / 档案导航</span><button data-close="site-menu" aria-label="关闭导航">CLOSE ×</button></div><div class="menu-content"><p class="mono">选择一份记录，<br>继续你的探索。</p><nav aria-label="全部项目">{links}<a href="{base}profile.html"><small>P / 02</small><span>人员档案</span><b>↗</b></a></nav></div><div class="menu-bottom mono">ZHANG WENYAN <button class="motion-toggle">动态效果：开启</button></div></dialog>
      <dialog id="viewer" aria-label="作品原图查看器"><div class="viewer-bar"><span id="viewer-caption" class="mono"></span><div><button id="zoom-toggle" aria-pressed="false">原尺寸</button><button data-close="viewer" aria-label="关闭原图">关闭 ×</button></div></div><div class="viewer-stage"><img id="viewer-image" alt="作品原图"></div><div class="viewer-bottom"><button id="image-prev" aria-label="上一张">← 上一张</button><span class="mono">← → 切换 / ESC 关闭</span><button id="image-next" aria-label="下一张">下一张 →</button></div></dialog>'''

def footer(base=''):
    return f'''<footer class="site-footer"><span>张文砚 / ZHANG WENYAN</span><span>DESIGN IS AN ONGOING EXPLORATION.</span><a href="{base}contact.html">建立联系 ↗</a></footer>'''

def document(title, content, base='', body=''):
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#171336"><meta name="description" content="张文砚的个人设计作品集，包含 Pacer UI Kit、开化寻踪、Shower Enjoyment 和个人视觉实践。"><title>{e(title)} — 张文砚</title><link rel="icon" href="{base}assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}archive.css?v=19"><link rel="stylesheet" href="{base}archive-v3.css?v=19"><link rel="stylesheet" href="{base}archive-v4.css?v=19"><link rel="stylesheet" href="{base}archive-v7.css?v=19"><link rel="stylesheet" href="{base}archive-v8.css?v=19"><link rel="stylesheet" href="{base}archive-v9.css?v=19"><script src="{base}archive.js?v=19" defer></script></head><body {body} data-base="{base}"><a class="skip-link" href="#main">跳到主要内容</a>{content}</body></html>'''

ORBIT='''<svg class="orbit-map" viewBox="0 0 640 400" aria-hidden="true"><defs><radialGradient id="sphere"><stop offset="0" stop-color="#8c987e" stop-opacity=".11"/><stop offset="1" stop-color="#8c987e" stop-opacity="0"/></radialGradient></defs><circle cx="320" cy="200" r="140" fill="url(#sphere)" stroke="none"/><ellipse cx="320" cy="200" rx="285" ry="84" transform="rotate(-24 320 200)"/><ellipse cx="320" cy="200" rx="180" ry="135" transform="rotate(24 320 200)"/><circle cx="320" cy="200" r="104"/><path d="M320 20v360M40 200h560" class="dashed"/><path d="M307 200h26m-13-13v26" class="cross"/><circle cx="504" cy="114" r="5" class="satellite"/><circle cx="165" cy="249" r="3" class="satellite"/><text x="344" y="190">ORIGIN / 001</text><text x="510" y="101">SIGNAL RECEIVED</text><text x="80" y="320">RECORDING IDEAS IN ORBIT</text></svg>'''

def build_home():
    cards=[]
    captions=['Pacer 产品组件库的设计与搭建','AR 卡牌叙事国家公园沉浸式服务体验设计','解压为中心的校园公共浴室服务体验设计','其他个人练习']
    for i,f in enumerate(FILES):
        n=i+1
        cards.append(f'''<a class="directory-hotspot directory-card hotspot-{n}" id="file-{f['id']}" href="projects/{f['id']}.html" data-card="{f['id']}" data-caption="{e(f['title'])}" aria-label="打开项目：{e(f['title'])}"><span class="card-visual"><span class="card-underlay" aria-hidden="true"><img class="card-underlay-texture" src="assets/layers/directorycard-orbit-bg.png" alt="" loading="eager"><img class="card-underlay-moon" src="assets/layers/directorycard-orbit-moon.png" alt="" loading="eager"></span><img class="directory-cover" src="assets/layers/directorycard-cover-{n:02d}.png" alt="" loading="eager" decoding="async"><img class="directory-text" src="assets/layers/directorycard-text-{n:02d}.png" alt="" loading="eager" decoding="async"></span><span class="card-foot"><span class="card-caption">{e(captions[i])}</span><strong>{n:02d}<i></i></strong></span></a>''')
    content=header(current='home')+f'''<main id="main" class="directory-main"><div class="directory-atmosphere" aria-hidden="true"><img class="directory-orbit-moon orbit-moon-a" src="assets/layers/directorycard-orbit-moon.png" alt=""><img class="directory-orbit-moon orbit-moon-b" src="assets/layers/directorycard-orbit-moon.png" alt=""><img class="directory-orbit-bg" src="assets/layers/directorycard-orbit-bg.png" alt=""><svg viewBox="0 0 1600 900" preserveAspectRatio="none"><path d="M-120 235 C300 -90 320 970 820 600 S1190 -40 1720 450"/><path d="M-80 520 H1680"/></svg></div><div class="directory-stage"><div class="directory-cards">{''.join(cards)}</div></div><div class="directory-bottom"><span>CONTENTS / 01—04</span><a href="profile.html">关于张文砚 ↗</a></div></main>'''+utilities()
    (ROOT/'home.html').write_text(document('作品索引 / ORBITAL ARCHIVE',content,body='class="home-page"'),encoding='utf-8')

def build_project(f, i):
    base='../'
    menu=''.join(f'<a href="#chapter-{j}" data-chapter-link="{j}"><small>{j+1:02d}</small><span>{e(c["title"])}</span><i></i></a>' for j,c in enumerate(f['chapters']))
    chapters=[]
    for j,c in enumerate(f['chapters']):
        pages=''.join(plate(p,base,c['title'],f'frame-{k}',False) for k,p in enumerate(c['pages']))
        chapters.append(f'''<section class="chapter" id="chapter-{j}" data-chapter="{j}"><header class="chapter-title" data-reveal><span class="chapter-number">{j+1:02d}</span><div><p class="mono">P.{c['pages'][0]:02d}—{c['pages'][-1]:02d}</p><h2>{e(c['title'])}</h2><p>{e(c['note'])}</p></div><span class="chapter-cross" aria-hidden="true">+</span></header><div class="image-sequence" tabindex="0" aria-label="{e(c['title'])}：左右滚动或使用下方按钮翻页">{pages}</div><div class="slide-controls"><span class="slide-current">01</span><span class="slide-track"><i></i></span><span class="slide-total">{len(c['pages']):02d}</span><button data-slide-prev aria-label="上一页"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M25 16H7m0 0 8-8m-8 8 8 8"/><circle cx="25" cy="16" r="1"/></svg></button><button data-slide-next aria-label="下一页"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M7 16h18m0 0-8-8m8 8-8 8"/><circle cx="7" cy="16" r="1"/></svg></button></div></section>''')
    cluebuttons=''.join(f'<button data-clue="{j}" aria-expanded="false" aria-controls="clue-panel"><small>{j+1:02d}</small>{e(cl[0])}<span>＋</span></button>' for j,cl in enumerate(f['clues']))
    prev,nextf=FILES[(i-1)%4],FILES[(i+1)%4]
    summary=project_summary(f)
    content=header(base)+f'''<main id="main"><section class="project-intro" style="--file-color:{f['accent']}"><div class="project-heading"><a href="../home.html#file-{f['id']}" class="back-link">← 返回目录</a><div class="project-title-row"><div><h1>{e(f['title'])}</h1></div><span class="project-serial">{i+1:02d}</span></div></div><div class="project-hero-grid"><div class="project-brief"><h2>{e(f['tagline'])}</h2><p>{e(f['short'])}</p><a class="begin-reading" href="#chapter-0">开始阅读 <span>↓</span></a></div><div class="project-cover" style="view-transition-name:cover-{f['id']}">{plate(f['cover'],base,'项目封面','cover-plate',True)}</div></div>{summary}<div class="clue-desk"><div class="clue-label"><h3>设计线索</h3><small id="clue-progress">0 / 3 已探索</small></div><div class="clue-actions">{cluebuttons}</div><div id="clue-panel" class="clue-panel" hidden><p></p><a href="#chapter-0">定位证据 ↗</a></div></div></section><div class="reading-area"><div class="reading-top mono"><span>{e(f['title'])} / {f['code']}</span><span class="reading-percent">00%</span></div><div class="reading-layout"><aside class="chapter-nav"><nav aria-label="项目章节">{menu}</nav></aside><article class="project-article">{''.join(chapters)}</article></div></div><section class="end-record"><h2>继续阅读</h2><a class="next-project" href="{nextf['id']}.html"><span class="next-art">{img(nextf['cover'],base,loading='lazy')}</span><span><small class="mono">NEXT / {nextf['code']}</small><strong>{e(nextf['title'])}</strong></span><b>↗</b></a><div class="end-links"><a href="{prev['id']}.html">← {e(prev['title'])}</a><a href="../home.html#file-{f['id']}">全部项目 ＋</a></div></section></main>'''+footer(base)+utilities(base)+f'<script type="application/json" id="clue-data">{json.dumps(f["clues"],ensure_ascii=False)}</script>'
    (ROOT/'projects'/f'{f["id"]}.html').write_text(document(f['title'],content,base,f'class="project-page" data-project="{f["id"]}"'),encoding='utf-8')

RESUME_ICON='''<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M12 5h17l8 8v30H12z"/><path d="M29 5v9h8M17 21h15M17 28h15M17 35h10"/><circle cx="8" cy="32" r="2"/></svg>'''
CONTACT_ICON='''<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M5 17V7h10M33 7h10v10M43 31v10H33M15 41H5V31"/><path d="M17 17h6v6h-6zM29 17h5v5h-5zM17 29h5v5h-5zM28 28h3m5 0v6h-6"/><path d="M23 7h3M7 23v3M41 23v3M23 41h3"/></svg>'''

WORK = [
    ('2026.04—07', 'UI 设计实习生', '北京百泰科技有限公司', [
        '参与 Pacer 的 UI/UX 设计与迭代。',
        '整理组件库、搭建页面组件与规范，并验证 AI 生成设计流程。',
        '参与目标设定、Streak 打卡、AE 动效及商店概览设计。']),
    ('2025.12—2026.01', '短片制作', '浙江医保「全民参保，浙里同行」系列 AI 宣传短片', [
        '与甲方对接，梳理需求并优化文字脚本。',
        '使用 AI 生成视频素材，完成剪辑与成片。']),
    ('2023.08—10', '内容运营实习生', '北京回旋加速网络科技有限公司', [
        '参与游戏 AI 生成图片的修复与创作。',
        '参与 LoRA 模型训练，负责风格筛选与图片分类打标。'])
]

PROJECT_SUMMARIES = {
    'pacer': ('参与 Pacer UI/UX 设计、组件库整理与设计规范搭建。', '按页面复杂度组织页面结构模板和深度组件，连接基础规范与通用组件。', '基础规范、页面模式与组件方案，并通过真实页面和 AI 生成流程验证。'),
    'kaihua': ('体验策略、交互流程与视觉设计。', '以实体卡牌串联地图打卡、现场 AR 互动和后续分享。', '服务流程、地图任务、卡牌规则与 AR 拍摄界面。'),
    'shower': ('服务体验与产品界面设计。', '沿洗澡前、中、后的用户旅程，整合浴位状态、流程引导与反馈。', '状态查询、核心服务流程、订单及反馈等界面方案。'),
    'practice': ('角色设定、场景表达与主题插画。', '以角色叙事和自然史观察两条线处理比例、材质与画面信息。', '角色形象、场景与周边应用，以及自然史主题插画。')
}

def work_card(item):
    period, title, employer, points = item
    lines = ''.join(f'<li>{e(point)}</li>' for point in points)
    return f'''<article class="about-work work-entry"><time>{e(period)}</time><div class="work-entry-body"><div class="work-entry-head"><h3>{e(title)}</h3><p>{e(employer)}</p></div><span class="work-entry-label">工作内容 / CONTRIBUTION</span><ul>{lines}</ul></div></article>'''

def project_summary(f):
    headings = ('我的职责', '设计决策', '设计产出')
    cards = ''.join(f'<div class="project-summary-item"><span>{n:02d} / {e(heading)}</span><p>{e(value)}</p></div>' for n, (heading, value) in enumerate(zip(headings, PROJECT_SUMMARIES[f['id']]), 1))
    return f'<section class="project-summary" aria-label="项目导读：职责、决策与产出">{cards}</section>'

def awards_markup():
    awards = [
        ('2023', '设计马拉松 · 银奖'),
        ('2024', '设计马拉松 · 金奖'),
        ('2025', '全国大学生数字媒体科技竞赛 · 国赛三等奖'),
        ('2025', '全国大学生数字媒体科技竞赛 · 北京赛区一等奖'),
        ('2025', 'UXDA 国际用户体验创新大赛 · 银奖')
    ]
    rows = ''.join(f'<li><time>{e(year)}</time><span>{e(title)}</span></li>' for year, title in awards)
    return f'<section class="about-awards awards-panel" aria-label="获奖经历"><h3>获奖<span>award</span><i aria-hidden="true"></i></h3><ol>{rows}</ol></section>'

def build_profile():
    layer=lambda name,cls='',alt='': f'<img class="{cls}" src="assets/layers/{name}.png" alt="{e(alt)}" loading="lazy" decoding="async">'
    content=header(current='profile')+f'''<main id="main" class="profile-main">
      <section class="about-scene" aria-label="关于张文砚"><div class="about-orbit" aria-hidden="true">{layer('aboutme_orbit4','about-orbit-moon')}{layer('aboutme_orbit5','about-orbit-stone')}</div>
        <div class="about-head">{layer('aboutMe_title','about-title','About Me. 关于我')}<span class="about-section-code">PERSONNEL / 02</span></div>
        <div class="about-hero"><div class="about-portrait" data-about-depth="1.1">{layer('aboutme_photo','about-photo','张文砚的个人照片')}{layer('aboutme_name','about-name','张文砚 / ZHANGWENYAN')}{layer('aboutme_orbit1','about-photo-note')}</div>
          <div class="about-facts"><div class="about-contact about-contact-card" data-about-depth=".5"><span class="contact-title-cn">联系方式</span><h2>Contact Information</h2><div class="contact-detail"><span>WECHAT</span><a href="contact.html">zwywz <b>↗</b></a></div><div class="contact-detail"><span>PHONE</span><span class="contact-static">18792793260</span></div><div class="contact-detail"><span>EMAIL</span><span class="contact-static">1165873093@qq.com</span></div></div>
            <div class="about-fact-grid"><div data-about-depth=".35">{layer('aboutme_age','','24 岁')}</div><div data-about-depth=".55">{layer('aboutme_edu','','北京服装学院，数字媒体艺术方向，研二')}</div><div data-about-depth=".3">{layer('aboutme_mbti','','MBTI：INFP')}</div></div>
            <div class="about-hobby" data-about-depth=".7">{layer('aboutme_hobby','','爱好：绘画、设计案例、音乐与游戏')}<p class="about-mobile-copy">喜欢绘画、设计案例、ACG 与游戏，也喜欢听朋友聊天，从不同经历中获取灵感。</p></div>
          </div></div><div class="about-skill" data-about-depth=".25">{layer('aboutme_skill','','技能：Illustrator、Photoshop、Procreate、After Effects、Blender 等')}</div><div class="about-after"><a class="about-contact-shortcut" href="contact.html">{CONTACT_ICON}<span>联系我</span><b>↗</b></a></div>
      </section>
      <section class="about-records" aria-label="工作经历与获奖"><div class="about-records-head">{layer('aboutme_workpro_title','','工作和项目经历')}{layer('aboutme_orbit2','about-record-note')}</div><div class="about-records-grid"><div class="about-work-list">{''.join(work_card(item) for item in WORK)}</div><div class="about-records-side">{awards_markup()}<div class="about-links"><a class="about-action about-action-resume" href="assets/resume.pdf" target="_blank" rel="noopener"><span class="about-action-icon">{RESUME_ICON}</span><span class="about-action-copy"><small>RESUME / PDF</small><strong>查看一页简历</strong></span><b>↗</b></a><a class="about-action about-action-contact" href="contact.html"><span class="about-action-icon">{CONTACT_ICON}</span><span class="about-action-copy"><small>WECHAT / CONNECT</small><strong>建立联系</strong></span><b>↗</b></a></div></div></div></section>
      <section id="contact" class="profile-closing" aria-label="感谢阅览"><div class="thanks-art" aria-hidden="true"></div><div class="thanks-content"><div class="thanks-mobile"><span>PERSONNEL / END</span><h2>THANKS.</h2><p>感谢阅览，期待与你交流。</p></div><div class="thanks-actions"><a href="contact.html">联系我 ↗</a><a href="home.html">返回档案目录 ↗</a></div></div></section></main>'''+utilities()
    (ROOT/'profile.html').write_text(document('人员档案',content,body='class="profile-page"'),encoding='utf-8')

def build_contact():
    content=header(current='contact')+f'''<main id="main" class="contact-main"><div class="contact-atmosphere" aria-hidden="true"><span class="contact-moon"></span><svg viewBox="0 0 1440 900" preserveAspectRatio="none"><ellipse cx="720" cy="450" rx="680" ry="180" transform="rotate(-18 720 450)"/><ellipse cx="720" cy="450" rx="520" ry="375" transform="rotate(24 720 450)"/><path d="M0 450h1440M720 0v900"/><circle cx="720" cy="450" r="6"/></svg></div><div class="contact-layout"><div class="contact-copy"><p class="contact-kicker">PERSONNEL / CONTACT 03</p><h1>建立联系<span>CONTACT.</span></h1><p class="contact-lead">扫描微信二维码，继续这次关于设计的对话。</p><div class="contact-ident"><span class="contact-ident-star">✦</span><div><strong>ZHANGWENYAN</strong><small>微信名 / zwywz</small></div></div><nav class="contact-return" aria-label="返回"><a href="profile.html">← 返回关于我</a><a href="home.html">返回档案目录 ↗</a></nav></div><div class="contact-qr-card"><div class="contact-card-head"><span>WECHAT / ACCESS</span><span class="contact-card-signal"><i></i> SIGNAL AVAILABLE</span></div><div class="contact-qr-mat"><div class="contact-qr-crop"><img src="assets/wechat-qr-source.png" alt="张文砚的微信二维码，可使用微信扫一扫添加好友" width="1179" height="2556"></div></div><div class="contact-card-foot"><span>扫描二维码<br>添加我为好友</span>{CONTACT_ICON}</div></div></div></main>'''+utilities()
    (ROOT/'contact.html').write_text(document('建立联系',content,body='class="contact-page"'),encoding='utf-8')

CASSETTE='''<svg viewBox="0 0 520 340" aria-hidden="true"><path d="M30 46h460v262H30z" class="tape-shell"/><path d="M48 65h424v170H48z" class="tape-label"/><path d="M96 130h328v66H96z" class="tape-window"/><g class="reel reel-a"><circle cx="150" cy="163" r="26"/><circle cx="150" cy="163" r="9"/><path d="M150 137v16m0 20v16m-26-26h16m20 0h16"/></g><g class="reel reel-b"><circle cx="370" cy="163" r="26"/><circle cx="370" cy="163" r="9"/><path d="M370 137v16m0 20v16m-26-26h16m20 0h16"/></g><path d="M122 260h276l24 48H98z" class="tape-bottom"/><circle cx="53" cy="283" r="4"/><circle cx="467" cy="283" r="4"/><text x="64" y="100">ORBITAL / PERSONAL DESIGN RECORDS</text><text x="64" y="220">A — 001</text><text x="405" y="220">2026</text><path d="M10 163h25m450 0h25M260 22v25m0 262v20" class="measure"/></svg>'''

def build_boot():
    particles=''.join(f'<i style="--particle-index:{i}"></i>' for i in range(14))
    content=f'''<main id="main" class="cover-main"><h1 class="sr-only">张文砚作品集 2026</h1>
      <div class="cover-art" aria-hidden="true"><div class="cover-canvas">
        <img class="cover-layer cover-bg" src="assets/layers/cover-bg.png" alt="" fetchpriority="high">
        <img class="cover-layer cover-gradient" src="assets/layers/cover-c.png" alt="">
        <span class="cover-moon-plane"><img class="cover-moon" src="assets/layers/cover-subject-moon.png" alt=""></span>
        <img class="cover-moon-rear" src="assets/layers/cover-orbit2.png" alt="">
        <img class="cover-layer cover-orbits" src="assets/layers/cover_orbit1.png" alt="">
        <div class="cover-wordmark"><span class="cover-discipline">求职意向 ui/ux/产品设计</span></div>
        <img class="cover-layer cover-cats" src="assets/layers/cover-subject-cat.png" alt="">
      </div></div><div class="cover-identity"><strong>ZHANGWENYAN</strong><a href="tel:18792793260">18792793260</a></div>
      <div class="cover-startrail" aria-hidden="true"><svg viewBox="0 0 1600 900" preserveAspectRatio="none"><path d="M-120 620 C260 800 280 115 740 176 S1260 825 1690 230"/><path d="M-100 690 C340 510 530 950 860 720 S1260 90 1740 450"/><circle cx="740" cy="176" r="3"/><circle cx="860" cy="720" r="2"/></svg></div>
      <div class="cover-glitch" aria-hidden="true"></div><div class="cover-particles" aria-hidden="true">{particles}</div><div class="cover-scan" aria-hidden="true"></div>
      <div class="cover-control"><div class="cover-access-row"><div class="cover-loading"><svg class="status-glyph" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="13"/><path d="M22 2v11m0 18v11M2 22h11m18 0h11M17 22l4 4 7-9"/></svg><span id="boot-state" role="status" aria-live="polite">正在读取作品档案</span><strong id="boot-percent">00%</strong></div><a class="enter-button" href="home.html" hidden><svg viewBox="0 0 36 36" aria-hidden="true"><circle cx="18" cy="18" r="12"/><path d="M12 18h12m-5-5 5 5-5 5"/></svg><span>点击进入</span><b>↗</b></a></div><div class="boot-progress" aria-hidden="true"><i></i><span class="progress-beacon"></span></div><div class="boot-steps" aria-hidden="true"><span class="step-load"></span><span class="step-auth"></span><span class="step-enter"></span></div></div>
      <div class="cover-wipe" aria-hidden="true"><span></span><div class="wipe-rings"><i></i><i></i><i></i><b></b></div></div></main>'''
    (ROOT/'index.html').write_text(document('接入个人作品档案',content,body='class="boot-page"'),encoding='utf-8')

build_home()
for i,f in enumerate(FILES): build_project(f,i)
build_profile()
build_contact()
build_boot()
(ROOT/'assets/mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 44"><rect width="44" height="44" rx="8" fill="#171c19"/><g fill="none" stroke="#d3d8b5" stroke-width="1.6"><circle cx="22" cy="22" r="11"/><ellipse cx="22" cy="22" rx="20" ry="6" transform="rotate(-40 22 22)"/></g></svg>',encoding='utf-8')
(ROOT/'.nojekyll').touch()
legacy='<main id="main"><p>正在定位档案…</p>'+''.join(f'<p><a href="projects/{f["id"]}.html">{f["title"]}</a></p>' for f in FILES)+'</main><script>const id=new URLSearchParams(location.search).get("id");if(["pacer","kaihua","shower","practice"].includes(id))location.replace("projects/"+id+".html"+location.hash);else location.replace("home.html");</script>'
(ROOT/'project.html').write_text(document('档案转接',legacy),encoding='utf-8')
print('Built loading, index, profile, contact, 4 project pages, and legacy route.')


