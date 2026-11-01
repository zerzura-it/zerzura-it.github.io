#!/usr/bin/env python3
"""Converte l'export Takeout di Blogger (feed.atom) in contenuti Hugo.

Uso: python3 -I converti.py <cartella blog Takeout> <cartella album Takeout> <progetto Hugo>
"""
import sys, os, re, json, shutil, subprocess, unicodedata, hashlib
import xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import unquote, unquote_plus, urlparse, parse_qs
from PIL import Image
from bs4 import BeautifulSoup, NavigableString, Tag

BLOG, ALBUM, OUT = sys.argv[1:4]
NS = {'a': 'http://www.w3.org/2005/Atom', 'b': 'http://schemas.google.com/blogger/2018'}
DOMINI_INTERNI = ('www.zerzura.it', 'zerzura.it', 'versozerzura.blogspot.com')

# ---------- album immagini ----------
def norm(name):
    name = re.sub(r'#U([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), name)
    return unicodedata.normalize('NFC', name)

album = {}
# prima l'album del blog, poi gli altri album dello stesso account (alcune immagini stanno lì)
cartelle = [ALBUM] + sorted(os.path.join(os.path.dirname(ALBUM), d) for d in os.listdir(os.path.dirname(ALBUM))
                            if os.path.join(os.path.dirname(ALBUM), d) != ALBUM)
for d in cartelle:
    for f in sorted(os.listdir(d)):
        if f.endswith('.json'):
            continue
        album.setdefault(norm(f), os.path.join(d, f))
for d in cartelle:
    for f in sorted(os.listdir(d)):
        if not f.endswith('.json'):  # "x(1).jpg" -> "x.jpg" come ripiego
            album.setdefault(norm(re.sub(r'\(\d+\)(?=\.[^.]+$|$)', '', f)), os.path.join(d, f))

IMG_DIR = os.path.join(OUT, 'static', 'images')
os.makedirs(IMG_DIR, exist_ok=True)
rapporto = {'locali': {}, 'remote': {}}

def slug_file(name):
    base, ext = os.path.splitext(name)
    base = unicodedata.normalize('NFKD', base).encode('ascii', 'ignore').decode()
    base = re.sub(r'[^A-Za-z0-9._-]+', '-', base).strip('-') or 'immagine'
    return base + ext.lower()

def is_blogger_img(u):
    h = urlparse(u).netloc
    return h.endswith('googleusercontent.com') or h.endswith('bp.blogspot.com')

def risolvi_immagine(url, post):
    """Ritorna il percorso locale /images/... se l'immagine è nell'album, altrimenti None."""
    name = urlparse(url).path.rsplit('/', 1)[-1]
    while unquote_plus(name) != name:  # alcuni URL sono codificati due volte
        name = unquote_plus(name)
    name = norm(name)
    src = album.get(name)
    if not src:
        rapporto['remote'].setdefault(url, post)
        return None
    dest = slug_file(name)
    with Image.open(src) as im:
        fmt = (im.format or 'JPEG').upper()
        if not os.path.splitext(dest)[1]:  # es. "[UNSET]": nome dal post, estensione dal formato
            dest = slug_file(os.path.basename(post).removesuffix('.html')) + '.' + {'JPEG': 'jpg'}.get(fmt, fmt.lower())
        if max(im.size) > 1600:  # alleggerisce le foto troppo grandi per il web
            im.thumbnail((1600, 1600))
            im.save(os.path.join(IMG_DIR, dest), fmt, **({'quality': 85} if fmt in ('JPEG', 'WEBP') else {'optimize': True}))
        else:
            shutil.copyfile(src, os.path.join(IMG_DIR, dest))
    rapporto['locali'][name] = dest
    return '/images/' + dest

def immagine_grande(img):
    """Preferisce l'URL dell'immagine a piena risoluzione (il link che la circonda)."""
    a = img.find_parent('a')
    if a and a.get('href') and is_blogger_img(a['href']):
        return a['href']
    return img.get('src', '')

# ---------- pulizia HTML ----------
def allineata_destra(el):
    return isinstance(el, Tag) and 'text-align: right' in (el.get('style') or '')

def testo_vuoto(el):
    if isinstance(el, NavigableString):
        return not str(el).replace('\xa0', ' ').strip()
    return not el.get_text().replace('\xa0', ' ').strip() and not el.find(['img', 'iframe'])

def converti_html(html, post, segnaposto):
    soup = BeautifulSoup(html, 'html.parser')

    def token(html_frammento):
        k = 'ZZBLOCCO%dZZ' % len(segnaposto)
        segnaposto[k] = html_frammento
        return k

    # video YouTube -> shortcode
    for fr in soup.find_all('iframe'):
        src = fr.get('src', '')
        m = re.search(r'youtube(?:-nocookie)?\.com/embed/([\w-]+)', src)
        rep = '{{< youtube %s >}}' % m.group(1) if m else str(fr)
        blocco = fr
        if fr.parent and fr.parent.name == 'div' and len([c for c in fr.parent.contents if not testo_vuoto(c)]) == 1:
            blocco = fr.parent
        p = soup.new_tag('p'); p.string = token(rep); blocco.replace_with(p)

    # tabelle-didascalia di Blogger e immagini singole -> <figure>
    def figura(img, didascalia_html):
        url = immagine_grande(img)
        loc = risolvi_immagine(url, post) if is_blogger_img(url) else None
        src = loc or url
        alt = (img.get('alt') or img.get('title') or '').replace('"', '&quot;')
        cap = f'<figcaption>{didascalia_html}</figcaption>' if didascalia_html else ''
        return f'<figure><a href="{src}"><img src="{src}" alt="{alt}" loading="lazy"></a>{cap}</figure>'

    for t in soup.find_all('table', class_='tr-caption-container'):
        img = t.find('img')
        cap = t.find(class_='tr-caption')
        cap_html = ''
        if cap:
            for x in cap.find_all(True):
                for att in ('style', 'rel', 'target', 'class'):
                    x.attrs.pop(att, None)
            for x in cap.find_all('span'):
                x.unwrap()
            cap_html = cap.decode_contents().strip()
            cap_html = re.sub(r'(<br\s*/?>|\s|&nbsp;|\xa0)+$', '', cap_html)
        p = soup.new_tag('p'); p.string = token(figura(img, cap_html) if img else str(t))
        t.replace_with(p)

    for img in soup.find_all('img'):
        if not img.parent:
            continue
        blocco = img.find_parent('a') or img
        sep = blocco.find_parent('div', class_='separator')
        if sep is not None and len(sep.find_all('img')) == 1:
            blocco = sep
        p = soup.new_tag('p'); p.string = token(figura(img, ''))
        blocco.replace_with(p)

    # blocchi allineati a destra (epigrafi): righe consecutive -> un paragrafo con classe
    for el in list(soup.find_all(['div', 'p'])):
        if el.parent is None or not allineata_destra(el) or testo_vuoto(el):
            continue
        prev = el.find_previous_sibling()
        if prev is not None and prev.get('data-destra'):
            continue  # già unito
        gruppo = [el]
        nxt = el.find_next_sibling()
        while nxt is not None and allineata_destra(nxt) and not testo_vuoto(nxt):
            gruppo.append(nxt); nxt = nxt.find_next_sibling()
        p = soup.new_tag('p'); p['data-destra'] = '1'
        for i, g in enumerate(gruppo):
            if i:
                p.append(soup.new_tag('br'))
            for c in list(g.contents):
                p.append(c.extract())
            if g is not el:
                g.decompose()
        # togli <br> finali
        while p.contents and isinstance(p.contents[-1], Tag) and p.contents[-1].name == 'br':
            p.contents[-1].decompose()
        el.replace_with(p)
        marca = soup.new_tag('p'); marca.string = 'ZZDESTRAZZ'
        p.insert_after(marca)

    # Blogger scrive spesso una riga per <div>: righe consecutive -> un paragrafo con a capo,
    # i <div> vuoti separano i paragrafi
    BLOCCHI = ['p', 'div', 'table', 'blockquote', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'hr']
    def riga(el):
        return isinstance(el, Tag) and el.name == 'div' and not el.find(BLOCCHI)
    def unisci(contenitore):
        figli = list(contenitore.children)
        gruppo = []
        def chiudi():
            pieni = [g for g in gruppo if not testo_vuoto(g)]
            if pieni:
                p = soup.new_tag('p')
                for i, g in enumerate(pieni):
                    if i:
                        p.append(soup.new_tag('br'))
                    for c in list(g.contents):
                        p.append(c.extract())
                pieni[0].insert_before(p)
            for g in gruppo:
                g.decompose()
            gruppo.clear()
        for c in figli:
            if riga(c):
                if testo_vuoto(c):
                    chiudi(); c.decompose()
                else:
                    gruppo.append(c)
            elif isinstance(c, NavigableString) and not str(c).strip():
                continue
            else:
                chiudi()
                if isinstance(c, Tag) and c.name in ('div', 'blockquote'):
                    unisci(c)
        chiudi()
    unisci(soup)

    # link interni -> percorsi relativi al sito
    for a in soup.find_all('a', href=True):
        u = urlparse(a['href'])
        if u.netloc == 'www.google.com' and u.path == '/url':
            q = parse_qs(u.query).get('url') or parse_qs(u.query).get('q')
            if q:
                a['href'] = q[0]; u = urlparse(a['href'])
        if u.netloc in DOMINI_INTERNI:
            a['href'] = (u.path or '/') + (('#' + u.fragment) if u.fragment and not u.fragment.startswith('c') else '')
        for att in ('rel', 'target', 'imageanchor', 'style'):
            a.attrs.pop(att, None)

    return str(soup)

def a_markdown(html, segnaposto):
    md = subprocess.run(
        ['pandoc', '-f', 'html', '-t', 'markdown_strict+pipe_tables+strikeout+raw_html-native_spans-native_divs',
         '--wrap=none'],
        input=html, capture_output=True, text=True, check=True).stdout
    # pulizia del markdown
    md = md.replace('\xa0', ' ')
    md = re.sub(r'<span[^>]*>|</span>', '', md)
    md = re.sub(r'</?div[^>]*>', '', md)
    md = re.sub(r'<br\s*/?>\s*\n?', '  \n', md)          # a capo semplici -> hard break markdown
    md = re.sub(r'(?m)^[ \t]+$', '', md)
    righe, in_lista = [], False
    for r in md.split('\n'):
        if re.match(r'\s*([-*+]|\d+\.)\s', r):
            in_lista = True
        elif not r.strip():
            pass
        elif r[:1] == ' ' and not in_lista:
            r = r.lstrip()        # rientri (es. sonetti) che diventerebbero blocchi di codice
        elif r[:1] != ' ':
            in_lista = False
        righe.append(r)
    md = '\n'.join(righe)
    md = re.sub(r'(?m)^\\$', '', md)
    md = re.sub(r'(  \n){2,}', '\n\n', md)               # due a capo -> nuovo paragrafo
    md = re.sub(r'(?m)^  $', '', md)
    md = re.sub(r'  \n(\s*\n)', r'\n\1', md)             # niente hard break a fine paragrafo
    md = re.sub(r'\n\s*\n\s*ZZDESTRAZZ', '\n{.destra}', md)
    md = re.sub(r'(?m)^\s*ZZDESTRAZZ\s*$', '', md)
    for k, v in segnaposto.items():
        md = md.replace(k, v)
    md = re.sub(r'\*\*\s*\*\*|\*\s+\*', '', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip() + '\n'

def ora_locale(iso):
    """Date di Blogger (UTC) -> ora italiana, così la data mostrata è quella giusta."""
    d = datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(ZoneInfo('Europe/Rome'))
    return d.replace(microsecond=0).isoformat()

def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)

# ---------- lettura feed ----------
root = ET.parse(os.path.join(BLOG, 'feed.atom')).getroot()
elenco = []
for e in root.findall('a:entry', NS):
    tipo = e.findtext('b:type', None, NS)
    stato = e.findtext('b:status', None, NS)
    if tipo not in ('POST', 'PAGE') or e.find('b:trashed', NS).text:
        continue  # commenti (spam) e cestino ignorati
    percorso = e.findtext('b:filename', None, NS)
    titolo = (e.findtext('a:title', '', NS) or '').strip()
    data = ora_locale(e.findtext('a:published', None, NS))
    agg = ora_locale(e.findtext('a:updated', None, NS))
    autore = e.findtext('a:author/a:name', '', NS)
    etichette = [c.get('term') for c in e.findall('a:category', NS) if c.get('term')]
    descr = (e.findtext('b:metaDescription', '', NS) or '').strip()
    segnaposto = {}
    html = converti_html(e.findtext('a:content', '', NS) or '', percorso, segnaposto)
    corpo = a_markdown(html, segnaposto)

    fm = ['---', f'title: {yaml_str(titolo)}', f'date: {data}', f'lastmod: {agg}',
          f'url: {percorso}', f'author: {yaml_str(autore)}']
    if etichette:
        fm.append('tags: [' + ', '.join(yaml_str(t) for t in etichette) + ']')
    if descr:
        fm.append(f'description: {yaml_str(descr)}')
    if stato != 'LIVE':
        fm.append('draft: true')
    fm.append('---')

    slug = percorso.rsplit('/', 1)[-1].removesuffix('.html')
    if tipo == 'POST':
        nome = os.path.join(OUT, 'content', 'posts', data[:4], f'{slug}.md')
    else:
        nome = os.path.join(OUT, 'content', 'pagine', f'{slug}.md')
    os.makedirs(os.path.dirname(nome), exist_ok=True)
    with open(nome, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fm) + '\n\n' + corpo)
    elenco.append({'tipo': tipo, 'stato': stato, 'url': percorso, 'titolo': titolo,
                   'file': os.path.relpath(nome, OUT)})

with open(os.path.join(OUT, 'scripts', 'url-originali.json'), 'w', encoding='utf-8') as f:
    json.dump(elenco, f, ensure_ascii=False, indent=1)
print(json.dumps({'voci': len(elenco), 'immagini_locali': len(rapporto['locali']),
                  'immagini_remote': len(rapporto['remote'])}, ensure_ascii=False))
for u, p in rapporto['remote'].items():
    print('REMOTA', p, u[:90])
