(function () {
  'use strict';
  var root = document.documentElement;
  root.classList.remove('no-js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var t = function (key, fallback) { return (window.aule && window.aule.t(key)) || fallback; };


  /* Headings marked data-split rise line by line out of a mask. */
  var splitLines = function (el) {
    var parts = el.innerHTML.split(/<br\s*\/?>/i);
    el.innerHTML = parts.map(function (p, i) {
      return '<span class="au-line"><span style="--l:' + i + '">' + p.trim() + '</span></span>';
    }).join(' ');
    el.classList.add('is-split');
  };
  var splitAll = function () { document.querySelectorAll('[data-split]').forEach(splitLines); };
  splitAll();
  document.addEventListener('aule:lang', splitAll);

  /* Staggered groups: number the children so they arrive in order. */
  document.querySelectorAll('.au-stagger').forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) { child.style.setProperty('--i', i); });
  });
  document.querySelectorAll('.au-compare tbody tr').forEach(function (row, i) { row.style.setProperty('--i', i); });

  /* Hero intro once the web font is ready (never waits more than 600ms). */
  var ready = function () {
    if (root.classList.contains('is-ready')) return;
    root.classList.add('is-ready');
    /* once the logo mark has landed, hover reacts without the intro delays */
    setTimeout(function () { document.querySelectorAll('.au-mark').forEach(function (m) { m.classList.add('is-settled'); }); }, 2200);
  };
  var readyTimer = setTimeout(ready, 300);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { clearTimeout(readyTimer); requestAnimationFrame(ready); });
  }

  /* Scroll reveal: each section rises once, never replays. */
  var reveals = document.querySelectorAll('.au-reveal');
  if (!hasIO) {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var revealIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var t = e.target;
          t.classList.add('is-visible');
          revealIO.unobserve(t);
          if (t.classList.contains('au-stagger')) setTimeout(function () { t.classList.add('is-settled'); }, 700 + t.children.length * 90);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
    reveals.forEach(function (el) { revealIO.observe(el); });
  }

  /* Tagline reveal: words light up one at a time as they cross the trigger line. */
  var initTagline = function (el, instant) {
    if (el.__io) el.__io.disconnect();
    var words = [];
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var span = document.createElement('span');
            span.className = 'au-word';
            span.textContent = part;
            frag.appendChild(span);
            words.push(span);
          });
          child.parentNode.replaceChild(frag, child);
        } else if (child.nodeType === 1 && child.tagName !== 'BR') {
          walk(child);
        }
      });
    };
    walk(el);
    if (instant || reduce || !hasIO) { words.forEach(function (w) { w.classList.add('is-on'); }); return; }

    var queue = [], timer = null;
    var drain = function () {
      var next = queue.shift();
      if (!next) { timer = null; return; }
      next.classList.add('is-on');
      timer = setTimeout(drain, 70);
    };
    var wordIO = new IntersectionObserver(function (entries) {
      entries
        .filter(function (e) { return e.isIntersecting; })
        .sort(function (a, b) { return words.indexOf(a.target) - words.indexOf(b.target); })
        .forEach(function (e) { queue.push(e.target); wordIO.unobserve(e.target); });
      queue.sort(function (a, b) { return words.indexOf(a) - words.indexOf(b); });
      if (!timer && queue.length) drain();
    }, { rootMargin: '0px 0px -35% 0px' });
    el.__io = wordIO;
    words.forEach(function (w) { wordIO.observe(w); });
  };
  var taglines = document.querySelectorAll('[data-tagline]');
  taglines.forEach(function (el) { initTagline(el, false); });
  /* After a language switch the text is replaced: split it again, already lit. */
  document.addEventListener('aule:lang', function () {
    taglines.forEach(function (el) { initTagline(el, true); });
  });



  /* Figures count up once when they come into view, formatted for the active language. */
  var counters = Array.prototype.slice.call(document.querySelectorAll('[data-count]'));
  var fmt = function (v) {
    var lang = (window.aule && window.aule.lang) || 'tr';
    try { return new Intl.NumberFormat(lang === 'en' ? 'en-US' : 'tr-TR', { style: 'currency', currency: 'TRY', currencyDisplay: 'narrowSymbol', maximumFractionDigits: 0 }).format(v); }
    catch (e) { return '₺' + Math.round(v); }
  };
  var paint = function (el, v) { el.textContent = fmt(v); };
  counters.forEach(function (el) { el.__target = Number(el.getAttribute('data-count')); paint(el, el.__target); });
  if (hasIO && !reduce && counters.length) {
    counters.forEach(function (el) { paint(el, 0); });
    var countIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        countIO.unobserve(e.target);
        var el = e.target, start = performance.now(), dur = 1400;
        var step = function (now) {
          var p = Math.min(1, (now - start) / dur);
          var eased = 1 - Math.pow(1 - p, 4);
          paint(el, el.__target * eased);
          if (p < 1) requestAnimationFrame(step); else el.__done = true;
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { countIO.observe(el); });
  }
  document.addEventListener('aule:lang', function () {
    counters.forEach(function (el) { if (el.__done || reduce || !hasIO) paint(el, el.__target); });
  });

  /* Service journey: tabs that advance on their own until the visitor takes over. */
  var work = document.querySelector('[data-work]');
  if (work) {
    var wTabs = Array.prototype.slice.call(work.querySelectorAll('[role="tab"]'));
    var wPanels = Array.prototype.slice.call(work.querySelectorAll('[role="tabpanel"]'));
    var current = 0, autoplay = !reduce, inView = false;
    var run = function () {
      wTabs.forEach(function (t) { t.classList.remove('is-running'); });
      if (!autoplay || !inView) return;
      var tab = wTabs[current];
      void tab.offsetWidth; /* restart the progress animation */
      tab.classList.add('is-running');
    };
    var select = function (i, focus) {
      current = (i + wTabs.length) % wTabs.length;
      wTabs.forEach(function (t, k) {
        var on = k === current;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        wPanels[k].classList.toggle('is-active', on);
      });
      if (focus) wTabs[current].focus();
      run();
    };
    wTabs.forEach(function (t, k) {
      t.addEventListener('click', function () { autoplay = false; select(k); });
      t.addEventListener('keydown', function (e) {
        var d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (e.key === 'Home') d = -current; if (e.key === 'End') d = wTabs.length - 1 - current;
        if (d === undefined) return;
        e.preventDefault(); autoplay = false; select(current + d, true);
      });
      t.querySelector('.au-work-progress span').addEventListener('animationend', function () {
        if (autoplay && inView) select(current + 1);
      });
    });
    work.addEventListener('mouseenter', function () { work.classList.add('is-paused'); });
    work.addEventListener('mouseleave', function () { work.classList.remove('is-paused'); });
    work.addEventListener('focusin', function () { work.classList.add('is-paused'); });
    work.addEventListener('focusout', function () { work.classList.remove('is-paused'); });
    if (hasIO) {
      new IntersectionObserver(function (entries) {
        inView = entries[0].isIntersecting;
        run();
      }, { threshold: 0.35 }).observe(work);
    }
    select(0);
  }



  /* Pause infinite animations (CSS and SVG) while their container is off screen. */
  if (hasIO) {
    var loops = document.querySelectorAll('.au-panel, .au-hero-mark, .au-work-stage, .au-tagline-band');
    var loopIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var off = !e.isIntersecting;
        e.target.classList.toggle('is-offscreen', off);
        e.target.querySelectorAll('svg').forEach(function (s) {
          if (typeof s.pauseAnimations === 'function') { if (off) s.pauseAnimations(); else s.unpauseAnimations(); }
        });
      });
    }, { rootMargin: '100px 0px' });
    loops.forEach(function (el) { loopIO.observe(el); });
  }

  /* Theme: dark by default, light on request; the choice is remembered. */
  var themeBtns = document.querySelectorAll('[data-theme-toggle]');
  var themeMeta = document.querySelector('meta[name="theme-color"]');
  var currentTheme = function () { return root.getAttribute('data-theme') === 'light' ? 'light' : 'dark'; };
  var syncTheme = function () {
    var light = currentTheme() === 'light';
    themeBtns.forEach(function (b) {
      b.setAttribute('aria-label', light ? t('toDark', 'Koyu temaya geç') : t('toLight', 'Açık temaya geç'));
    });
    if (themeMeta) themeMeta.setAttribute('content', light ? '#f6f3ec' : '#131209');
  };
  var applyTheme = function (next) {
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('aule-theme', next); } catch (e) {}
    syncTheme();
  };
  themeBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var next = currentTheme() === 'light' ? 'dark' : 'light';
      if (document.startViewTransition && !reduce) document.startViewTransition(function () { applyTheme(next); });
      else applyTheme(next);
    });
  });
  syncTheme();
  document.addEventListener('aule:lang', syncTheme);

  /* Navigation: current section and mobile menu. */
  var navLinks = document.querySelectorAll('[data-nav-link]');
  if (hasIO && navLinks.length) {
    var sections = [];
    navLinks.forEach(function (a) {
      var s = document.querySelector(a.getAttribute('href'));
      if (s && sections.indexOf(s) < 0) sections.push(s);
    });
    var setCurrent = function (id) {
      navLinks.forEach(function (a) {
        if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
    };
    var navIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) setCurrent(e.target.id); });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { navIO.observe(s); });
  }

  var nav = document.querySelector('.au-nav');
  if (nav && !reduce) {
    var lastY = window.pageYOffset, ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.pageYOffset;
        var menuOpen = document.body.style.overflow === 'hidden';
        if (Math.abs(y - lastY) > 4) nav.classList.toggle('is-hidden', y > lastY && y > 160 && !menuOpen && !nav.contains(document.activeElement));
        lastY = y;
        ticking = false;
      });
    }, { passive: true });
  }

  var toggle = document.querySelector('[data-menu-toggle]');
  var menu = document.getElementById('menu');
  if (toggle && menu) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? t('menuClose', 'Menüyü kapat') : t('menuOpen', 'Menüyü aç'));
      menu.classList.toggle('is-open', open);
      menu.setAttribute('aria-hidden', String(!open));
      menu.inert = !open;
      document.body.style.overflow = open ? 'hidden' : '';
      if (open) { var first = menu.querySelector('a'); if (first) first.focus({ preventScroll: true }); }
    };
    setOpen(false);
    toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) { setOpen(false); toggle.focus(); }
    });
  }

  /* Contact form: client side validation, inline errors, calm confirmation. */
  var form = document.querySelector('[data-contact-form]');
  if (form) {
    // Endpoint is Web3Forms (set via data-endpoint on the form); empty = demo mode.
    var ENDPOINT = form.getAttribute('data-endpoint') || '';
    var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    var check = function (input) {
      var field = input.closest('.au-field');
      var error = field.querySelector('.au-field-error');
      var value = input.value.trim();
      var msg = '';
      if (input.required && !value) msg = t('required', 'Bu alan zorunludur.');
      else if (input.type === 'email' && value && !EMAIL.test(value)) msg = t('email', 'Geçerli bir e-posta adresi girin.');
      field.classList.toggle('is-invalid', !!msg);
      input.setAttribute('aria-invalid', String(!!msg));
      error.textContent = msg;
      return !msg;
    };
    form.querySelectorAll('.au-input').forEach(function (input) {
      input.addEventListener('blur', function () { if (input.value) check(input); });
      input.addEventListener('input', function () { if (input.closest('.is-invalid')) check(input); });
    });
    document.addEventListener('aule:lang', function () {
      form.querySelectorAll('.is-invalid .au-input').forEach(check);
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var inputs = Array.prototype.slice.call(form.querySelectorAll('.au-input'));
      var ok = inputs.map(check).every(Boolean);
      if (!ok) { var bad = form.querySelector('[aria-invalid="true"]'); if (bad) bad.focus(); return; }
      var button = form.querySelector('button[type="submit"]');
      var label = button.querySelector('.au-btn-label');
      var original = label.textContent;
      button.setAttribute('aria-busy', 'true');
      button.disabled = true;
      label.textContent = t('sending', 'Gönderiliyor');
      var done = function (success) {
        button.removeAttribute('aria-busy');
        button.disabled = false;
        label.textContent = original;
        if (success !== true) {
          /* Never claim delivery: say what failed and offer the direct address when one is set. */
          var err = form.querySelector('[data-form-error]');
          if (!err) {
            err = document.createElement('p');
            err.className = 'au-form-error caption-2';
            err.setAttribute('data-form-error', '');
            err.setAttribute('role', 'alert');
            button.parentNode.insertBefore(err, button);
          }
          var mail = form.getAttribute('data-fallback-email') || '';
          err.textContent = success === 'offline' ? t('notConnected', 'Çevrimiçi form henüz aktif değil.') : t('failed', 'Mesaj gönderilemedi.');
          if (mail) {
            var a = document.createElement('a');
            a.href = 'mailto:' + mail; a.textContent = mail;
            err.appendChild(document.createTextNode(' ' + t('writeTo', 'Bize doğrudan yazın:') + ' '));
            err.appendChild(a);
          }
          return;
        }
        var stale = form.querySelector('[data-form-error]');
        if (stale) stale.remove();
        var name = (form.elements.name.value.trim().split(/\s+/)[0]) || '';
        var success_ = document.querySelector('[data-form-success]');
        success_.querySelector('[data-success-name]').textContent = t('thanks', 'Teşekkürler') + (name ? ', ' + name + '.' : '.');
        form.reset();
        form.querySelectorAll('.au-field').forEach(function (f) {
          f.classList.remove('is-invalid');
          var i = f.querySelector('.au-input'); if (i) i.removeAttribute('aria-invalid');
          var er = f.querySelector('.au-field-error'); if (er) er.textContent = '';
        });
        form.hidden = true;
        success_.hidden = false;
        success_.focus();
      };
      var again = document.querySelector('[data-form-again]');
      if (again && !again.__bound) {
        again.__bound = true;
        again.addEventListener('click', function () {
          var box = document.querySelector('[data-form-success]');
          var reopen = function () {
            box.hidden = true;
            box.classList.remove('is-closing');
            box.style.height = '';
            form.hidden = false;
            var first = form.querySelector('.au-input'); if (first) first.focus({ preventScroll: true });
          };
          var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
          if (reduce || box.classList.contains('is-closing')) { reopen(); return; }
          // Shrink the card to zero height, then hide it.
          box.style.height = box.offsetHeight + 'px';
          void box.offsetHeight;
          box.classList.add('is-closing');
          box.style.height = '0px';
          setTimeout(reopen, 460);
        });
      }
      if (!ENDPOINT) { setTimeout(function () { done('offline'); }, 400); return; } // no form service connected yet: report it honestly
      fetch(ENDPOINT, { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(form) })
        .then(function (r) { return r.json().then(function (d) { return r.ok && d.success !== false; }, function () { return r.ok; }); })
        .then(done)
        .catch(function () { done(false); });
    });
  }

  var year = document.querySelector('[data-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
