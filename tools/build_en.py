"""Build the English page and the structured data for both languages.

    python tools/build_en.py

Turkish is written in index.html; English lives in assets/js/i18n.js (the EN dictionary), keyed by the
same data-i18n names. This script:
  1. regenerates the JSON-LD block in index.html from the visible Turkish text,
  2. writes en/index.html: every data-i18n element and data-i18n-attr attribute replaced with English,
     English head metadata, paths adjusted for /en/, and JSON-LD from the visible English text.
Run it after every change to index.html or i18n.js. Do not edit en/index.html by hand.
"""
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
             'legalName': ORG['legal_name'], 'url': SITE + '/', 'description': org_desc, 'knowsLanguage': ['tr', 'en'],
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


def main():
    en = load_en()
    tr = SRC.read_text(encoding='utf-8')

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
    doc = re.sub(r'((?:href|src)=")(assets/|gizlilik\.html|kosullar\.html)', r'\1../\2', doc)
    doc = put_jsonld(doc, graph('en', doc, title, desc))
    doc = doc.replace('<!doctype html>\n', '<!doctype html>\n<!-- Generated by tools/build_en.py from index.html and assets/js/i18n.js. Do not edit by hand. -->\n', 1)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(doc, encoding='utf-8', newline='\n')
    left = re.findall(r'[ğüşıöçĞÜŞİÖÇ]', re.sub(r'<script.*?</script>|aria-label="Türkçe"|>TR<', '', doc, flags=re.S))
    print(f'en/index.html written ({len(doc):,} bytes); Turkish characters left in body: {len(left)}')


if __name__ == '__main__':
    main()
