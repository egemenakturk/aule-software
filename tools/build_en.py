"""Build the English page and the structured data for both languages.

    python tools/build_en.py

Turkish is written in index.html; English lives in assets/js/i18n.js (the EN dictionary), keyed by the
same data-i18n names. This script:
  1. regenerates the JSON-LD block in index.html from the visible Turkish text,
  2. writes en/index.html: every data-i18n element and data-i18n-attr attribute replaced with English,
     English head metadata, paths adjusted for /en/, and JSON-LD from the visible English text.
Run it after every change to index.html or i18n.js. Do not edit en/index.html by hand.
"""
import datetime
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'index.html'
I18N = ROOT / 'assets' / 'js' / 'i18n.js'
OUT = ROOT / 'en' / 'index.html'
SITE = 'https://www.aulesoftware.com'

# Company facts used in the structured data of both pages (supplied by the founders).
ORG = {
    'legal_name': 'Aule Yazılım',
    'address': {'streetAddress': 'Eğitim Mah.', 'addressLocality': 'Kadıköy', 'addressRegion': 'İstanbul',
                'postalCode': '34722', 'addressCountry': 'TR'},
    'email': 'info@aulesoftware.com',
    'same_as': ['https://www.linkedin.com/company/aule-software/'],
    'founders': [('Egemen Doğuş Aktürk', 'egemen.akturk@aulesoftware.com'), ('Mert Kelkit', 'mert.kelkit@aulesoftware.com')],
    'knows_about': {
        'tr': ['Kuruma özel yazılım geliştirme', 'İş süreçleri analizi', 'Süreç otomasyonu', 'Kurumsal intranet platformları',
               'Ödeme sistemleri', 'SWIFT', 'Havayolu rezervasyon sistemleri'],
        'en': ['Custom software development', 'Business process analysis', 'Process automation', 'Enterprise intranet platforms',
               'Payment systems', 'SWIFT', 'Airline reservation systems'],
    },
}


def load_en():
    js = I18N.read_text(encoding='utf-8')
    body = js[js.index('var EN = {') + len('var EN = {'): js.index('\n  };', js.index('var EN = {'))]
    out = {}
    for k, v in re.findall(r"'([A-Za-z0-9._-]+)':\s*'((?:[^'\\]|\\.)*)'", body):
        v = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), v)
        out[k] = v.replace("\\'", "'").replace('\\\\', '\\')
    return out


def element_spans(doc, key):
    """Yield (content_start, content_end) for every element whose opening tag has data-i18n="key"."""
    for m in re.finditer(r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*\sdata-i18n="%s"[^>]*>' % re.escape(key), doc):
        tag, start = m.group(1).lower(), m.end()
        depth, i = 1, start
        pat = re.compile(r'<(/?)%s\b[^>]*?(/?)>' % tag, re.I)
        while depth:
            n = pat.search(doc, i)
            if not n:
                raise ValueError(f'unclosed <{tag}> for {key}')
            if n.group(1):
                depth -= 1
            elif not n.group(2):
                depth += 1
            i = n.end()
        yield start, n.start()


def text_of(fragment):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fragment))).strip()


def visible(doc, key):
    for a, b in element_spans(doc, key):
        return text_of(doc[a:b])
    raise KeyError(key)


def translate_body(doc, en):
    keys = set(re.findall(r'\sdata-i18n="([^"]+)"', doc))
    missing = sorted(k for k in keys if k not in en)
    if missing:
        raise SystemExit('Missing English for: ' + ', '.join(missing))
    for key in sorted(keys, key=len, reverse=True):
        while True:
            spans = list(element_spans(doc, key))
            todo = [s for s in spans if doc[s[0]:s[1]] != en[key]]
            if not todo:
                break
            a, b = todo[0]
            doc = doc[:a] + en[key] + doc[b:]

    def attrs(m):
        tag = m.group(0)
        for pair in m.group(1).split(','):
            name, key = (x.strip() for x in pair.split('='))
            if key not in en:
                raise SystemExit('Missing English for attribute key: ' + key)
            value = html.escape(en[key], quote=True)
            tag = re.sub(r'(\s%s=")[^"]*(")' % re.escape(name), lambda mm: mm.group(1) + value + mm.group(2), tag, count=1)
        return tag
    return re.sub(r'<[^>]*\sdata-i18n-attr="([^"]+)"[^>]*>', attrs, doc)


def graph(lang, doc, title, desc):
    base = SITE + ('/en/' if lang == 'en' else '/')
    faqs = []
    i = 1
    while re.search(r'data-i18n="faq\.%d\.q"' % i, doc):
        faqs.append({'@type': 'Question', 'name': visible(doc, f'faq.{i}.q'),
                     'acceptedAnswer': {'@type': 'Answer', 'text': visible(doc, f'faq.{i}.a')}})
        i += 1
    steps = [visible(doc, f'work.{n}.t') for n in range(1, 6)]
    org_desc = visible(doc, 'work.d')
    return {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'Organization', '@id': SITE + '/#organization', 'name': 'Aule Software', 'alternateName': 'Aule',
             'legalName': ORG['legal_name'], 'url': SITE + '/', 'logo': SITE + '/assets/apple-touch-icon.png',
             'sameAs': ORG['same_as'], 'description': org_desc, 'knowsLanguage': ['tr', 'en'],
             'address': {'@type': 'PostalAddress', **ORG['address']}, 'email': ORG['email'],
             'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales', 'email': ORG['email'], 'availableLanguage': ['Turkish', 'English']},
             'founder': [{'@type': 'Person', 'name': n, 'email': e, 'jobTitle': visible(doc, 'about.role')} for n, e in ORG['founders']],
             'knowsAbout': ORG['knows_about'][lang]},
            {'@type': 'WebSite', '@id': SITE + '/#website', 'url': SITE + '/', 'name': 'Aule Software',
             'inLanguage': ['tr', 'en'], 'publisher': {'@id': SITE + '/#organization'}},
            {'@type': 'WebPage', '@id': base + '#webpage', 'url': base, 'name': title, 'description': desc,
             'inLanguage': lang, 'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': SITE + '/#organization'}},
            {'@type': 'Service', '@id': base + '#service', 'name': visible(doc, 'hero.eyebrow'),
             'serviceType': 'Custom software development', 'provider': {'@id': SITE + '/#organization'},
             'description': visible(doc, 'hero.sub'),
             'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': visible(doc, 'work.eyebrow'),
                                 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s}} for s in steps]}},
            {'@type': 'FAQPage', '@id': base + '#faq', 'isPartOf': {'@id': base + '#webpage'}, 'mainEntity': faqs},
        ],
    }


def put_jsonld(doc, data):
    block = ('  <!--jsonld:start-->\n  <script type="application/ld+json">\n'
             + json.dumps(data, ensure_ascii=False, indent=2).replace('</', '<\\/') + '\n  </script>\n  <!--jsonld:end-->\n')
    return re.sub(r'  <!--jsonld:start-->.*?<!--jsonld:end-->\n', lambda m: block, doc, count=1, flags=re.S)


def head_value(doc, pattern):
    return html.unescape(re.search(pattern, doc).group(1))


LEGAL = [
    # (lang, path, title, h1, source in content/legal/, other-language path, other-language label)
    ('tr', 'gizlilik', 'Gizlilik politikası ve KVKK aydınlatma metni', 'Gizlilik politikası', 'gizlilik.md', 'en/privacy', 'English'),
    ('tr', 'kosullar', 'Kullanım koşulları', 'Kullanım koşulları', 'kosullar.md', 'en/terms', 'English'),
    ('en', 'en/privacy', 'Privacy policy', 'Privacy policy', 'privacy.md', 'gizlilik', 'Türkçe'),
    ('en', 'en/terms', 'Terms of use', 'Terms of use', 'terms.md', 'kosullar', 'Türkçe'),
]
LEGAL_UPDATED = datetime.date(2026, 11, 11)   # change when the texts change


def build_legal():
    """Legal pages live in folders (/gizlilik/, /en/privacy/) so their URLs have no .html on any host.
    Texts are Markdown in content/legal/, rendered with the blog's Markdown subset."""
    import build_blog
    for lang, path, title, h1, src, alt, alt_label in LEGAL:
        body, _ = build_blog.markdown((ROOT / 'content' / 'legal' / src).read_text(encoding='utf-8'))
        up = '../' * (path.count('/') + 1)
        home = up if lang == 'tr' else up + 'en/'
        eyebrow, back, skip = ('Yasal', 'Ana sayfaya dön', 'İçeriğe geç') if lang == 'tr' else ('Legal', 'Back to home', 'Skip to content')
        d = LEGAL_UPDATED
        updated = (f'Son güncelleme: {d.day} {build_blog.MONTHS[d.month - 1]} {d.year}' if lang == 'tr'
                   else f'Last updated: {d.strftime("%B")} {d.day}, {d.year}')
        page = f'''<!doctype html>
<!-- Generated by tools/build_en.py. Do not edit by hand. -->
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>
    (function () {{
      var t = null; try {{ t = localStorage.getItem('aule-theme'); }} catch (e) {{}}
      document.documentElement.setAttribute('data-theme', t === 'light' ? 'light' : 'dark');
    }})();
  </script>
  <title>{title} | Aule Software</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE}/{path}/">
  <link rel="icon" href="{up}favicon.ico" sizes="48x48">
  <link rel="icon" href="{up}assets/favicon-192.png" sizes="192x192" type="image/png">
  <link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
  <link rel="preload" href="{up}assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{up}assets/css/tokens.css">
  <link rel="stylesheet" href="{up}assets/css/aule.css">
</head>
<body>
<a class="au-skip button-sm" href="#content">{skip}</a>
<main id="content" class="au-section">
  <div class="au-container">
    <div class="au-section-head au-measure" style="padding-top: var(--spacing-900)">
      <a class="au-logo au-logo-lg" href="{home}" aria-label="Aule Software">Aule<i>.</i></a>
      <p class="au-eyebrow caption-4">{eyebrow}</p>
      <h1 class="heading-2">{h1}</h1>
      <p class="caption-2 au-muted">{updated}</p>
      <div><a class="au-btn au-btn-secondary" href="{home}">{back}</a> <a class="au-btn au-btn-secondary" href="{up}{alt}/" hreflang="{'en' if lang == 'tr' else 'tr'}" lang="{'en' if lang == 'tr' else 'tr'}">{alt_label}</a></div>
    </div>
    <div class="au-prose body-7 au-legal">
{body}
    </div>
  </div>
</main>
</body>
</html>
'''
        out = ROOT / path / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding='utf-8', newline='\n')
    print('legal pages written:', ', '.join('/' + p[1] + '/' for p in LEGAL))


def build_llms(tr, en, posts):
    """llms.txt (llmstxt.org): a plain summary of the site and links for AI assistants, from the visible text."""
    tr_desc = head_value(tr, r'<meta name="description" content="([^"]*)"')
    a = ORG['address']
    lines = [
        '# Aule Software', '',
        '> ' + visible(tr, 'work.d'), '',
        'English: ' + en['work.d'], '',
        f'- Merkez / Headquarters: {a["streetAddress"]}, {a["postalCode"]} {a["addressLocality"]}, {a["addressRegion"]}, Türkiye',
        f'- İletişim / Contact: {ORG["email"]}',
        '- Kurucular / Founders: ' + ', '.join(n for n, _ in ORG['founders']),
        '- Diller / Languages: Türkçe, English',
        '- LinkedIn: ' + ORG['same_as'][0], '',
        '## Sayfalar / Pages', '',
        f'- [Ana sayfa (Türkçe)]({SITE}/): {tr_desc}',
        f'- [Home page (English)]({SITE}/en/): {en["meta.desc"]}',
        f'- [Blog]({SITE}/blog/): Kuruma özel yazılım, süreç analizi ve yapay zekâ destekli geliştirme üzerine yazılar (Türkçe).', '',
        '## Hizmetler / Services', '',
    ]
    lines += [f'- {visible(tr, f"work.{n}.t")}: {visible(tr, f"work.{n}.d")}' for n in range(1, 6)]
    lines += ['', '## Blog yazıları / Articles (Turkish)', '']
    lines += [f'- [{p["title"]}]({SITE}/blog/{p["slug"]}/): {p["description"]}' for p in posts]
    lines += ['', '## Sık sorulan sorular / FAQ', '']
    i = 1
    while re.search(r'data-i18n="faq\.%d\.q"' % i, tr):
        lines.append(f'- {visible(tr, f"faq.{i}.q")} {visible(tr, f"faq.{i}.a")}')
        i += 1
    lines += ['', '## Optional', '',
              f'- [RSS]({SITE}/blog/rss.xml)',
              f'- [Gizlilik politikası]({SITE}/gizlilik/)',
              f'- [Kullanım koşulları]({SITE}/kosullar/)', '']
    (ROOT / 'llms.txt').write_text('\n'.join(lines), encoding='utf-8', newline='\n')
    print('llms.txt written')


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_blog
    build_blog.main()          # blog pages, the "Son yazılar" block in index.html, sitemap.xml
    build_legal()
    en = load_en()
    tr = SRC.read_text(encoding='utf-8')
    build_llms(tr, en, build_blog.load_posts())

    # Turkish page: structured data from its own visible text
    tr_title = head_value(tr, r'<title>(.*?)</title>')
    tr_desc = head_value(tr, r'<meta name="description" content="([^"]*)"')
    tr = put_jsonld(tr, graph('tr', tr, tr_title, tr_desc))
    SRC.write_text(tr, encoding='utf-8', newline='\n')

    # English page
    doc = translate_body(tr, en)
    title, desc = en['meta.title'], en['meta.desc']
    swaps = [
        ('<html lang="tr" class="no-js" data-href-en="en/">', '<html lang="en" class="no-js" data-href-tr="../">'),
        (f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}/en/">'),
        (f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{SITE}/en/">'),
        ('<meta property="og:locale" content="tr_TR">', '<meta property="og:locale" content="en_US">'),
        ('<meta property="og:locale:alternate" content="en_US">', '<meta property="og:locale:alternate" content="tr_TR">'),
        ('<a href="./" data-lang="tr" hreflang="tr" lang="tr" aria-label="Türkçe" aria-current="true">TR</a>',
         '<a href="../" data-lang="tr" hreflang="tr" lang="tr" aria-label="Türkçe">TR</a>'),
        ('<a href="en/" data-lang="en" hreflang="en" lang="en" aria-label="English">EN</a>',
         '<a href="./" data-lang="en" hreflang="en" lang="en" aria-label="English" aria-current="true">EN</a>'),
    ]
    for a, b in swaps:
        if a not in doc:
            raise SystemExit('Expected markup not found in index.html: ' + a)
        doc = doc.replace(a, b, 1)
    doc = re.sub(r'<title>.*?</title>', lambda m: f'<title>{html.escape(title, quote=False)}</title>', doc, count=1)
    doc = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc, quote=True), doc, count=1)
    doc = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(title, quote=True), doc, count=1)
    doc = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(en['meta.ogDesc'], quote=True), doc, count=1)
    doc = doc.replace(f'{SITE}/assets/og-image.png', f'{SITE}/assets/og-image-en.png')
    # relative paths one level down
    # the blog is Turkish only: no teaser on the English page, menu link goes to the Turkish blog
    doc = re.sub(r'  <!--blog:start-->.*?<!--blog:end-->\n', '', doc, count=1, flags=re.S)
    doc = doc.replace('href="blog/"', 'href="../blog/" hreflang="tr"')
    doc = re.sub(r'((?:href|src)=")(assets/)', r'\1../\2', doc)
    doc = doc.replace('href="gizlilik/"', 'href="privacy/"').replace('href="kosullar/"', 'href="terms/"')
    doc = put_jsonld(doc, graph('en', doc, title, desc))
    doc = doc.replace('<!doctype html>\n', '<!doctype html>\n<!-- Generated by tools/build_en.py from index.html and assets/js/i18n.js. Do not edit by hand. -->\n', 1)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(doc, encoding='utf-8', newline='\n')
    left = re.findall(r'[ğüşıöçĞÜŞİÖÇ]', re.sub(r'<script.*?</script>|aria-label="Türkçe"|>TR<', '', doc, flags=re.S))
    print(f'en/index.html written ({len(doc):,} bytes); Turkish characters left in body: {len(left)}')


if __name__ == '__main__':
    main()
