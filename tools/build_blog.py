"""Build the Turkish and English blog from Markdown.

    python tools/build_en.py        (runs this first, then builds the English page and the English blog)

Turkish posts live in content/blog/*.md, English posts in content/blog/en/*.md, each with a front matter block:

    ---
    title: Hazır yazılım mı, kuruma özel yazılım mı? Karar rehberi
    description: One or two sentences for search results and the post header.
    slug: hazir-yazilim-mi-kuruma-ozel-yazilim-mi
    date: 2026-11-09
    author: egemen            (a key of AUTHORS below)
    category: Karar rehberi
    order: 1                  (optional; lower comes first on the same date)
    tr: <turkish slug>        (English posts only: the Turkish post this one translates)
    ---

Supported Markdown: ## and ### headings, paragraphs, - and 1. lists, > callouts, pipe tables,
**bold**, `code` and [links](url). This script writes:
  blog/ and en/blog/ (index, posts, rss.xml), the "Son yazılar" block in index.html (between
  <!--blog:start--> and <!--blog:end-->) and sitemap.xml. build_en.py puts the English block
  into en/index.html and calls build_pages('en', ...).
"""
import datetime
import html
import json
import math
import re
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://www.aulesoftware.com'
SRC = {'tr': ROOT / 'content' / 'blog', 'en': ROOT / 'content' / 'blog' / 'en'}
HOME = {'tr': '/', 'en': '/en/'}          # home page path per language
BLOG = {'tr': '/blog/', 'en': '/en/blog/'}

AUTHORS = {
    'egemen': {'name': 'Egemen Doğuş Aktürk', 'initials': 'EA',
               'email': 'egemen.akturk@aulesoftware.com',
               'bio': {'tr': 'Bankacılık ve havacılık sektörlerinde 7 yılı aşkın deneyim. ISO standartlarına uygun uluslararası SWIFT para transferi ürününde ve IATA standartlarına uygun havayolu rezervasyon sistemlerinde görev aldı.',
                       'en': 'More than 7 years of experience in banking and aviation. Worked on an international SWIFT money transfer product built to ISO standards and on airline reservation systems built to IATA standards.'}},
    'mert': {'name': 'Mert Kelkit', 'initials': 'MK',
             'email': 'mert.kelkit@aulesoftware.com',
             'bio': {'tr': 'Bankacılık sektöründe 7 yılı aşkın deneyim. ISO standartlarına uygun uluslararası SWIFT para transferi ürününde ve 10\'dan fazla bankada kullanılan TCMB FAST ve KOLAS ürünlerinde görev aldı.',
                     'en': 'More than 7 years of experience in banking. Worked on an international SWIFT money transfer product built to ISO standards and on the Central Bank of the Republic of Türkiye FAST and KOLAS products used by more than 10 banks.'}},
}

T = {
    'tr': dict(
        html_lang='tr', locale='tr_TR', locale_alt='en_US', og_image='og-image.png', skip='İçeriğe geç',
        role='Kurucu Ortak', home='Ana sayfa', crumbs='İçerik yolu', toc='İçindekiler', related='Diğer yazılar',
        author='Yazar', read='dk okuma', mins='dk',
        cta_eyebrow='Ön görüşme', cta_title='Bu yazıdaki konuları kurumunuz için konuşalım.',
        cta_text='Kısa bir ön görüşmede hedeflerinizi ve öncelikli süreçlerinizi birlikte değerlendirelim.',
        cta_btn='Ön görüşme planlayın',
        index_title='Blog | Aule Software', index_h1='Kuruma özel yazılım ve<br> dijital dönüşüm üzerine.',
        index_desc='Kuruma özel yazılım, iş süreçleri analizi ve dijital dönüşüm üzerine Aule Software kurucularının yazıları.',
        teaser_title='Son yazılar', all_posts='Tüm yazılar',
        teaser_desc='Kuruma özel yazılım, süreç analizi ve dijital dönüşüm üzerine kurucularımızın yazıları.',
        rss_desc='Kuruma özel yazılım, iş süreçleri analizi ve dijital dönüşüm üzerine yazılar.'),
    'en': dict(
        html_lang='en', locale='en_US', locale_alt='tr_TR', og_image='og-image-en.png', skip='Skip to content',
        role='Founding Partner', home='Home', crumbs='Breadcrumb', toc='Contents', related='More articles',
        author='Author', read='min read', mins='min',
        cta_eyebrow='Consultation', cta_title='Let’s talk about these topics for your organization.',
        cta_text='In a short introductory call, we will review your goals and priority processes together.',
        cta_btn='Book a consultation',
        index_title='Blog | Aule Software', index_h1='On custom software and<br> digital transformation.',
        index_desc='Articles by the founders of Aule Software on custom software, business process analysis and digital transformation.',
        teaser_title='Latest articles', all_posts='All articles',
        teaser_desc='Articles by our founders on custom software, process analysis and digital transformation.',
        rss_desc='Articles on custom software, business process analysis and digital transformation.'),
}
MONTHS = {'tr': ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'],
          'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}
ARROW = '<svg class="au-icon" viewBox="0 0 256 256" aria-hidden="true"><line x1="40" y1="128" x2="216" y2="128"/><polyline points="144 56 216 128 144 200"/></svg>'


# ── Markdown ──────────────────────────────────────────────────────

def slugify(text):
    t = text.lower()
    for a, b in zip('çğıöşüâîû', 'cgiosuaiu'):
        t = t.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)

    def link(m):
        href = html.escape(m.group(2), quote=True)
        ext = href.startswith('http') and 'aulesoftware.com' not in href
        rel = ' rel="noopener" target="_blank"' if ext else ''
        return f'<a href="{href}"{rel}>{m.group(1)}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)


def markdown(src):
    """Return (html, toc) for the subset of Markdown described in the module docstring."""
    out, toc = [], []
    lines = src.strip('\n').split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r'(#{2,3}) (.+)', line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            anchor = slugify(text)
            if level == 2:
                toc.append((anchor, text))
            cls = 'heading-4' if level == 2 else 'heading-6'
            out.append(f'<h{level} id="{anchor}" class="{cls}">{inline(text)}</h{level}>')
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            t = ['<div class="au-table-wrap"><table class="au-table">', '<thead><tr>' + ''.join(f'<th scope="col">{inline(c)}</th>' for c in head) + '</tr></thead><tbody>']
            for r in body:
                t.append('<tr>' + ''.join((f'<th scope="row">{inline(c)}</th>' if k == 0 else f'<td>{inline(c)}</td>') for k, c in enumerate(r)) + '</tr>')
            t.append('</tbody></table></div>')
            out.append(''.join(t))
            continue
        if line.startswith('> '):
            paras, cur = [], []
            while i < len(lines) and lines[i].startswith('>'):
                text = lines[i][1:].strip()
                if text:
                    cur.append(text)
                elif cur:
                    paras.append(' '.join(cur)); cur = []
                i += 1
            if cur:
                paras.append(' '.join(cur))
            out.append('<aside class="au-callout">' + ''.join(f'<p>{inline(x)}</p>' for x in paras) + '</aside>')
            continue
        if re.match(r'(- |\d+\. )', line):
            ordered = bool(re.match(r'\d+\. ', line))
            items = []
            while i < len(lines) and re.match(r'(- |\d+\. )', lines[i]):
                items.append(re.sub(r'^(- |\d+\. )', '', lines[i]))
                i += 1
                while i < len(lines) and lines[i].startswith('  ') and lines[i].strip():
                    items[-1] += ' ' + lines[i].strip()
                    i += 1
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
            continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'(#{2,3} |\||> |- |\d+\. )', lines[i]):
            buf.append(lines[i].strip())
            i += 1
        out.append(f'<p>{inline(" ".join(buf))}</p>')
    return '\n'.join(out), toc


# ── Posts ─────────────────────────────────────────────────────────

def load_posts(lang='tr'):
    posts = []
    for f in sorted(SRC[lang].glob('*.md')):
        raw = f.read_text(encoding='utf-8')
        m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
        if not m:
            raise SystemExit(f'{f.name}: missing front matter')
        meta = {k: re.sub(r'^"(.*)"$', r'\1', v)
                for k, v in re.findall(r'^(\w+):\s*(.+?)\s*$', m.group(1), re.M)}
        for k in ('title', 'description', 'slug', 'date', 'author', 'category'):
            if k not in meta:
                raise SystemExit(f'{f.name}: front matter needs "{k}"')
        if meta['author'] not in AUTHORS:
            raise SystemExit(f'{f.name}: unknown author {meta["author"]}')
        body, toc = markdown(m.group(2))
        words = len(re.findall(r'\w+', re.sub(r'<[^>]+>', ' ', body)))
        meta.update(lang=lang, body=body, toc=toc, words=words, minutes=max(1, math.ceil(words / 200)),
                    date_obj=datetime.date.fromisoformat(meta['date']), order=int(meta.get('order', 99)))
        posts.append(meta)
    posts.sort(key=lambda p: (-p['date_obj'].toordinal(), p['order']))
    return posts


def load_all():
    """Both languages, with each post's translation path in p['alt'] (or None)."""
    tr, en = load_posts('tr'), load_posts('en')
    tr_slugs = {p['slug'] for p in tr}
    en_of = {}
    for p in en:
        if p.get('tr') and p['tr'] not in tr_slugs:
            raise SystemExit(f'en/{p["slug"]}: no Turkish post with slug {p["tr"]}')
        if p.get('tr'):
            en_of[p['tr']] = p['slug']
    for p in tr:
        p['alt'] = BLOG['en'] + en_of[p['slug']] + '/' if p['slug'] in en_of else None
    for p in en:
        p['alt'] = BLOG['tr'] + p['tr'] + '/' if p.get('tr') else None
    return {'tr': tr, 'en': en}


def path_of(p):
    return BLOG[p['lang']] + p['slug'] + '/'


def human_date(d, lang):
    m = MONTHS[lang][d.month - 1]
    return f'{d.day} {m} {d.year}' if lang == 'tr' else f'{m} {d.day}, {d.year}'


# ── Shared chrome (navigation and footer copied from the home page) ──

def chrome(page_html, base):
    """Header and footer of a home page, with every relative link made root-absolute against `base`."""
    header = page_html[page_html.index('<header>'): page_html.index('</header>') + len('</header>')]
    footer = page_html[page_html.index('<footer'): page_html.index('</footer>') + len('</footer>')]

    def absolute(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r'(https?:|mailto:|/|#content$)', url):
            return m.group(0)
        return f'{attr}="{urljoin(base, url)}"'

    def fix(part):
        part = part.replace(' data-nav-link', '').replace(' aria-current="true"', '')
        return re.sub(r'(href|src)="([^"]*)"', absolute, part)
    return fix(header), fix(footer)


def set_lang_links(header, lang, tr_href, en_href):
    header = re.sub(r'<a href="[^"]*" data-lang="tr"', f'<a href="{tr_href}" data-lang="tr"', header)
    header = re.sub(r'<a href="[^"]*" data-lang="en"', f'<a href="{en_href}" data-lang="en"', header)
    return re.sub(r'(<a href="[^"]*" data-lang="%s"[^>]*)>' % lang, r'\1 aria-current="true">', header, count=1)


def head(lang, title, desc, path, alternates, extra='', og_type='website'):
    t = T[lang]
    url = SITE + path
    alt = ''.join(f'  <link rel="alternate" hreflang="{l}" href="{SITE}{u}">\n' for l, u in alternates.items())
    if alternates:
        alt += f'  <link rel="alternate" hreflang="x-default" href="{SITE}{alternates.get("tr", path)}">\n'
    return f'''<!doctype html>
<!-- Generated by tools/build_blog.py from content/blog. Do not edit by hand. -->
<html lang="{t["html_lang"]}" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>
    (function () {{
      var t = null; try {{ t = localStorage.getItem('aule-theme'); }} catch (e) {{}}
      document.documentElement.setAttribute('data-theme', t === 'light' ? 'light' : 'dark');
    }})();
  </script>
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc, quote=True)}">
  <meta name="theme-color" content="#131209">
  <link rel="canonical" href="{url}">
{alt}  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="{t["locale"]}">
  <meta property="og:site_name" content="Aule Software">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(desc, quote=True)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/{t["og_image"]}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/{t["og_image"]}">
  <link rel="alternate" type="application/rss+xml" title="Aule Software Blog" href="{SITE}{BLOG[lang]}rss.xml">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/assets/favicon-192.png" sizes="192x192" type="image/png">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/aule.css">
{extra}</head>
<body>
<a class="au-skip button-sm" href="#content">{t["skip"]}</a>
'''


def tail(footer):
    return f'''{footer}
<script src="/assets/js/i18n.js" defer></script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''


def jsonld(data):
    return ('  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2).replace('</', '<\\/')
            + '\n  </script>\n')


def author_line(a, p):
    t = T[p['lang']]
    return (f'<span class="au-avatar au-avatar-sm" aria-hidden="true">{a["initials"]}</span>'
            f'<span><strong>{a["name"]}</strong><br><span class="au-muted">{human_date(p["date_obj"], p["lang"])} · {p["minutes"]} {t["read"]}</span></span>')


def card(p, href):
    a = AUTHORS[p['author']]
    return f'''      <article class="au-post-card">
        <p class="caption-4 au-post-cat">{html.escape(p["category"])}</p>
        <h3 class="title-1"><a href="{href}">{html.escape(p["title"])}</a></h3>
        <p class="body-6 au-muted">{html.escape(p["description"])}</p>
        <p class="au-post-meta caption-5">{a["name"]} · {human_date(p["date_obj"], p["lang"])} · {p["minutes"]} {T[p["lang"]]["mins"]}</p>
      </article>
'''


# ── Pages ─────────────────────────────────────────────────────────

def write(path, text):
    out = ROOT / path.strip('/') / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8', newline='\n')


def build_post(p, posts, page_html):
    lang, t = p['lang'], T[p['lang']]
    path, url = path_of(p), SITE + path_of(p)
    a = AUTHORS[p['author']]
    other = 'en' if lang == 'tr' else 'tr'
    header, footer = chrome(page_html, HOME[lang])
    links = {lang: path, other: p['alt'] or BLOG[other]}
    header = set_lang_links(header, lang, links['tr'], links['en'])
    alternates = {lang: path, other: p['alt']} if p['alt'] else {}
    org = {'@id': SITE + '/#organization'}
    data = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BlogPosting', '@id': url + '#article', 'headline': p['title'], 'description': p['description'],
         'datePublished': p['date'], 'dateModified': p.get('updated', p['date']), 'inLanguage': lang,
         'mainEntityOfPage': url, 'url': url, 'image': f'{SITE}/assets/{t["og_image"]}', 'wordCount': p['words'],
         'articleSection': p['category'],
         'author': {'@type': 'Person', 'name': a['name'], 'jobTitle': t['role'], 'email': a['email'], 'worksFor': org},
         'publisher': org, 'isPartOf': {'@id': SITE + BLOG[lang] + '#blog'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': t['home'], 'item': SITE + HOME[lang]},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': SITE + BLOG[lang]},
            {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': url}]},
    ]}
    if p['alt']:
        data['@graph'][0]['workTranslation' if lang == 'tr' else 'translationOfWork'] = {'@id': SITE + p['alt'] + '#article'}
    toc = ''.join(f'<li><a href="#{anc}">{html.escape(x)}</a></li>' for anc, x in p['toc'])
    others = [q for q in posts if q['slug'] != p['slug']][:2]
    related = ''.join(card(q, f'../{q["slug"]}/') for q in others)
    page = head(lang, f'{p["title"]} | Aule Software Blog', p['description'], path, alternates, jsonld(data), 'article') + header + f'''
<main id="content">
  <article class="au-article">
    <header class="au-container au-article-head">
      <nav class="au-crumbs caption-4" aria-label="{t["crumbs"]}"><a href="{HOME[lang]}">{t["home"]}</a><span aria-hidden="true">/</span><a href="../">Blog</a></nav>
      <p class="au-eyebrow caption-4">{html.escape(p["category"])}</p>
      <h1 class="heading-2 au-article-title">{html.escape(p["title"])}</h1>
      <p class="body-3 au-muted au-article-lead">{html.escape(p["description"])}</p>
      <div class="au-article-meta caption-2">{author_line(a, p)}</div>
    </header>
    <div class="au-container au-article-layout">
      <nav class="au-toc" aria-label="{t["toc"]}">
        <p class="caption-3">{t["toc"]}</p>
        <ol class="body-6">{toc}</ol>
      </nav>
      <div class="au-prose body-7">
{p["body"]}
      </div>
    </div>
    <div class="au-container au-article-foot">
      <aside class="au-author-box" aria-label="{t["author"]}">
        <span class="au-avatar" aria-hidden="true">{a["initials"]}</span>
        <div>
          <p class="title-2">{a["name"]}</p>
          <p class="caption-4 au-founder-role">{t["role"]}, Aule Software</p>
          <p class="body-6 au-muted">{html.escape(a["bio"][lang])}</p>
          <a class="au-founder-mail caption-2" href="mailto:{a["email"]}">{a["email"]}</a>
        </div>
      </aside>
      <div class="au-band au-post-cta">
        <div>
          <p class="au-eyebrow caption-4">{t["cta_eyebrow"]}</p>
          <p class="heading-5">{t["cta_title"]}</p>
          <p class="body-6">{t["cta_text"]}</p>
        </div>
        <a class="au-btn au-btn-primary" href="{HOME[lang]}#contact"><span class="au-btn-label">{t["cta_btn"]}</span>{ARROW}</a>
      </div>
    </div>
  </article>
  <section class="au-section au-related" aria-labelledby="related-title">
    <div class="au-container">
      <h2 class="heading-5" id="related-title">{t["related"]}</h2>
      <div class="au-post-grid">
{related}      </div>
    </div>
  </section>
</main>
''' + tail(footer)
    write(path, page)


def build_index(lang, posts, page_html):
    t, path = T[lang], BLOG[lang]
    url = SITE + path
    header, footer = chrome(page_html, HOME[lang])
    header = set_lang_links(header, lang, BLOG['tr'], BLOG['en'])
    header = header.replace(f'href="{path}" data-i18n="nav.blog">', f'href="{path}" data-i18n="nav.blog" aria-current="page">')
    data = {'@context': 'https://schema.org', '@type': 'Blog', '@id': url + '#blog', 'url': url, 'name': 'Aule Software Blog',
            'description': t['index_desc'], 'inLanguage': lang, 'publisher': {'@id': SITE + '/#organization'},
            'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': SITE + path_of(p),
                          'datePublished': p['date'], 'author': {'@type': 'Person', 'name': AUTHORS[p['author']]['name']}} for p in posts]}
    cards = ''.join(card(p, f'{p["slug"]}/') for p in posts)
    page = head(lang, t['index_title'], t['index_desc'], path, {'tr': BLOG['tr'], 'en': BLOG['en']}, jsonld(data)) + header + f'''
<main id="content">
  <section class="au-section au-blog-head">
    <div class="au-container">
      <div class="au-section-head au-measure">
        <p class="au-eyebrow caption-4">Blog</p>
        <h1 class="heading-2">{t["index_h1"]}</h1>
        <p class="body-3 au-muted">{t["index_desc"]}</p>
      </div>
      <div class="au-post-grid">
{cards}      </div>
    </div>
  </section>
</main>
''' + tail(footer)
    write(path, page)


def build_rss(lang, posts):
    items = ''.join(f'''    <item>
      <title>{html.escape(p["title"])}</title>
      <link>{SITE}{path_of(p)}</link>
      <guid>{SITE}{path_of(p)}</guid>
      <pubDate>{datetime.datetime.combine(p["date_obj"], datetime.time(9, 0)).strftime("%a, %d %b %Y %H:%M:%S +0300")}</pubDate>
      <description>{html.escape(p["description"])}</description>
    </item>
''' for p in posts)
    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Aule Software Blog</title>
    <link>{SITE}{BLOG[lang]}</link>
    <description>{T[lang]["rss_desc"]}</description>
    <language>{lang}</language>
{items}  </channel>
</rss>
'''
    out = ROOT / BLOG[lang].strip('/') / 'rss.xml'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rss, encoding='utf-8', newline='\n')


def teaser_block(lang, posts):
    """The 'latest articles' section for a home page; links are relative to that home page."""
    t = T[lang]
    cards = ''.join(card(p, f'blog/{p["slug"]}/') for p in posts[:3])
    return f'''  <!--blog:start-->
  <!-- Blog -->
  <section class="au-section" id="blog" aria-labelledby="blog-title">
    <div class="au-container">
      <div class="au-section-head au-measure au-reveal">
        <p class="au-eyebrow caption-4">Blog</p>
        <h2 class="heading-2" id="blog-title" data-split>{t["teaser_title"]}</h2>
        <p class="body-3 au-muted">{t["teaser_desc"]}</p>
      </div>
      <div class="au-post-grid au-reveal au-stagger">
{cards}      </div>
      <p class="au-blog-more au-reveal"><a class="au-btn au-btn-secondary" href="blog/"><span class="au-btn-label">{t["all_posts"]}</span>{ARROW}</a></p>
    </div>
  </section>
  <!--blog:end-->
'''


def put_teaser(page_html, block):
    return re.sub(r'  <!--blog:start-->.*?<!--blog:end-->\n', lambda m: block, page_html, count=1, flags=re.S)


def build_pages(lang, page_html, everything=None):
    """Posts, index and RSS for one language; page_html is that language's home page (for the header and footer)."""
    posts = (everything or load_all())[lang]
    for p in posts:
        build_post(p, posts, page_html)
    build_index(lang, posts, page_html)
    build_rss(lang, posts)
    return posts


def build_sitemap(everything):
    tr, en = everything['tr'], everything['en']
    dates = [p['date_obj'] for p in tr + en]
    today = max(dates).isoformat() if dates else datetime.date.today().isoformat()

    def entry(path, lastmod, alts):
        x = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{u}"/>' for l, u in alts.items())
        if alts:
            x += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{alts.get("tr", path)}"/>'
        return f'  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{lastmod}</lastmod>{x}\n  </url>\n'

    pair = {'tr': '/', 'en': '/en/'}
    urls = entry('/', today, pair) + entry('/en/', today, pair)
    bpair = {'tr': BLOG['tr'], 'en': BLOG['en']}
    urls += entry(BLOG['tr'], today, bpair) + entry(BLOG['en'], today, bpair) if en else entry(BLOG['tr'], today, {})
    spair = {'tr': '/hizmetler/', 'en': '/en/services/'}
    urls += entry(spair['tr'], today, spair) + entry(spair['en'], today, spair)
    for p in tr + en:
        alts = {p['lang']: path_of(p), ('en' if p['lang'] == 'tr' else 'tr'): p['alt']} if p['alt'] else {}
        urls += entry(path_of(p), p.get('updated', p['date']), alts)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')
    (ROOT / 'sitemap.xml').write_text(xml, encoding='utf-8', newline='\n')


def main():
    """Turkish blog, the Turkish home page block and the sitemap. build_en.py then builds the English side."""
    everything = load_all()
    src = ROOT / 'index.html'
    index_html = put_teaser(src.read_text(encoding='utf-8'), teaser_block('tr', everything['tr']))
    src.write_text(index_html, encoding='utf-8', newline='\n')
    build_pages('tr', index_html, everything)
    build_sitemap(everything)
    for lang in ('tr', 'en'):
        print(f'blog ({lang}): {len(everything[lang])} posts, ' + ', '.join(f'{p["slug"]} ({p["words"]} words)' for p in everything[lang]))
    return everything


if __name__ == '__main__':
    main()
