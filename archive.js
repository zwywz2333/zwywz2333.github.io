/* Progressive enhancement. Every record and original image is a normal link. */
(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js');
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const systemMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const storage = {
    get(key) { try { return sessionStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { sessionStorage.setItem(key, value); } catch {} }
  };
  if (storage.get('archive-motion') === 'off') root.classList.add('motion-reduced');
  const reduced = () => systemMotion.matches || root.classList.contains('motion-reduced');
  function updateMotion() {
    $$('.motion-toggle').forEach(button => {
      button.textContent = systemMotion.matches ? '动态效果：跟随系统减少' : `动态效果：${reduced() ? '关闭' : '开启'}`;
      button.disabled = systemMotion.matches;
      button.setAttribute('aria-pressed', String(!reduced()));
    });
    if (reduced()) $$('[data-depth]').forEach(el => el.style.removeProperty('--float'));
  }
  $$('.motion-toggle').forEach(button => button.addEventListener('click', () => {
    root.classList.toggle('motion-reduced');
    storage.set('archive-motion', reduced() ? 'off' : 'on');
    updateMotion();
  }));
  systemMotion.addEventListener('change', updateMotion);
  updateMotion();

  // One instrument cursor spans the viewport on the cover, index, and profile.
  const coverScene = $('.cover-main');
  const directoryScene = $('.directory-main');
  const profileCursor = document.body.classList.contains('profile-page');
  if ((coverScene || directoryScene || profileCursor) && matchMedia('(pointer:fine)').matches) {
    const grid = document.createElement('div');
    grid.className = 'pointer-grid';
    grid.setAttribute('aria-hidden', 'true');
    grid.innerHTML = '<span class="pointer-core"><img src="' + (document.body.dataset.base || '') + 'assets/layers/crosshair-center.png" alt=""></span>';
    document.body.appendChild(grid);
    let x = innerWidth * .25, y = innerHeight * .4, targetX = x, targetY = y, frame = 0, idleTimer = 0;
    const render = () => {
      if (reduced()) { x = targetX; y = targetY; }
      else { const ease = profileCursor ? .48 : .22; x += (targetX - x) * ease; y += (targetY - y) * ease; }
      grid.style.setProperty('--pointer-x', `${x}px`);
      grid.style.setProperty('--pointer-y', `${y}px`);
      if (coverScene) {
        coverScene.style.setProperty('--scan-x', `${x}px`);
        coverScene.style.setProperty('--scan-y', `${y}px`);
        coverScene.style.setProperty('--drift-x', reduced() ? '0' : `${(x / innerWidth - .5).toFixed(3)}`);
        coverScene.style.setProperty('--drift-y', reduced() ? '0' : `${(y / innerHeight - .5).toFixed(3)}`);
      }
      if (directoryScene && !reduced()) {
        directoryScene.style.setProperty('--orbit-x', `${((x / innerWidth - .5) * 34).toFixed(1)}px`);
        directoryScene.style.setProperty('--orbit-y', `${((y / innerHeight - .5) * 26).toFixed(1)}px`);
      }
      if (Math.abs(x - targetX) + Math.abs(y - targetY) > .3) frame = requestAnimationFrame(render);
      else frame = 0;
    };
    const moveCursor = event => {
      targetX = event.clientX; targetY = event.clientY;
      grid.classList.add('is-visible');
      coverScene?.classList.add('tracking');
      if (!frame) frame = requestAnimationFrame(render);
      if (profileCursor) {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(() => grid.classList.remove('is-visible'), 1600);
      }
    };
    window.addEventListener('pointermove', moveCursor, {capture:true,passive:true});
    if (profileCursor) window.addEventListener('mousemove', moveCursor, {capture:true,passive:true});
    document.addEventListener('pointerleave', () => { grid.classList.remove('is-visible'); coverScene?.classList.remove('tracking'); });
    addEventListener('blur', () => grid.classList.remove('is-visible'));
  }

  // Loading is tied to actual critical images; slow resources never block entry.
  if (document.body.classList.contains('boot-page')) {
    let entering = false;
    function enter() {
      if (entering) return;
      entering = true;
      document.body.classList.add('leaving');
      setTimeout(() => location.replace('home.html'), reduced() ? 0 : 870);
    }
    $$('.enter-button').forEach(a => a.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); enter();
    }));
      const assets = ['cover-bg.png','cover-subject-cat.png','cover-subject-moon.png','cover_orbit1.png',
        'directorycard-cover-01.png','directorycard-cover-02.png','directorycard-cover-03.png','directorycard-cover-04.png',
        'directorycard-text-01.png','directorycard-text-02.png','directorycard-text-03.png','directorycard-text-04.png'];
      let completed = 0, failed = 0, assetsDone = false, assetsFinishedAt = 0, stageFinished = false;
      const startedAt = performance.now();
      const minimumProgress = reduced() ? 0 : 1350;
      const finalSweep = reduced() ? 0 : 150;
      const progress = $('.boot-progress');
      let statusRevision = 0;
      function setBootStatus(message) {
        const label = $('#boot-state');
        if (reduced()) { label.textContent = message; return; }
        const revision = ++statusRevision;
        label.animate([{opacity:1,filter:'blur(0)'},{opacity:.12,filter:'blur(2px)',offset:.48},{opacity:1,filter:'blur(0)'}],{duration:480,easing:'ease-in-out'});
        setTimeout(() => { if (revision === statusRevision) label.textContent = message; }, 230);
      }
      function showProgress(value) {
        const percentage = Math.min(100,Math.max(0,value));
        progress.querySelector('i').style.width = `${percentage}%`;
        progress.style.setProperty('--progress-pct', `${percentage}%`);
        $('#boot-percent').textContent = `${String(Math.round(percentage)).padStart(2,'0')}%`;
      }
      function finishLoading() {
        if (stageFinished) return;
        stageFinished = true;
        document.body.classList.add('authenticating');
        setBootStatus(failed ? '部分素材稍后读取 · 验证权限' : '正在验证登录权限');
        setTimeout(() => {
          document.body.classList.add('authenticated');
          setBootStatus('登录权限验证通过');
          setTimeout(() => {
            document.body.classList.add('ready');
            $('.enter-button').hidden = false;
          }, reduced() ? 0 : 500);
        }, reduced() ? 0 : 500);
      }
      function animateProgress(now) {
        const elapsed = now - startedAt;
        let value;
        if (reduced()) value = assetsDone ? 100 : Math.min(92,completed / assets.length * 92);
        else if (elapsed < minimumProgress) value = elapsed / minimumProgress * 92;
        else value = 92 + Math.min(1,(elapsed - minimumProgress) / finalSweep) * 8;
        showProgress(value);
        if (value >= 100) finishLoading();
        else requestAnimationFrame(animateProgress);
      }
      requestAnimationFrame(animateProgress);
      Promise.all(assets.map(asset => new Promise(resolve => {
        const image = new Image();
        let settled = false;
        const done = error => {
          if (settled) return;
          settled = true;
          completed++; if (error) failed++;
          resolve();
        };
        image.onload = () => done(false); image.onerror = () => done(true);
        image.src = `assets/layers/${asset}`;
        setTimeout(() => done(true), 12000);
      }))).then(() => { assetsDone = true; assetsFinishedAt = performance.now(); });
      setTimeout(() => { if (completed < assets.length) setBootStatus('仍在读取作品素材'); }, 4500);
    return;
  }

  $('[data-return-previous]')?.addEventListener('click', () => {
    let sameSite = false;
    try { sameSite = !!document.referrer && new URL(document.referrer).origin === location.origin; } catch {}
    if (sameSite) history.back();
    else location.href = 'profile.html';
  });

  const menu = $('#site-menu');
  const menuTrigger = $('.menu-trigger');
  if (menu && menuTrigger) {
    menuTrigger.addEventListener('click', () => { menu.showModal(); menuTrigger.setAttribute('aria-expanded','true'); });
    menu.addEventListener('close', () => { menuTrigger.setAttribute('aria-expanded','false'); menuTrigger.focus({preventScroll:true}); });
  }
  $$('[data-close]').forEach(button => button.addEventListener('click', () => document.getElementById(button.dataset.close)?.close()));
  window.addEventListener('pageshow', event => { if (event.persisted) $$('dialog[open]').forEach(d => d.close()); });

  // Full-resolution image reading, with native-dialog focus containment.
  const viewer = $('#viewer');
  const images = $$('a[data-page]');
  if (viewer && images.length) {
    const display = $('#viewer-image'), stage = $('.viewer-stage');
    const previous = $('#image-prev'), next = $('#image-next'), zoom = $('#zoom-toggle');
    let current = 0, version = 0, opener = null;
    function resetZoom() {
      stage.classList.remove('is-zoomed'); stage.scrollTo(0,0);
      zoom.textContent = '原尺寸'; zoom.setAttribute('aria-pressed','false');
    }
    function show(index) {
      if (index < 0 || index >= images.length) return;
      current = index; const ticket = ++version, link = images[index];
      resetZoom();
      $('#viewer-caption').textContent = `RECORD / P.${link.dataset.page.padStart(2,'0')} · ${link.dataset.title}`;
      display.alt = `${link.dataset.title}，原始作品集第 ${link.dataset.page} 页`;
      display.src = $('img',link)?.src || `${document.body.dataset.base}assets/portfolio-slides/slide-${link.dataset.page.padStart(2,'0')}.jpg`;
      const full = new Image();
      full.onload = () => { if (ticket === version) display.src = full.src; };
      full.src = link.href;
      previous.disabled = current === 0; next.disabled = current === images.length - 1;
      if (!viewer.open) viewer.showModal();
    }
    images.forEach((link,index) => link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); opener = link; show(index);
    }));
    previous.addEventListener('click', () => show(current - 1));
    next.addEventListener('click', () => show(current + 1));
    zoom.addEventListener('click', () => {
      const expanded = stage.classList.toggle('is-zoomed');
      zoom.textContent = expanded ? '适应屏幕' : '原尺寸'; zoom.setAttribute('aria-pressed',String(expanded));
      stage.scrollTo(0,0);
    });
    viewer.addEventListener('keydown', event => {
      if (stage.classList.contains('is-zoomed')) return;
      if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
      if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
    });
    stage.addEventListener('click', event => { if (event.target === stage) viewer.close(); });
    viewer.addEventListener('close', () => { version++; resetZoom(); opener?.focus({preventScroll:true}); });
  }

  // Optional evidence index. Content is always available without exploring it.
  const clueData = $('#clue-data');
  if (clueData) {
    const clues = JSON.parse(clueData.textContent), buttons = $$('[data-clue]'), panel = $('#clue-panel');
    const key = `archive-clues-${document.body.dataset.project}`;
    let saved; try { saved = JSON.parse(storage.get(key) || '[]'); } catch { saved = []; }
    const visited = new Set(Array.isArray(saved) ? saved : []);
    function updateClues() {
      buttons.forEach((button,index) => button.classList.toggle('explored',visited.has(index)));
      $('#clue-progress').textContent = `${visited.size} / ${clues.length} 已探索`;
    }
    buttons.forEach((button,index) => button.addEventListener('click', () => {
      const wasOpen = button.getAttribute('aria-expanded') === 'true';
      buttons.forEach(b => b.setAttribute('aria-expanded','false'));
      panel.hidden = wasOpen;
      if (!wasOpen) {
        button.setAttribute('aria-expanded','true');
        $('p',panel).textContent = clues[index][1];
        $('a',panel).href = `#chapter-${clues[index][2]}`;
        visited.add(index); storage.set(key, JSON.stringify([...visited])); updateClues();
      }
    }));
    updateClues();
  }

  // Reveal each figure once; all content stays visible when JS is unavailable.
  if ('IntersectionObserver' in window && !reduced()) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), {rootMargin:'0px 0px 20px 0px', threshold:.04});
    $$('[data-reveal]').forEach((el,index) => {
      if (el.getBoundingClientRect().top > innerHeight * .95) {
        el.classList.add('reveal-wait'); el.style.transitionDelay = `${index % 2 * 65}ms`; observer.observe(el);
      }
    });
  }

  const chapters = $$('[data-chapter]'), chapterLinks = $$('[data-chapter-link]');
  chapters.forEach(chapter => {
    const rail = $('.image-sequence', chapter), slides = $$('.plate', rail);
    if (slides.length === 1) chapter.classList.add('single-slide');
    const previous = $('[data-slide-prev]', chapter), next = $('[data-slide-next]', chapter);
    let current = 0, queuedSlide = false;
    function setSlide(index, move = false) {
      current = Math.max(0, Math.min(slides.length - 1, index));
      $('.slide-current', chapter).textContent = String(current + 1).padStart(2,'0');
      $('.slide-track i', chapter).style.width = `${(current + 1) / slides.length * 100}%`;
      previous.disabled = current === 0; next.disabled = current === slides.length - 1;
      if (move) rail.scrollTo({left:slides[current].offsetLeft - rail.offsetLeft - (rail.clientWidth - slides[current].clientWidth) / 2,behavior:reduced()?'instant':'smooth'});
    }
    previous.addEventListener('click', () => setSlide(current - 1, true));
    next.addEventListener('click', () => setSlide(current + 1, true));
    rail.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); setSlide(current + (event.key === 'ArrowRight' ? 1 : -1), true); }
    });
    rail.addEventListener('scroll', () => {
      if (queuedSlide) return; queuedSlide = true;
      requestAnimationFrame(() => { queuedSlide = false; const center = rail.scrollLeft + rail.clientWidth / 2; let nearest = 0;
        slides.forEach((slide,index) => { if (Math.abs(slide.offsetLeft - rail.offsetLeft + slide.clientWidth / 2 - center) < Math.abs(slides[nearest].offsetLeft - rail.offsetLeft + slides[nearest].clientWidth / 2 - center)) nearest = index; });
        if (nearest !== current) setSlide(nearest);
      });
    }, {passive:true});
    setSlide(0);
  });
  const article = $('.project-article');
  const floating = new Set();
  if ('IntersectionObserver' in window) {
    const visible = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) floating.add(entry.target); else floating.delete(entry.target);
    }), {rootMargin:'100px'});
    $$('.image-sequence [data-depth]').forEach(frame => visible.observe(frame));
  }
  let queued = false, activeChapter = -1;
  function syncScroll() {
    queued = false;
    if (article) {
      const rect = article.getBoundingClientRect();
      const progress = Math.max(0,Math.min(1,(innerHeight*.45-rect.top)/Math.max(1,rect.height)));
      root.style.setProperty('--reading',progress);
      $('.reading-percent').textContent = `${String(Math.round(progress*100)).padStart(2,'0')}%`;
      let selected = 0;
      chapters.forEach((chapter,index) => { if (chapter.getBoundingClientRect().top < innerHeight*.4) selected=index; });
      if (selected !== activeChapter) {
        activeChapter = selected;
        chapterLinks.forEach((link,index) => {
          link.classList.toggle('is-active',index === selected);
          if(index === selected) { link.setAttribute('aria-current','location'); link.classList.add('visited'); }
          else link.removeAttribute('aria-current');
        });
        const active = chapterLinks[selected], nav = active?.parentElement;
        if (innerWidth <= 760 && nav && active) nav.scrollTo({left:Math.max(0,active.offsetLeft-nav.offsetLeft-12),behavior:reduced()?'instant':'smooth'});
      }
    }
    if (!reduced() && innerWidth > 760) floating.forEach(frame => {
      const rect = frame.getBoundingClientRect();
      const depth = Number(frame.dataset.depth);
      frame.style.setProperty('--float', `${Math.max(-depth,Math.min(depth,(innerHeight/2-rect.top-rect.height/2)*.018)).toFixed(2)}px`);
    });
  }
  addEventListener('scroll', () => { if (!queued) { queued=true; requestAnimationFrame(syncScroll); } }, {passive:true});
  addEventListener('resize', syncScroll); syncScroll();
  $$('a[href^="#chapter-"]').forEach(link => link.addEventListener('click', () => {
    const target = document.getElementById(link.hash.slice(1));
    if (!target) return;
    target.classList.remove('is-targeted');
    requestAnimationFrame(() => target.classList.add('is-targeted'));
    setTimeout(() => target.classList.remove('is-targeted'),1100);
  }));

  const readout = $('#card-readout');
  $$('[data-card]').forEach(card => {
    const select = () => { if (readout) readout.textContent = `${card.dataset.card.toUpperCase()} / ${card.dataset.caption}`; };
    card.addEventListener('pointerenter',select); card.addEventListener('focus',select);
    card.addEventListener('click',() => storage.set('archive-selected',card.id));
  });
  const directory = $('.directory-main');
  if (directory) {
    let leaving = false;
    if (matchMedia('(pointer:fine)').matches) {
      $$('.directory-card',directory).forEach(card => {
        card.addEventListener('pointermove',event => {
          if (reduced()) return;
          const box = card.getBoundingClientRect();
          const px = (event.clientX - box.left) / box.width - .5;
          const py = (event.clientY - box.top) / box.height - .5;
          card.style.setProperty('--tilt-y', `${px * 9}deg`);
          card.style.setProperty('--tilt-x', `${-py * 9}deg`);
          card.style.setProperty('--card-px', `${px * 14}px`);
          card.style.setProperty('--card-py', `${py * 12}px`);
          card.style.setProperty('--back-x', `${-px * 13}px`);
          card.style.setProperty('--back-y', `${-py * 11}px`);
          card.style.setProperty('--front-x', `${px * 5}px`);
          card.style.setProperty('--front-y', `${py * 5}px`);
          card.style.setProperty('--text-x', `${px * 12}px`);
          card.style.setProperty('--text-y', `${py * 10}px`);
        }, {passive:true});
        card.addEventListener('pointerleave',() => {
          card.style.removeProperty('--tilt-x'); card.style.removeProperty('--tilt-y');
          card.style.removeProperty('--card-px'); card.style.removeProperty('--card-py');
          for (const name of ['--back-x','--back-y','--front-x','--front-y','--text-x','--text-y']) card.style.removeProperty(name);
        });
      });
    }
    $$('.directory-card',directory).forEach(card => card.addEventListener('click',event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || leaving) return;
      event.preventDefault(); leaving = true;
      card.classList.add('is-opening'); directory.classList.add('is-leaving');
      setTimeout(() => { location.href = card.href; }, reduced() ? 0 : 470);
    }));
  }
  const about = $('.about-scene');
  if (about && matchMedia('(pointer:fine)').matches) {
    about.addEventListener('pointermove', event => {
      if (reduced()) return;
      const rect = about.getBoundingClientRect();
      about.style.setProperty('--about-x', `${(((event.clientX - rect.left) / rect.width - .5) * 72).toFixed(1)}px`);
      about.style.setProperty('--about-y', `${(((event.clientY - rect.top) / rect.height - .5) * 58).toFixed(1)}px`);
    }, {passive:true});
    about.addEventListener('pointerleave', () => {
      about.style.setProperty('--about-x','0px');
      about.style.setProperty('--about-y','0px');
    });
  }
  if (about) {
    let aboutFrame = 0;
    const aboutScroll = () => {
      aboutFrame = 0;
      if (reduced()) { about.style.setProperty('--about-scroll','0px'); return; }
      const rect = about.getBoundingClientRect();
      const ratio = Math.max(-1,Math.min(1,(innerHeight / 2 - rect.top - rect.height / 2) / Math.max(innerHeight,rect.height)));
      about.style.setProperty('--about-scroll',`${(ratio * 48).toFixed(1)}px`);
    };
    addEventListener('scroll',() => { if (!aboutFrame) aboutFrame = requestAnimationFrame(aboutScroll); },{passive:true});
    addEventListener('resize',aboutScroll);
    aboutScroll();
  }
  const contactScene = $('.contact-main');
  if (contactScene && matchMedia('(pointer:fine)').matches) {
    contactScene.addEventListener('pointermove', event => {
      if (reduced()) return;
      const rect = contactScene.getBoundingClientRect();
      contactScene.style.setProperty('--contact-x', `${(((event.clientX - rect.left) / rect.width - .5) * 42).toFixed(1)}px`);
      contactScene.style.setProperty('--contact-y', `${(((event.clientY - rect.top) / rect.height - .5) * 36).toFixed(1)}px`);
    },{passive:true});
  }
  const recordsScene = $('.about-records');
  if (recordsScene) {
    const revealRecords = () => {
      if (recordsScene.classList.contains('is-entered')) return;
      const bounds = recordsScene.getBoundingClientRect();
      if (window.scrollY > 60 && bounds.top < innerHeight * .86 && bounds.bottom > 80) {
        recordsScene.classList.add('is-entered');
        window.removeEventListener('scroll', revealRecords);
      }
    };
    window.addEventListener('scroll', revealRecords, {passive:true});
    window.addEventListener('load', revealRecords, {once:true});
    requestAnimationFrame(revealRecords);
    if ('IntersectionObserver' in window) {
      const recordReveal = new IntersectionObserver(entries => entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        if (entry.target.classList.contains('profile-closing')) entry.target.classList.add('is-visible');
        recordReveal.unobserve(entry.target);
      }), {threshold:.12,rootMargin:'0px 0px -8% 0px'});
      const closing = $('.profile-closing');
      if (closing) recordReveal.observe(closing);
    } else {
      recordsScene.classList.add('is-entered');
      $('.profile-closing')?.classList.add('is-visible');
    }
  }
  const instrument = $('.hero-instrument');
  if (instrument && matchMedia('(pointer:fine)').matches) {
    $('.home-hero').addEventListener('pointermove',event => {
      if (reduced()) return;
      const rect = instrument.getBoundingClientRect();
      instrument.style.setProperty('--px',`${Math.max(-8,Math.min(8,(event.clientX-rect.left-rect.width/2)*.018))}px`);
      instrument.style.setProperty('--py',`${Math.max(-6,Math.min(6,(event.clientY-rect.top-rect.height/2)*.025))}px`);
    },{passive:true});
  }
})();
