#!/usr/bin/env python3
"""Trova i link esterni rotti nei post e li sostituisce con la copia su archive.org.

Per ogni link esterno dei post controlla se la pagina risponde ancora. Se non
esiste più (errore 404/410, dominio scomparso, connessione rifiutata...) cerca
su archive.org la copia salvata più vicina alla data del post e sostituisce il
link con quella.

Uso (dalla cartella del progetto):
    python3 scripts/link_rotti.py              # solo rapporto, non modifica nulla
    python3 scripts/link_rotti.py --sostituisci

I siti che bloccano i controlli automatici (Instagram, Facebook, Amazon...)
rispondono spesso con 403 o 429 anche quando la pagina esiste: questi link
vengono segnalati come "da verificare a mano" e non vengono toccati.
"""
import json, pathlib, re, socket, ssl, sys, time, urllib.error, urllib.parse, urllib.request

RADICE = pathlib.Path(__file__).resolve().parent.parent
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'
# link in Markdown [testo](url) e in HTML href="url"
LINK = re.compile(r'(?<=\]\()https?://[^)\s]+(?=\))|(?<=href=")https?://[^"]+(?=")')
IGNORA = ('web.archive.org', 'archive.org/wayback', 'googleusercontent.com', 'bp.blogspot.com',
          'zerzura.it', 'zerzura-it.github.io')
ROTTO = {404, 410, 451}
BLOCCATO = {401, 403, 405, 406, 429, 999}


def controlla(url):
    """Ritorna ('ok'|'rotto'|'dubbio', dettaglio)."""
    for tentativo in range(2):
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*;q=0.8',
                                                   'Accept-Language': 'it,en;q=0.8'})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return 'ok', str(r.status)
        except urllib.error.HTTPError as e:
            if e.code in ROTTO:
                return 'rotto', f'HTTP {e.code}'
            if e.code in BLOCCATO:
                return 'dubbio', f'HTTP {e.code} (il sito blocca i controlli automatici)'
            if e.code >= 500 and tentativo == 0:
                time.sleep(3)
                continue
            return 'dubbio', f'HTTP {e.code}'
        except urllib.error.URLError as e:
            motivo = e.reason
            if isinstance(motivo, socket.gaierror):
                return 'rotto', 'dominio inesistente'
            if isinstance(motivo, ConnectionRefusedError):
                return 'rotto', 'connessione rifiutata'
            if isinstance(motivo, ssl.SSLError) or 'CERTIFICATE' in str(motivo):
                return 'rotto', 'certificato non valido'
            if tentativo == 0:
                time.sleep(3)
                continue
            return 'dubbio', str(motivo)[:80]
        except (TimeoutError, socket.timeout):
            if tentativo == 0:
                continue
            return 'dubbio', 'tempo scaduto'
        except Exception as e:  # risposte malformate ecc.
            return 'dubbio', type(e).__name__
    return 'dubbio', '?'


def copia_archiviata(url, data):
    """Copia su archive.org più vicina a data (AAAAMMGG), preferendo quelle precedenti al post."""
    q = urllib.parse.urlencode({'url': url, 'timestamp': data})
    for tentativo in range(3):
        try:
            req = urllib.request.Request(f'https://archive.org/wayback/available?{q}', headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                snap = json.load(r).get('archived_snapshots', {}).get('closest')
            if snap and snap.get('available') and str(snap.get('status', '200')).startswith(('2', '3')):
                return f"https://web.archive.org/web/{snap['timestamp']}/{url}", snap['timestamp']
            return None, None
        except Exception:
            time.sleep(5 * (tentativo + 1))
    return None, None


def data_post(testo):
    m = re.search(r'(?m)^date:\s*(\d{4})-(\d{2})-(\d{2})', testo)
    return ''.join(m.groups()) if m else '20200101'


def principale():
    sostituisci = '--sostituisci' in sys.argv
    esiti = {}
    righe = []
    for md in sorted((RADICE / 'content').rglob('*.md')):
        testo = md.read_text(encoding='utf-8')
        data = data_post(testo)
        sostituzioni = {}
        for url in dict.fromkeys(LINK.findall(testo)):
            if any(x in url for x in IGNORA):
                continue
            if url not in esiti:
                esiti[url] = controlla(url)
                time.sleep(0.5)
            stato, dettaglio = esiti[url]
            archiviata = ''
            if stato == 'rotto':
                arch, quando = copia_archiviata(url, data)
                time.sleep(1.5)  # archive.org limita le richieste troppo fitte
                if arch:
                    archiviata = arch
                    sostituzioni[url] = arch
                else:
                    dettaglio += ', nessuna copia su archive.org'
            if stato != 'ok':
                righe.append((stato, str(md.relative_to(RADICE)), url, dettaglio, archiviata))
        if sostituisci and sostituzioni:
            # sostituisce solo i link esatti, non altri testi che li contengono
            nuovo = LINK.sub(lambda m: sostituzioni.get(m.group(0), m.group(0)), testo)
            md.write_text(nuovo, encoding='utf-8')

    # rapporto (anche in formato Markdown per il riepilogo di GitHub Actions)
    tot = len(esiti)
    rotti = [r for r in righe if r[0] == 'rotto']
    dubbi = [r for r in righe if r[0] == 'dubbio']
    out = [f'## Controllo dei link esterni', '',
           f'Link controllati: {tot} · rotti: {len(rotti)} · da verificare a mano: {len(dubbi)}', '']
    if rotti:
        out += ['### Link rotti', '', '| Post | Link | Problema | Copia su archive.org |', '|---|---|---|---|']
        out += [f'| {f} | {u} | {d} | {a or "—"} |' for _, f, u, d, a in rotti]
        out.append('')
        out.append('I link con una copia su archive.org ' +
                   ('**sono stati sostituiti**.' if sostituisci else 'verranno sostituiti lanciando lo script con `--sostituisci`.'))
        out.append('')
    if dubbi:
        out += ['### Da verificare a mano', '', '| Post | Link | Risposta |', '|---|---|---|']
        out += [f'| {f} | {u} | {d} |' for _, f, u, d, _ in dubbi]
        out.append('')
    rapporto = '\n'.join(out)
    print(rapporto)
    (RADICE / 'scripts' / 'rapporto-link.md').write_text(rapporto + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(principale())
