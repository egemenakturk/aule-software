"""Build the Services page in both languages from content/services.json.

    python tools/build_en.py        (calls main(tr_home_html, en_home_html) after the home pages are built)

Writes hizmetler/index.html and en/services/index.html. The header, footer and the commitments band are
taken from each language's home page, so they stay identical to it.
"""
import html
import json
import re
from pathlib import Path

import build_blog as B

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'content' / 'services.json'
PATHS = {'tr': '/hizmetler/', 'en': '/en/services/'}
CHECK = '<svg class="au-icon" viewBox="0 0 256 256" aria-hidden="true"><polyline points="40 144 96 200 224 72"/></svg>'


def esc(s):
    return html.escape(s, quote=False)


def section(page_html, sid):
    m = re.search(r'  <section[^>]*id="%s".*?</section>\n' % sid, page_html, re.S)
    if not m:
        raise SystemExit(f'services: no section #{sid} in the home page')
    return m.group(0)


def build(lang, c, home_html):
    path, url = PATHS[lang], B.SITE + PATHS[lang]
    home = B.HOME[lang]
    t = B.T[lang]
    header, footer = B.chrome(home_html, home)
    header = B.set_lang_links(header, lang, PATHS['tr'], PATHS['en'])
    header = header.replace(f'href="{path}" data-i18n="nav.services">', f'href="{path}" data-i18n="nav.services" aria-current="page">')
    # the commitments band, exactly as on the home page, with its links made absolute
    band = section(home_html, 'commitments')
    band = re.sub(r'href="(?!https?:|mailto:|/|#)([^"]*)"', lambda m: f'href="{home}{m.group(1)}"', band)

    org = {'@id': B.SITE + '/#organization'}
    data = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': c['title'], 'description': c['description'],
         'inLanguage': lang, 'isPartOf': {'@id': B.SITE + '/#website'}, 'about': org},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': t['home'], 'item': B.SITE + home},
            {'@type': 'ListItem', 'position': 2, 'name': c['eyebrow'], 'item': url}]},
        {'@type': 'ItemList', 'name': c['eyebrow'], 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'item': {
                '@type': 'Service', 'name': s['t'], 'description': s['d'], 'url': f'{url}#{s["id"]}',
                'provider': org, 'areaServed': ['TR', 'Worldwide'], 'serviceOutput': s['out']}}
            for i, s in enumerate(c['steps'])]},
    ]}

    index = ''.join(f'<li><a href="#{s["id"]}"><span class="code">{s["n"]}</span><span class="title-4">{esc(s["t"])}</span></a></li>'
                    for s in c['steps'])
    steps = ''
    for s in c['steps']:
        items = ''.join(f'<li>{CHECK}<span>{esc(x)}</span></li>' for x in s['items'])
        steps += f'''  <section class="au-section au-svc" id="{s["id"]}" aria-labelledby="{s["id"]}-title">
    <div class="au-container au-svc-grid">
      <div class="au-svc-intro au-reveal">
        <p class="code au-svc-num">{s["n"]}</p>
        <h2 class="heading-2" id="{s["id"]}-title">{esc(s["t"])}</h2>
        <p class="body-2 au-muted">{esc(s["d"])}</p>
      </div>
      <div class="au-svc-detail au-reveal">
        <div class="au-svc-card">
          <h3 class="title-3 au-svc-label">{c["what"]}</h3>
          <ul class="au-svc-list body-3">{items}</ul>
        </div>
        <div class="au-svc-out">
          <p class="caption-4 au-svc-label">{c["deliverable"]}</p>
          <p class="title-2">{esc(s["out"])}</p>
        </div>
      </div>
    </div>
  </section>
'''
    page = B.head(lang, c['title'], c['description'], path, {'tr': PATHS['tr'], 'en': PATHS['en']}, B.jsonld(data)) + header + f'''
<main id="content">
  <section class="au-section au-blog-head au-svc-hero">
    <div class="au-container">
      <nav class="au-crumbs caption-4" aria-label="{t["crumbs"]}"><a href="{home}">{t["home"]}</a><span aria-hidden="true">/</span><span>{esc(c["eyebrow"])}</span></nav>
      <div class="au-section-head au-measure">
        <p class="au-eyebrow caption-4">{esc(c["eyebrow"])}</p>
        <h1 class="heading-2">{esc(c["h1"])}</h1>
        <p class="body-3 au-muted">{esc(c["lead"])}</p>
      </div>
      <nav class="au-svc-index" aria-label="{c["nav_label"]}"><ol>{index}</ol></nav>
    </div>
  </section>
{steps}{band}  <section class="au-section">
    <div class="au-container">
      <div class="au-band au-post-cta">
        <div>
          <p class="au-eyebrow caption-4">{c["cta_eyebrow"]}</p>
          <p class="heading-5">{esc(c["cta_title"])}</p>
          <p class="body-6">{esc(c["cta_text"])}</p>
        </div>
        <div class="au-svc-cta-actions">
          <a class="au-btn au-btn-primary" href="{home}#contact"><span class="au-btn-label">{c["cta_btn"]}</span>{B.ARROW}</a>
          <a class="au-svc-cases caption-2" href="{home}#cases">{c["cases_link"]}</a>
        </div>
      </div>
    </div>
  </section>
</main>
''' + B.tail(footer)
    B.write(path, page)


def main(tr_home_html, en_home_html):
    content = json.loads(DATA.read_text(encoding='utf-8'))
    build('tr', content['tr'], tr_home_html)
    build('en', content['en'], en_home_html)
    print('services pages written: ' + ', '.join(PATHS.values()))
