/* Aule Software — two languages.
 * Turkish lives in the HTML; English lives in EN below, keyed by data-i18n.
 * data-i18n="key"            → element content (may hold <br> or <span>)
 * data-i18n-attr="attr=key"  → attribute values, comma separated
 * The language is chosen in <head> before first paint (?lang=, saved choice, then location).
 */
(function () {
  'use strict';
  var STORE = 'aule-lang';
  var root = document.documentElement;

  var EN = {
    'skip': 'Skip to content',
    'nav.label': 'Main menu',
    'nav.home': 'Aule Software, back to top',
    'nav.services': 'Services',
    'nav.approach': 'Approach',
    'nav.process': 'Process',
    'nav.faq': 'FAQ',
    'nav.contact': 'Contact',
    'nav.commitments': 'Commitments',
    'lang.label': 'Language',
    'cta': 'Book a consultation',

    'hero.eyebrow': 'Enterprise digital transformation',
    'hero.title': 'Software that raises<br> efficiency and lowers<br> operating costs.',
    'trust.1': 'You own the source code',
    'trust.2': 'Annual maintenance and technical support',
    'hero.sub': 'We analyze how your departments work, then design and build software tailored to your organization to make your operations faster and leaner.',

    'map.label': 'Diagram showing your departments brought together on one tailored platform',
    'map.d1': 'Finance',
    'map.d2': 'Human resources',
    'map.d3': 'Operations',
    'map.d4': 'Procurement',
    'map.d5': 'Sales',
    'map.core': 'Your tailored platform',
    'map.live': 'Live',
    'map.t1': 'Request approved',
    'map.t2': 'Invoice matched',
    'map.t3': 'Report sent',
    'map.s3': 'HR',
    'map.sync': 'Syncing',
    'map.m1': 'Automation',
    'map.m2': 'Integrated data',
    'map.m3': 'Reporting',
    'map.k1': 'Efficiency',
    'map.k2': 'Operating costs',

    'value.eyebrow': 'Why Aule',
    'value.title': 'Digital transformation,<br> measurable results.',
    'value.1.t': 'Higher efficiency',
    'value.1.d': 'We automate repetitive work so your teams can focus on what creates value.',
    'value.2.t': 'Lower operating costs',
    'value.2.d': 'We permanently reduce the cost of manual processes and calculate the return on investment upfront.',
    'value.3.t': 'Built around your processes',
    'value.3.d': 'Rather than adapting to a packaged product, your software is built around the way your departments work.',

    'value.4.t': 'Fast and economical with AI',
    'value.4.d': 'AI accelerated engineering sharply reduces the cost and delivery time of software built for your organization.',
    'value.4.a': 'Traditional',
    'value.4.b': 'With Aule',

    'work.eyebrow': 'Services and process',
    'work.title': 'From analysis to ongoing support,<br> one partner.',
    'work.label': 'Service steps',
    'work.1.t': 'Analysis',
    'work.1.d': 'Through one to one sessions with your departments, we map current workflows and uncover repetitive manual steps and hidden costs. We quantify staff hours, error rates and opportunity cost together.',
    'work.2.t': 'Solution design',
    'work.2.d': 'We prioritize the areas with the highest automation potential and set out the return on investment and implementation roadmap for each proposal. What gets built, in what order and over what timeline is clear from the start.',
    'work.3.t': 'Development',
    'work.3.d': 'We build secure web platforms that fit your internal infrastructure, including user and role management, reporting dashboards and integration with your existing systems. AI accelerated engineering lets us move in short iterations, testing alongside your teams.',
    'work.4.t': 'Training and rollout',
    'work.4.d': 'We roll the system out in stages and give every user group practical training. With user guides and change management support, the software becomes part of daily work from day one.',
    'work.5.t': 'Maintenance and support',
    'work.5.d': 'Under annual maintenance and technical support, we take care of security updates, performance improvements and new feature development. Your systems stay current and secure long after launch.',
    'viz.1.title': 'Manual workload map',
    'viz.1.tag': 'Analysis report',
    'viz.opportunity': 'Opportunity',
    'viz.2.title': 'Prioritized proposals',
    'viz.proposal': 'Proposal',
    'viz.roi': 'Return on investment',
    'viz.priority': 'Priority',
    'viz.3.title': 'Delivery iterations',
    'viz.3.live': 'Live',
    'viz.3.a': 'Design',
    'viz.3.b': 'Build',
    'viz.3.c': 'Test',
    'viz.4.title': 'Team adoption',
    'viz.4.tag': 'Training complete',
    'viz.5.title': 'Annual maintenance plan',
    'viz.5.tag': 'Annual plan',
    'viz.5.a': 'Security updates',
    'viz.5.b': 'Performance monitoring',
    'viz.5.c': 'Technical support',
    'viz.5.d': 'New development',
    'viz.5.ok': 'Up to date',
    'viz.5.active': 'Active',
    'viz.5.avail': 'Available',
    'viz.5.plan': 'Scheduled',

    'nav.cases': 'Projects',
    'work.1.o1': 'Workflow map',
    'work.1.o2': 'Cost analysis',
    'work.1.o3': 'Opportunity report',
    'work.2.o1': 'Prioritization',
    'work.2.o2': 'ROI case',
    'work.2.o3': 'Roadmap',
    'work.3.o1': 'Intranet platform',
    'work.3.o2': 'Roles and permissions',
    'work.3.o3': 'Reporting dashboards',
    'work.4.o1': 'Practical training',
    'work.4.o2': 'User guides',
    'work.4.o3': 'Change management',
    'work.5.o1': 'Security updates',
    'work.5.o2': 'Performance monitoring',
    'work.5.o3': 'New features',
    'cases.eyebrow': 'Projects',
    'cases.title': 'Transformation,<br> in numbers.',
    'cases.d': 'Two projects we delivered in different departments, and their results.',
    'cases.note': 'Costs show annual operating costs; the software investment is listed separately. We work out the numbers for your own processes together after the analysis.',
    'case.problem': 'Challenge',
    'case.solution': 'Solution',
    'case.ledger': 'Cost comparison',
    'case.opex': 'Annual operating cost',
    'case.manual': 'Manual process',
    'case.after': 'After software',
    'case.invest': 'Software investment',
    'case.save': 'Annual operating savings',
    'case.1.tag': 'Banking · Human resources',
    'case.1.title': 'HR events and training management',
    'case.1.sub': 'The HR department of a large bank ran its year round events and training programs entirely by hand.',
    'case.1.prob': 'Event planning, attendee tracking, venue and catering, and training certificates all ran on Excel and email. Two employees ran these processes.',
    'case.1.sol': 'An intranet based event management platform: automatic invitations, attendance tracking, venue and catering management, certificate generation and reporting on a single screen.',
    'case.1.roi': 'The investment pays for itself in about 10 months',
    'case.2.tag': 'Energy · Legal',
    'case.2.title': 'Contract and legal process tracking',
    'case.2.sub': 'The legal department of an energy company tracked hundreds of supplier contracts and legal matters with paper files and Excel.',
    'case.2.prob': 'Contract renewals were missed, case tracking was difficult and regulatory changes were noticed late. Everyone in the department had to set time aside for this tracking now and then, and searching for files had become part of the daily routine.',
    'case.2.sol': 'A digital contract management system: automatic renewal reminders, a case calendar, a regulatory tracking module, approval workflows and search.',
    'case.2.roi': 'The investment pays for itself in about 10 months',
    'value.manual': 'Manual',
    'value.auto': 'Automated',
    'value.1.b1': 'Data entry',
    'value.1.b2': 'Approval workflows',
    'value.1.b3': 'Reporting',
    'value.1.b4': 'Notifications',
    'value.2.today': 'Today',
    'value.2.aule': 'With Aule',
    'value.2.manual': 'Manual work',
    'value.2.value': 'Value adding work',
    'value.3.f1': 'Request',
    'value.3.f2': 'Approval',
    'value.3.f3': 'Purchasing',
    'value.3.f4': 'Invoice',
    'value.4.p1': 'Analysis',
    'value.4.p2': 'Design',
    'value.4.p3': 'Build',
    'value.4.p4': 'Test',
    'tagline.label': 'Our principle',
    'tagline': 'Packaged software<br> is built for everyone.<br> We build for you.',

    'services.eyebrow': 'Services',
    'services.title': 'From analysis to training,<br> end to end.',
    'services.1.t': 'Business analysis',
    'services.1.d': 'We review departmental processes on site and identify opportunities to raise efficiency and cut costs.',
    'services.2.t': 'Solution design',
    'services.2.d': 'Prioritized product proposals grounded in analysis, each with a calculated return on investment.',
    'services.3.t': 'Software development',
    'services.3.d': 'AI accelerated engineering that delivers software tailored to your organization quickly and economically.',
    'services.4.t': 'Training and adoption',
    'services.4.d': 'User training that ensures your teams adopt the new system from day one.',

    'approach.eyebrow': 'Approach',
    'approach.title': 'Packaged software,<br> or software built for you?',
    'approach.d': 'What makes the difference is software built around your processes, and owned entirely by you.',
    'compare.caption': 'Packaged software compared with Aule',
    'compare.feature': 'Capability',
    'compare.pkg': 'Packaged software',
    'compare.1': 'Designed around your processes',
    'compare.2': 'Only the functionality you need',
    'compare.3': 'On site process analysis',
    'compare.4': 'Return on investment calculated upfront',
    'compare.5': 'Source code ownership',
    'compare.no': 'No',
    'compare.yes': 'Yes',

    'process.eyebrow': 'Process',
    'process.title': 'A clear process<br> in four steps.',
    'process.1.t': 'Analysis',
    'process.1.d': 'We study your departments’ processes on site and report the efficiency and cost opportunities.',
    'process.2.t': 'Development',
    'process.2.d': 'We build the prioritized solution in short iterations and test it together with your teams.',
    'process.3.t': 'Training and rollout',
    'process.3.d': 'We roll out the system and secure lasting adoption through user training.',

    'process.4.t': 'Maintenance and support',
    'process.4.d': 'Annual maintenance and technical support keep your systems current and secure.',

    'commit.eyebrow': 'Our commitments',
    'commit.title': 'A long term<br> partnership.',
    'commit.1.t': 'You own the code',
    'commit.1.d': 'The source code and data of everything we build belong entirely to your organization.',
    'commit.2.t': 'Project based pricing',
    'commit.2.d': 'Every project is priced on its own scope, so you never pay for anything you do not need.',
    'commit.3.t': 'Annual maintenance and support',
    'commit.3.d': 'Your systems stay current and secure after launch, and we are there whenever you need us.',

    'faq.eyebrow': 'FAQ',
    'faq.title': 'Frequently asked questions',
    'faq.1.q': 'Which organizations do you work with?',
    'faq.1.a': 'Organizations of any size whose operations rely on repetitive or manual processes and who want to raise efficiency.',
    'faq.2.q': 'Why bespoke software instead of a packaged product?',
    'faq.2.a': 'Packaged products are designed for common needs and require you to adapt your processes to them. Bespoke software fits your existing workflow, and you invest only in the functionality you need.',
    'faq.3.q': 'Doesn’t bespoke software require a large budget?',
    'faq.3.a': 'AI accelerated engineering has significantly reduced both cost and delivery time. Every proposal we make comes with its expected payback period.',
    'faq.4.q': 'How does an engagement begin?',
    'faq.4.a': 'An initial consultation defines your goals and priority departments. We then analyze your processes on site and report our recommendations.',
    'faq.5.q': 'How will our teams adapt to the new system?',
    'faq.5.a': 'User training is an integral part of our service. We provide practical training to your teams as the system goes live.',
    'faq.6.q': 'How is pricing determined?',
    'faq.6.a': 'Pricing depends on the scope of each project. After the analysis, we present a tailored proposal together with the expected return on investment.',
    'faq.7.q': 'Who owns the source code and data?',
    'faq.7.a': 'The source code and all data of the software we build belong to your organization.',
    'faq.8.q': 'Do you provide support after launch?',
    'faq.8.a': 'Yes. Our annual maintenance and technical support keeps your systems current and secure, and we are on hand whenever you need us.',

    'contact.eyebrow': 'Contact',
    'contact.title': 'Let’s plan your transformation together.',
    'contact.d': 'In a short initial consultation, we will discuss your goals and priority processes.',
    'contact.b1': 'Analysis first, then a proposal',
    'contact.b2': 'You own the source code and data',
    'contact.b3': 'Annual maintenance and technical support',

    'form.name': 'Full name',
    'form.email': 'Work email',
    'form.emailPh': 'name@company.com',
    'form.company': 'Company <span class="au-muted">(optional)</span>',
    'form.message': 'How can we help?',
    'form.messagePh': 'Briefly describe your goals and priority processes.',
    'form.note': 'Your details are used only to respond to your enquiry.',
    'form.success': 'We have received your message and will be in touch shortly.',
    'form.again': 'Send another message',

    'footer.tag': 'Enterprise digital transformation and bespoke software.',
    'footer.privacy': 'Privacy policy',
    'footer.terms': 'Terms of use',

    '404.eyebrow': '404',
    '404.title': 'This page could not be found.',
    '404.d': 'The link may be out of date or the address may be mistyped.',
    'back': 'Back to home',
    'legal': 'Legal',
    'privacy.d': '{{privacy policy text, to be provided by your legal advisor}}',
    'terms.d': '{{terms of use text, to be provided by your legal advisor}}'
  };

  /* Strings used by scripts (form validation, menu). */
  var MSG = {
    tr: {
      required: 'Bu alan zorunludur.',
      email: 'Geçerli bir mail adresi girin. Örnek: ad@sirket.com',
      sending: 'Gönderiliyor',
      failed: 'Mesaj gönderilemedi. Lütfen bağlantınızı kontrol edip tekrar deneyin.',
      thanks: 'Teşekkürler',
      menuOpen: 'Menüyü aç',
      menuClose: 'Menüyü kapat',
      toLight: 'Açık temaya geç',
      toDark: 'Koyu temaya geç'
    },
    en: {
      required: 'This field is required.',
      email: 'Enter a valid email address, for example name@company.com',
      sending: 'Sending',
      failed: 'Your message could not be sent. Please check your connection and try again.',
      thanks: 'Thank you',
      menuOpen: 'Open menu',
      menuClose: 'Close menu',
      toLight: 'Switch to light theme',
      toDark: 'Switch to dark theme'
    }
  };

  var META = {
    tr: { title: document.title, desc: (document.querySelector('meta[name="description"]') || {}).content || '', locale: 'tr_TR' },
    en: {
      title: document.body.getAttribute('data-title-en') || 'Aule Software | Enterprise digital transformation and bespoke software',
      desc: document.body.getAttribute('data-desc-en') || 'Aule Software analyzes how your departments work and builds tailored software that raises efficiency and lowers operating costs.',
      locale: 'en_US'
    }
  };

  /* Remember the Turkish originals from the HTML. */
  var nodes = Array.prototype.slice.call(document.querySelectorAll('[data-i18n]'));
  nodes.forEach(function (el) { el.__tr = el.innerHTML; });
  var attrNodes = Array.prototype.slice.call(document.querySelectorAll('[data-i18n-attr]'));
  attrNodes.forEach(function (el) {
    el.__trAttr = {};
    el.getAttribute('data-i18n-attr').split(',').forEach(function (pair) {
      var name = pair.split('=')[0].trim();
      el.__trAttr[name] = el.getAttribute(name);
    });
  });

  var current = root.lang === 'en' ? 'en' : 'tr';

  function apply(lang) {
    current = lang;
    nodes.forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      el.innerHTML = lang === 'en' && EN[key] != null ? EN[key] : el.__tr;
    });
    attrNodes.forEach(function (el) {
      el.getAttribute('data-i18n-attr').split(',').forEach(function (pair) {
        var parts = pair.split('='), name = parts[0].trim(), key = (parts[1] || '').trim();
        el.setAttribute(name, lang === 'en' && EN[key] != null ? EN[key] : el.__trAttr[name]);
      });
    });
    root.lang = lang;
    document.title = META[lang].title;
    var desc = document.querySelector('meta[name="description"]');
    if (desc) desc.setAttribute('content', META[lang].desc);
    var loc = document.querySelector('meta[property="og:locale"]');
    if (loc) loc.setAttribute('content', META[lang].locale);
    document.querySelectorAll('[data-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang));
    });
    root.classList.remove('i18n-pending');
    document.dispatchEvent(new CustomEvent('aule:lang', { detail: { lang: lang } }));
  }

  function set(lang) {
    if (lang === current) return;
    try { localStorage.setItem(STORE, lang); } catch (e) {}
    try {
      var url = new URL(location.href);
      url.searchParams.set('lang', lang);
      history.replaceState(null, '', url);
    } catch (e) {}
    apply(lang);
  }

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-lang]');
    if (b) set(b.getAttribute('data-lang'));
  });

  window.aule = {
    get lang() { return current; },
    t: function (key) { return MSG[current][key]; },
    set: set
  };

  apply(current);
})();
