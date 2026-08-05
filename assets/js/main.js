(function(){
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Language (route-based: /en/ and /pt/) ---------- */
  const isPt = document.body.classList.contains('pt') || document.documentElement.lang === 'pt-BR';
  const waText = {
    en: 'Hi Gustavo! I found your website and would like to talk.',
    pt: 'Olá, Gustavo! Encontrei seu site e queria conversar.'
  };
  function updateWaLinks(){
    const msg = waText[isPt ? 'pt' : 'en'];
    document.querySelectorAll('a.wa-link').forEach(a => {
      a.href = 'https://wa.me/5547992537917?text=' + encodeURIComponent(msg);
    });
  }
  updateWaLinks();

  /* ---------- Compass rose ticks (generated) ---------- */
  const ticks = document.getElementById('roseTicks');
  if (ticks){
    let d = '';
    for (let i = 0; i < 72; i++){
      const a = (i * 5) * Math.PI / 180;
      const long = i % 18 === 0, mid = i % 6 === 0;
      const r1 = long ? 268 : mid ? 276 : 282;
      const x1 = 300 + r1 * Math.sin(a), y1 = 300 - r1 * Math.cos(a);
      const x2 = 300 + 292 * Math.sin(a), y2 = 300 - 292 * Math.cos(a);
      d += `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}"${long ? ' stroke="#B08C4A" stroke-opacity=".55"' : ''}/>`;
    }
    ticks.innerHTML = d;
  }

  /* ---------- Nav state ---------- */
  const nav = document.getElementById('nav');
  const hud = document.getElementById('hud');

  /* ---------- Scroll-driven: rose rotation, HUD needle, section tracking ---------- */
  const rose = document.getElementById('roseSpin');
  const needle = document.getElementById('hudNeedle');
  const hudSection = document.getElementById('hudSection');
  const fieldImg = document.getElementById('fieldImg');
  const sections = Array.from(document.querySelectorAll('[data-section-en]'));
  let currentSection = null;
  let ticking = false;

  function updateHudLabel(){
    if (!currentSection){ hudSection.textContent = isPt ? 'Início' : 'Intro'; return; }
    hudSection.textContent = currentSection.dataset[isPt ? 'sectionPt' : 'sectionEn'];
  }

  function onScroll(){
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = window.scrollY;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const p = max > 0 ? y / max : 0;

      nav.classList.toggle('scrolled', y > 40);
      // some perto do fim da página para não cobrir o rodapé
      hud.classList.toggle('visible', y > window.innerHeight * .5 && max - y > 140);

      if (!reduced){
        if (rose) rose.style.transform = `rotate(${p * 140}deg)`;
        if (needle) needle.style.transform = `rotate(${p * 360}deg)`;
        if (fieldImg){
          const r = fieldImg.parentElement.getBoundingClientRect();
          if (r.bottom > 0 && r.top < window.innerHeight){
            const drift = (r.top + r.height/2 - window.innerHeight/2) * -0.10;
            fieldImg.style.transform = `translateY(${drift.toFixed(1)}px)`;
          }
        }
      }

      // section under the viewport center
      const mid = y + window.innerHeight * .5;
      let found = null;
      for (const s of sections){
        const top = s.offsetTop;
        if (mid >= top && mid < top + s.offsetHeight) { found = s; break; }
      }
      if (found !== currentSection){ currentSection = found; updateHudLabel(); }
      ticking = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Compass HUD: tap/click advances to the next section ---------- */
  function hudGo(){
    const mid = window.scrollY + window.innerHeight * .5;
    const next = sections.find(s => s.offsetTop > mid + 1);
    if (next) next.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth' });
    else window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
  }
  hud.addEventListener('click', hudGo);
  hud.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); hudGo(); }
  });

  /* ---------- About: coluna fixa apenas se couber inteira na janela ---------- */
  const aboutSide = document.querySelector('.about-side');
  const aboutPortrait = document.querySelector('.about-portrait');
  function fitAboutSticky(){
    if (!aboutSide) return;
    aboutSide.classList.remove('no-stick','squeeze');
    if (aboutPortrait) aboutPortrait.style.maxWidth = '';
    if (window.innerWidth <= 960) return;
    const fits = () => {
      const top = parseFloat(getComputedStyle(aboutSide).top) || 96;
      return top + aboutSide.offsetHeight + 12 <= window.innerHeight;
    };
    const shrinkPortrait = (minW) => {
      if (!aboutPortrait) return false;
      for (let w = aboutPortrait.offsetWidth; w >= minW; w -= 10){
        aboutPortrait.style.maxWidth = w + 'px';
        if (fits()) return true;
      }
      return false;
    };
    if (fits()) return;
    if (shrinkPortrait(170)) return;
    aboutSide.classList.add('squeeze');
    if (fits() || shrinkPortrait(140)) return;
    aboutSide.classList.remove('squeeze');
    if (aboutPortrait) aboutPortrait.style.maxWidth = '';
    aboutSide.classList.add('no-stick');
  }
  window.addEventListener('resize', fitAboutSticky, { passive: true });
  window.addEventListener('load', fitAboutSticky);
  fitAboutSticky();

  /* ---------- Reveal on intersection ---------- */
  const io = new IntersectionObserver((entries) => {
    for (const e of entries){
      if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
    }
  }, { threshold: .18, rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  /* ---------- Diagrams: hydrate from assets, then animate ---------- */
  async function injectDiagrams(){
    const slots = Array.from(document.querySelectorAll('.diagram-slot[data-svg-src]'));
    if (!slots.length) return;
    await Promise.all(slots.map(async (slot) => {
      try {
        const res = await fetch(slot.getAttribute('data-svg-src'), { credentials: 'same-origin' });
        if (!res.ok) throw new Error(res.status + ' ' + slot.getAttribute('data-svg-src'));
        const wrap = document.createElement('div');
        wrap.innerHTML = (await res.text()).trim();
        const svg = wrap.querySelector('svg');
        if (!svg) return;
        const id = slot.getAttribute('data-svg-id');
        if (id) svg.setAttribute('id', id);
        const label = slot.getAttribute('aria-label');
        if (label && !svg.getAttribute('aria-label')) svg.setAttribute('aria-label', label);
        slot.replaceWith(svg);
      } catch (err) {
        console.error('Diagram load failed', err);
      }
    }));
  }

  function bindDiagrams(){
    const ioDiag = new IntersectionObserver((entries) => {
      for (const e of entries){
        if (e.isIntersecting){ e.target.classList.add('drawn'); ioDiag.unobserve(e.target); }
      }
    }, { threshold: .35 });
    document.querySelectorAll('.diagram').forEach(el => ioDiag.observe(el));
    document.querySelectorAll('.diagram').forEach(svg => {
      svg.addEventListener('click', () => {
        if (!svg.classList.contains('drawn') || reduced) return;
        svg.classList.add('replay');
        svg.classList.remove('drawn');
        void svg.getBoundingClientRect();
        requestAnimationFrame(() => requestAnimationFrame(() => {
          svg.classList.remove('replay');
          svg.classList.add('drawn');
        }));
      });
    });
  }

  /* ---------- Counters: count up once ---------- */
  function fmt(n, mode){
    if (mode === 'compact') return n >= 1000000 ? (n/1000000).toFixed(n%1000000?1:0) + 'M' : n >= 1000 ? Math.round(n/1000) + 'K' : String(n);
    if (mode === 'k') return n >= 1000 ? Math.round(n/1000) + 'K' : String(n);
    return String(n);
  }
  const ioCount = new IntersectionObserver((entries) => {
    for (const e of entries){
      if (!e.isIntersecting) continue;
      ioCount.unobserve(e.target);
      const el = e.target, target = +el.dataset.target, mode = el.dataset.format;
      if (reduced){ el.textContent = fmt(target, mode); continue; }
      const dur = 1600, t0 = performance.now();
      (function step(t){
        const k = Math.min((t - t0) / dur, 1);
        const eased = 1 - Math.pow(1 - k, 4); // strong ease-out
        el.textContent = fmt(Math.round(target * eased), mode);
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    }
  }, { threshold: .6 });
  document.querySelectorAll('.count').forEach(el => ioCount.observe(el));

  /* ---------- Magnetic buttons (subtle, spring-back) ---------- */
  if (!reduced && matchMedia('(pointer:fine)').matches){
    document.querySelectorAll('.magnetic').forEach(btn => {
      btn.addEventListener('mousemove', (ev) => {
        const r = btn.getBoundingClientRect();
        const dx = (ev.clientX - r.left - r.width/2) / r.width;
        const dy = (ev.clientY - r.top - r.height/2) / r.height;
        btn.style.transform = `translate(${dx*7}px, ${dy*5}px)`;
      });
      btn.addEventListener('mouseleave', () => {
        btn.style.transition = 'transform .5s cubic-bezier(.16,1,.3,1)';
        btn.style.transform = '';
        setTimeout(() => btn.style.transition = '', 500);
      });
    });
  }

  injectDiagrams().then(bindDiagrams).catch((err) => {
    console.error(err);
    bindDiagrams();
  });
})();
