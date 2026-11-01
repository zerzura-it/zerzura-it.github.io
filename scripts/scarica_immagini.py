#!/usr/bin/env python3
"""Scarica le immagini rimaste sui server di Google e aggiorna i post.

Alcune immagini dei vecchi post (soprattutto quelle incollate da Google Docs)
non erano nell'export di Blogger: i post le richiamano ancora da
*.googleusercontent.com. Questo script le scarica in static/images/ e
sostituisce gli indirizzi nei file Markdown.

Uso (dalla cartella del progetto):  python3 scripts/scarica_immagini.py
Si può lanciare più volte: le immagini già scaricate non vengono toccate.
"""
import pathlib, re, sys, urllib.request

RADICE = pathlib.Path(__file__).resolve().parent.parent
IMMAGINI = RADICE / 'static' / 'images'
URL = re.compile(r'https?://(?:[\w-]+\.)*(?:googleusercontent\.com|bp\.blogspot\.com)/[^\s"\')<>]+')
ESTENSIONI = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/gif': '.gif', 'image/webp': '.webp'}

def scarica(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (migrazione zerzura.it)'})
    with urllib.request.urlopen(req, timeout=60) as r:
        tipo = r.headers.get_content_type()
        if not tipo.startswith('image/'):
            raise ValueError(f'non è un\'immagine ({tipo})')
        return r.read(), ESTENSIONI.get(tipo, '.' + tipo.split('/')[1])

def principale():
    IMMAGINI.mkdir(parents=True, exist_ok=True)
    fatti, falliti = {}, []
    for md in sorted((RADICE / 'content').rglob('*.md')):
        testo = md.read_text(encoding='utf-8')
        trovati = list(dict.fromkeys(URL.findall(testo)))
        if not trovati:
            continue
        nome_post = md.stem
        for i, url in enumerate(trovati, 1):
            if url not in fatti:
                # chiede la versione a piena risoluzione dove possibile
                grande = re.sub(r'=w\d+-h\d+(-[\w-]+)?$', '=s0', url)
                try:
                    dati, est = scarica(grande)
                except Exception:
                    try:
                        dati, est = scarica(url)
                    except Exception as e:
                        falliti.append((md.relative_to(RADICE), url, e))
                        continue
                nome = f'{nome_post}-{i}{est}'
                (IMMAGINI / nome).write_bytes(dati)
                fatti[url] = '/images/' + nome
                print(f'scaricata  {nome}  ({len(dati) // 1024} KB)')
            testo = testo.replace(url, fatti[url])
        md.write_text(testo, encoding='utf-8')
    print(f'\n{len(fatti)} immagini scaricate.')
    for f, url, e in falliti:
        print(f'NON SCARICATA  {f}: {url[:80]}…  ({e})')
    return 1 if falliti else 0

if __name__ == '__main__':
    sys.exit(principale())
