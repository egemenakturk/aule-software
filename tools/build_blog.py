"""Build the blog from Markdown.

    python tools/build_en.py        (runs this first, then builds the English page)

Posts live in content/blog/*.md with a front matter block:

    ---
    title: Hazır yazılım mı, kuruma özel yazılım mı? Karar rehberi
    description: One or two sentences for search results and the post header.
    slug: hazir-yazilim-mi-kuruma-ozel-yazilim-mi
    date: 2026-11-09
    author: egemen            (a key of AUTHORS below)
    category: Karar rehberi
    order: 1                  (optional; lower comes first on the same date)
    ---

Supported Markdown: ## and ### headings, paragraphs, - and 1. lists, > callouts, pipe tables,
**bold**, `code` and [links](url). This script writes:
  blog/index.html, blog/<slug>/index.html, the "Son yazılar" block in index.html (between
  <!--blog:start--> and <!--blog:end-->) and sitemap.xml.
"""
import datetime
import html
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / 'content' / 'blog'
SITE = 'https://www.aulesoftware.com'

AUTHORS = {
    'egemen': {'name': 'Egemen Doğuş Aktürk', 'initials': 'EA', 'role': 'Kurucu Ortak',
               'email': 'egemen.akturk@aulesoftware.com',
               'bio': 'Bankacılık ve havacılık sektörlerinde 7 yılı aşkın deneyim. ISO standartlarına uygun uluslararası SWIFT para transferi ürününde ve IATA standartlarına uygun havayolu rezervasyon sistemlerinde görev aldı.'},
    'mert': {'name': 'Mert Kelkit', 'initials': 'MK', 'role': 'Kurucu Ortak',
             'email': 'mert.kelkit@aulesoftware.com',
             'bio': 'Bankacılık sektöründe 7 yılı aşkın deneyim. ISO standartlarına uygun uluslararası SWIFT para transferi ürününde ve 10\'dan fazla bankada kullanılan TCMB FAST ve KOLAS ürünlerinde görev aldı.'},
}
MONTHS = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
ARROW = '<svg class="au-icon" viewBox="0 0 256 256" aria-hidden="true"><line x1="40" y1="128" x2="216" y2="128"/><polyline points="144 56 216 128 144 200"/></svg>'
CLOCK = '<svg class="au-icon" viewBox="0 0 256 256" aria-hidden="true"><circle cx="128" cy="128" r="96"/><polyline points="128 72 128 128 184 128"/></svg>'


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

def load_posts():
    posts = []
    for f in sorted(POSTS.glob('*.md')):
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
        meta.update(body=body, toc=toc, words=words, minutes=max(1, math.ceil(words / 200)),
                    date_obj=datetime.date.fromisoformat(meta['date']), order=int(meta.get('order', 99)))
        posts.append(meta)
    posts.sort(key=lambda p: (-p['date_obj'].toordinal(), p['order']))
    return posts


def human_date(d):
    return f'{d.day} {MONTHS[d.month - 1]} {d.year}'


# ── Shared chrome (navigation and footer copied from index.html) ──

def chrome(index_html, up):
    header = index_html[index_html.index('<header>'): index_html.index('</header>') + len('</header>')]
    footer = index_html[index_html.index('<footer'): index_html.index('</footer>') + len('</footer>')]

    def fix(part):
        part = part.replace(' data-nav-link', '')
        part = re.sub(r'href="#(?!content")', f'href="{up}#', part)
        part = part.replace('href="./" data-lang="tr"', f'href="{up}" data-lang="tr"')
        part = re.sub(r'href="(blog/|en/|gizlilik/|kosullar/)', lambda m: f'href="{up}{m.group(1)}', part)
        part = part.replace(' aria-current="true">TR', '>TR')
        return part
    return fix(header), fix(footer)


def head(title, desc, canonical, up, extra=''):
    return f'''<!doctype html>
<!-- Generated by tools/build_blog.py from content/blog. Do not edit by hand. -->
<html lang="tr" class="no-js">
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
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="{'article' if '/blog/' in canonical and canonical.rstrip('/') != SITE + '/blog' else 'website'}">
  <meta property="og:locale" content="tr_TR">
  <meta property="og:site_name" content="Aule Software">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(desc, quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{SITE}/assets/og-image.png">
  <link rel="alternate" type="application/rss+xml" title="Aule Software Blog" href="{SITE}/blog/rss.xml">
  <link rel="icon" href="{up}favicon.ico" sizes="48x48">
  <link rel="icon" href="{up}assets/favicon-192.png" sizes="192x192" type="image/png">
  <link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="{up}assets/apple-touch-icon.png">
  <link rel="preload" href="{up}assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{up}assets/css/tokens.css">
  <link rel="stylesheet" href="{up}assets/css/aule.css">
{extra}</head>
<body>
<a class="au-skip button-sm" href="#content">İçeriğe geç</a>
'''


def tail(footer, up):
    return f'''{footer}
<script src="{up}assets/js/i18n.js" defer></script>
<script src="{up}assets/js/main.js" defer></script>
</body>
</html>
'''


def jsonld(data):
    return ('  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2).replace('</', '<\\/')
            + '\n  </script>\n')


def author_line(a, p):
    return (f'<span class="au-avatar au-avatar-sm" aria-hidden="true">{a["initials"]}</span>'
            f'<span><strong>{a["name"]}</strong><br><span class="au-muted">{human_date(p["date_obj"])} · {p["minutes"]} dk okuma</span></span>')


def card(p, href):
    a = AUTHORS[p['author']]
    return f'''      <article class="au-post-card">
        <p class="caption-4 au-post-cat">{html.escape(p["category"])}</p>
        <h3 class="title-1"><a href="{href}">{html.escape(p["title"])}</a></h3>
        <p class="body-6 au-muted">{html.escape(p["description"])}</p>
        <p class="au-post-meta caption-5">{a["name"]} · {human_date(p["date_obj"])} · {p["minutes"]} dk</p>
      </article>
'''


# ── Pages ─────────────────────────────────────────────────────────

def build_post(p, posts, index_html):
    up = '../../'
    url = f'{SITE}/blog/{p["slug"]}/'
    a = AUTHORS[p['author']]
    header, footer = chrome(index_html, up)
    org = {'@id': SITE + '/#organization'}
    data = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BlogPosting', '@id': url + '#article', 'headline': p['title'], 'description': p['description'],
         'datePublished': p['date'], 'dateModified': p.get('updated', p['date']), 'inLanguage': 'tr',
         'mainEntityOfPage': url, 'url': url, 'image': SITE + '/assets/og-image.png', 'wordCount': p['words'],
         'articleSection': p['category'],
         'author': {'@type': 'Person', 'name': a['name'], 'jobTitle': a['role'], 'email': a['email'], 'worksFor': org},
         'publisher': org, 'isPartOf': {'@id': SITE + '/blog/#blog'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Ana sayfa', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': SITE + '/blog/'},
            {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': url}]},
    ]}
    toc = ''.join(f'<li><a href="#{anc}">{html.escape(t)}</a></li>' for anc, t in p['toc'])
    others = [q for q in posts if q['slug'] != p['slug']][:2]
    related = ''.join(card(q, f'../{q["slug"]}/') for q in others)
    page = head(f'{p["title"]} | Aule Software Blog', p['description'], url, up, jsonld(data)) + header + f'''
<main id="content">
  <article class="au-article">
    <header class="au-container au-article-head">
      <nav class="au-crumbs caption-4" aria-label="İçerik yolu"><a href="{up}">Ana sayfa</a><span aria-hidden="true">/</span><a href="../">Blog</a></nav>
      <p class="au-eyebrow caption-4">{html.escape(p["category"])}</p>
      <h1 class="heading-2 au-article-title">{html.escape(p["title"])}</h1>
      <p class="body-3 au-muted au-article-lead">{html.escape(p["description"])}</p>
      <div class="au-article-meta caption-2">{author_line(a, p)}</div>
    </header>
    <div class="au-container au-article-layout">
      <nav class="au-toc" aria-label="İçindekiler">
        <p class="caption-3">İçindekiler</p>
        <ol class="body-6">{toc}</ol>
      </nav>
      <div class="au-prose body-7">
{p["body"]}
      </div>
    </div>
    <div class="au-container au-article-foot">
      <aside class="au-author-box" aria-label="Yazar">
        <span class="au-avatar" aria-hidden="true">{a["initials"]}</span>
        <div>
          <p class="title-2">{a["name"]}</p>
          <p class="caption-4 au-founder-role">{a["role"]}, Aule Software</p>
          <p class="body-6 au-muted">{html.escape(a["bio"])}</p>
          <a class="au-founder-mail caption-2" href="mailto:{a["email"]}">{a["email"]}</a>
        </div>
      </aside>
      <div class="au-band au-post-cta">
        <div>
          <p class="au-eyebrow caption-4">Ön görüşme</p>
          <p class="heading-5">Bu yazıdaki konuları kurumunuz için konuşalım.</p>
          <p class="body-6">Kısa bir ön görüşmede hedeflerinizi ve öncelikli süreçlerinizi birlikte değerlendirelim.</p>
        </div>
        <a class="au-btn au-btn-primary" href="{up}#contact"><span class="au-btn-label">Ön görüşme planlayın</span>{ARROW}</a>
      </div>
    </div>
  </article>
  <section class="au-section au-related" aria-labelledby="related-title">
    <div class="au-container">
      <h2 class="heading-5" id="related-title">Diğer yazılar</h2>
      <div class="au-post-grid">
{related}      </div>
    </div>
  </section>
</main>
''' + tail(footer, up)
    out = ROOT / 'blog' / p['slug'] / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding='utf-8', newline='\n')


def build_index(posts, index_html):
    up = '../'
    url = SITE + '/blog/'
    header, footer = chrome(index_html, up)
    header = header.replace('href="../blog/" data-i18n="nav.blog">Blog', 'href="./" data-i18n="nav.blog" aria-current="page">Blog')
    title = 'Blog | Aule Software'
    desc = 'Kuruma özel yazılım, iş süreçleri analizi ve dijital dönüşüm üzerine Aule Software kurucularının yazıları.'
    data = {'@context': 'https://schema.org', '@type': 'Blog', '@id': url + '#blog', 'url': url, 'name': 'Aule Software Blog',
            'description': desc, 'inLanguage': 'tr', 'publisher': {'@id': SITE + '/#organization'},
            'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': f'{SITE}/blog/{p["slug"]}/',
                          'datePublished': p['date'], 'author': {'@type': 'Person', 'name': AUTHORS[p['author']]['name']}} for p in posts]}
    cards = ''.join(card(p, f'{p["slug"]}/') for p in posts)
    page = head(title, desc, url, up, jsonld(data)) + header + f'''
<main id="content">
  <section class="au-section au-blog-head">
    <div class="au-container">
      <div class="au-section-head au-measure">
        <p class="au-eyebrow caption-4">Blog</p>
        <h1 class="heading-2">Kuruma özel yazılım ve<br> dijital dönüşüm üzerine.</h1>
        <p class="body-3 au-muted">{desc}</p>
      </div>
      <div class="au-post-grid">
{cards}      </div>
    </div>
  </section>
</main>
''' + tail(footer, up)
    (ROOT / 'blog').mkdir(exist_ok=True)
    (ROOT / 'blog' / 'index.html').write_text(page, encoding='utf-8', newline='\n')


def build_rss(posts):
    items = ''.join(f'''    <item>
      <title>{html.escape(p["title"])}</title>
      <link>{SITE}/blog/{p["slug"]}/</link>
      <guid>{SITE}/blog/{p["slug"]}/</guid>
      <pubDate>{datetime.datetime.combine(p["date_obj"], datetime.time(9, 0)).strftime("%a, %d %b %Y %H:%M:%S +0300")}</pubDate>
      <description>{html.escape(p["description"])}</description>
    </item>
''' for p in posts)
    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Aule Software Blog</title>
    <link>{SITE}/blog/</link>
    <description>Kuruma özel yazılım, iş süreçleri analizi ve dijital dönüşüm üzerine yazılar.</description>
    <language>tr</language>
{items}  </channel>
</rss>
'''
    (ROOT / 'blog' / 'rss.xml').write_text(rss, encoding='utf-8', newline='\n')


def build_teaser(posts, index_html):
    cards = ''.join(card(p, f'blog/{p["slug"]}/') for p in posts[:3])
    block = f'''  <!--blog:start-->
  <!-- Blog -->
  <section class="au-section" id="blog" aria-labelledby="blog-title">
    <div class="au-container">
      <div class="au-section-head au-measure au-reveal">
        <p class="au-eyebrow caption-4">Blog</p>
        <h2 class="heading-2" id="blog-title" data-split>Son yazılar</h2>
        <p class="body-3 au-muted">Kuruma özel yazılım, süreç analizi ve dijital dönüşüm üzerine kurucularımızın yazıları.</p>
      </div>
      <div class="au-post-grid au-reveal au-stagger">
{cards}      </div>
      <p class="au-blog-more au-reveal"><a class="au-btn au-btn-secondary" href="blog/"><span class="au-btn-label">Tüm yazılar</span>{ARROW}</a></p>
    </div>
  </section>
  <!--blog:end-->
'''
    return re.sub(r'  <!--blog:start-->.*?<!--blog:end-->\n', lambda m: block, index_html, count=1, flags=re.S)


def build_sitemap(posts):
    home = ['', 'en/']
    alt = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}/{h}"/>' for l, h in [('tr', ''), ('en', 'en/'), ('x-default', '')])
    today = max(p['date_obj'] for p in posts).isoformat() if posts else datetime.date.today().isoformat()
    urls = ''.join(f'  <url>\n    <loc>{SITE}/{h}</loc>\n    <lastmod>{today}</lastmod>{alt}\n  </url>\n' for h in home)
    urls += f'  <url>\n    <loc>{SITE}/blog/</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n'
    urls += ''.join(f'  <url>\n    <loc>{SITE}/blog/{p["slug"]}/</loc>\n    <lastmod>{p.get("updated", p["date"])}</lastmod>\n  </url>\n' for p in posts)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')
    (ROOT / 'sitemap.xml').write_text(xml, encoding='utf-8', newline='\n')


def main():
    posts = load_posts()
    src = ROOT / 'index.html'
    index_html = build_teaser(posts, src.read_text(encoding='utf-8'))
    src.write_text(index_html, encoding='utf-8', newline='\n')
    for p in posts:
        build_post(p, posts, index_html)
    build_index(posts, index_html)
    build_rss(posts)
    build_sitemap(posts)
    print(f'blog: {len(posts)} posts, ' + ', '.join(f'{p["slug"]} ({p["words"]} words)' for p in posts))


if __name__ == '__main__':
    main()
