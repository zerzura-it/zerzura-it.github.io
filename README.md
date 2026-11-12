# zerzura.it

Il blog *Zerzura*, costruito con [Hugo](https://gohugo.io) e pubblicato su GitHub Pages all'indirizzo https://www.zerzura.it/.

Come è stato migrato da Blogger: vedi [MIGRAZIONE.md](MIGRAZIONE.md).

## Com'è fatto il progetto

```
content/posts/AAAA/nome-del-post.md   i post, uno per file, divisi per anno
content/pagine/                       le pagine statiche (Nuvole, Stelle…)
content/archivio.md                   la pagina /archivio/
content/segui.md                      la pagina /segui/ (come seguire il blog via RSS)
static/images/                        le immagini
static/favicon.*, apple-touch-icon.png  l'icona del sito
layouts/                              i modelli delle pagine
layouts/_partials/                    pezzi riusati: barra laterale, post, condivisione
layouts/_shortcodes/youtube.html      il video di YouTube nei post
layouts/_markup/render-link.html      i link esterni che si aprono in una nuova scheda
assets/css/stile.css                  l'aspetto del sito
hugo.toml                             configurazione: titolo, menu, indirizzi
.pages.yml                            configurazione di Pages CMS
.github/workflows/                    pubblicazione e controlli automatici
scripts/                              script di servizio
```

## Lavorare sul blog

Prima di iniziare, scarica eventuali modifiche fatte su GitHub (per esempio dalle Action):

```bash
git pull
```

Anteprima sul tuo computer, con aggiornamento automatico a ogni salvataggio:

```bash
hugo server        # poi apri http://localhost:1313
hugo server -D     # mostra anche le bozze
```

Se una modifica a layout o configurazione non si vede, riavvia con `hugo server --disableFastRender`.

Pubblicazione: ogni push su `main` ricostruisce e ripubblica il sito in un paio di minuti.

```bash
git add .
git commit -m "Nuovo post: Titolo"
git push
```

## Versione di Hugo

Il sito pubblicato è costruito da GitHub con la versione di Hugo scritta in `.github/workflows/hugo.yml`, alla riga `HUGO_VERSION`. Perché l'anteprima sul computer sia identica al sito online, la versione installata in locale deve essere la stessa.

GitHub non la aggiorna da solo: cambia solo se si modifica quella riga. Sul computer invece può cambiare senza accorgersene, per esempio con un `winget upgrade --all`.

**Verificare che siano allineate** (in Git Bash, dalla cartella del progetto):

```bash
grep HUGO_VERSION .github/workflows/hugo.yml   # versione usata da GitHub
hugo version                                   # versione installata sul computer
```

I due numeri devono coincidere, e la versione locale deve essere *extended*.

**Installare la versione giusta** (Windows, con winget):

```bash
winget uninstall Hugo.Hugo.Extended
winget install -q Hugo.Hugo.Extended --version 0.152.2
winget pin add Hugo.Hugo.Extended
```

Al posto di `0.152.2` va il numero indicato in `hugo.yml`. `winget pin add` impedisce a `winget upgrade --all` di aggiornare Hugo di nascosto; quando si vuole cambiare versione si toglie con `winget pin remove Hugo.Hugo.Extended`. Dopo l'installazione chiudi e riapri il terminale e ricontrolla con `hugo version`.

### Quando aggiornare

Non serve seguire ogni rilascio: Hugo esce quasi ogni mese ed è ancora nella serie 0.x, quindi ogni tanto cambia qualcosa in modelli e configurazione, mentre una versione fissata continua a costruire il sito identico per anni. Conviene aggiornare:

- quando serve una funzione che la versione attuale non ha;
- quando la build mostra avvisi `WARN … deprecated`: segnalano qualcosa che in una versione futura smetterà di funzionare, ed è meglio sistemarlo prima che diventi un errore;
- altrimenti circa una volta l'anno, perché il salto tra una versione e l'altra non diventi troppo grande.

Meglio evitare strumenti che aggiornano la versione in automatico (come Renovate): per un blog personale portano avvisi e pull request da gestire senza un vero vantaggio.

### Come aggiornare

Il sito è statico, quindi si può confrontare il risultato prima e dopo l'aggiornamento, file per file.

1. **Costruisci il sito con la versione attuale** in una cartella fuori dal progetto:
   ```bash
   hugo --gc --minify -d ../prova-vecchia
   ```
2. **Leggi le note di rilascio** delle versioni intermedie su https://github.com/gohugoio/hugo/releases, cercando le voci *breaking changes* e *deprecated*.
3. **Installa la nuova versione** con i comandi sopra (con il nuovo numero) e ricostruisci, controllando che non ci siano errori né avvisi:
   ```bash
   hugo --gc --minify -d ../prova-nuova
   ```
4. **Confronta i due risultati:**
   ```bash
   diff -rq ../prova-vecchia ../prova-nuova                       # elenca i file diversi
   diff ../prova-vecchia/index.html ../prova-nuova/index.html     # mostra le differenze di una pagina
   ```
   È normale che cambino tutte le pagine, perché contengono il numero di versione di Hugo (`<meta name="generator">`). Se in qualche pagina di prova cambia solo quello, l'aggiornamento è innocuo; se cambia altro, controlla quelle pagine con `hugo server`.
5. **Aggiorna `HUGO_VERSION`** in `.github/workflows/hugo.yml` con lo stesso numero, fai commit e push, e dai un'occhiata al sito online.
6. Cancella le cartelle di prova: `rm -rf ../prova-vecchia ../prova-nuova`.

**Se qualcosa va storto** dopo il push, rimetti il numero precedente in `hugo.yml`, fai push e reinstalla la vecchia versione in locale. I contenuti non vengono toccati.

## Scrivere un post

Crea un file in `content/posts/` dentro la cartella dell'anno, per esempio `content/posts/2026/titolo-del-post.md`:

```
---
title: "Titolo del post"
date: 2026-11-15T10:00:00
tags: ["Nuvole"]
draft: true
---

Primo paragrafo del post.

Secondo paragrafo.
```

**Indirizzo.** Viene da anno e mese della data e dal nome del file: il file sopra diventa `/2026/11/titolo-del-post.html`, nello stesso stile dei post di Blogger. Usa nomi di file in minuscolo, senza spazi né accenti (`perche-no.md`, non `Perché no.md`). Per scegliere un indirizzo diverso aggiungi nel front matter `url: /2026/11/altro-nome.html`.

**Data.** Un post con data futura non compare finché quella data non arriva *e* il sito non viene ripubblicato: per programmare un post bisogna quindi fare un push (o lanciare a mano "Pubblica il sito") dopo l'ora indicata.

**Bozze.** `draft: true` nel front matter tiene il post nascosto; si vede solo con `hugo server -D`. Toglilo per pubblicarlo.

**Autore.** Non serve indicarlo e non viene mostrato. Solo se un post ha un `author` diverso da quello di `hugo.toml` (per esempio un post scritto da un ospite), in fondo compare "Scritto da Nome".

**Data ed etichette** compaiono sopra il titolo, in maiuscoletto ("MARTEDÌ 15 NOVEMBRE 2016 · NUVOLE"); le etichette sono cliccabili. La data si scrive senza fuso orario, come nell'esempio.

## Scrivere dal telefono (Pages CMS)

Da qualsiasi browser, anche sul telefono, si può scrivere e modificare con [Pages CMS](https://app.pagescms.org): si entra con il proprio account GitHub e si sceglie il repository. La configurazione è in `.pages.yml`.

- **Post** e **Pagine** sono le due sezioni. Un post nuovo ha i campi titolo, data, etichette (una per riga), bozza e il testo in Markdown.
- Salvare fa un commit su GitHub, che ripubblica il sito in un paio di minuti. Per un post nuovo conviene salvarlo con **Bozza** spuntata e toglierla quando è pronto.
- Il nome del file nasce dal titolo, quindi "Il mio post" pubblicato a novembre 2026 diventa `/2026/11/il-mio-post.html`. I post nuovi possono finire direttamente in `content/posts/` invece che nella cartella dell'anno: per il sito non cambia nulla.
- I campi che il modulo non mostra (`url`, `lastmod`, `author` dei post importati) vengono conservati al salvataggio.
- Le immagini caricate finiscono in `static/images/` e si richiamano come `/images/nome.jpg`, con la barra iniziale.
- **Andare a capo sul telefono**: le tastiere trasformano il doppio spazio in ". ", quindi a fine riga usa `<br>` (vedi sotto).
- Se due persone modificano lo stesso file insieme, il secondo salvataggio viene rifiutato ("File has changed…"): copia il tuo testo prima di ricaricare la pagina, poi reinseriscilo.
- Dopo aver scritto da Pages CMS, sul computer fai `git pull` prima di lavorare in locale.

## Formattazione

### Testo

```markdown
*corsivo*   **grassetto**   [un link](https://esempio.it)

### Un titoletto

> Una citazione,
> anche su più righe.

- un elenco
- puntato
```

**Andare a capo.** In Markdown un a capo semplice dentro un paragrafo vale come uno spazio. Per andare a capo senza iniziare un nuovo paragrafo, termina la riga con `\`:

```markdown
Prima riga\
seconda riga
```

Funzionano anche due spazi a fine riga (molti post importati li usano), ma sono invisibili e alcuni editor li cancellano salvando: se due righe si fondono, sostituisci gli spazi con `\`. Dal telefono, dove la tastiera trasforma il doppio spazio in ". " e può aggiungere uno spazio dopo il `\`, il modo più sicuro è `<br>` a fine riga:

```markdown
Prima riga<br>
seconda riga
```

**Link.** I link verso altri siti si aprono da soli in una nuova scheda; quelli interni al blog (`/2018/04/entropia-e-significato.html`) nella stessa. Vale per i link in Markdown: in un link scritto a mano in HTML aggiungi tu `target="_blank" rel="noopener"`.

### Epigrafi allineate a destra

Scrivi `{.destra}` nella riga subito sotto il paragrafo, senza riga vuota in mezzo. Le righe dell'epigrafe, tranne l'ultima, finiscono con **due spazi** (invisibili qui sotto) per andare a capo:

```markdown
Questo mistero è grande␣␣
lo dico in riferimento a Cristo e alla Chiesa!␣␣
Ef 5,32
{.destra}
```

(`␣␣` indica i due spazi: nel file vanno scritti come spazi veri.) Se l'editor li cancella salvando, usa al loro posto `\` a fine riga, che ha lo stesso effetto.

### Note a piè di pagina

```markdown
Il testo con il richiamo alla nota[^1] e a un'altra[^doron].

[^1]: Una nota breve.

[^doron]: Una nota di più paragrafi. I paragrafi dopo il primo
    sono rientrati di 4 spazi:

    > Anche una citazione dentro la nota,
    > con le righe rientrate.
    >
    > Secondo paragrafo della citazione.

    Un ultimo paragrafo della nota.
```

- Le note vengono numerate 1, 2, 3… nell'ordine dei richiami, qualunque nome tu usi dopo `^`.
- Compaiono in fondo al post, con una freccia ↩ che torna al richiamo.
- La nota finisce alla prima riga non rientrata. Usa spazi, non tabulazioni.

### Immagini

Copia l'immagine in `static/images/` (nome in minuscolo, senza spazi) e richiamala con `/images/`:

```markdown
![Descrizione dell'immagine](/images/foto.jpg)
```

Con didascalia, usa lo shortcode `figure`. La didascalia si scrive in Markdown e i link esterni si aprono in una nuova scheda come nel resto del testo:

```
{{< figure src="/images/foto.jpg" link="/images/foto.jpg" alt="Descrizione"
    caption="Foto di [Mario Rossi](https://esempio.it), *2016*" >}}
```

- `link` è facoltativo e rende l'immagine cliccabile;
- dentro `caption` non usare le virgolette doppie (`"`), che chiudono il parametro: usa quelle tipografiche (“ ”) o gli apostrofi.

I post importati usano `<figure>` scritto in HTML: lì il Markdown non viene interpretato, quindi un link nella didascalia va scritto in HTML con `target="_blank" rel="noopener"`.

**Dimensioni.** Le immagini sono centrate e grandi al massimo 400 pixel per lato, come le immagini "grandi" di Blogger; un clic apre la versione piena (con `link`). Sul telefono occupano tutta la larghezza del testo. I valori sono all'inizio della sezione immagini di `assets/css/stile.css`: `--max-immagini: 25rem` (400 px; `20rem` = 320 px, `30rem` = 480 px) e `--largh-immagini: 85%`.

Riduci le foto prima di caricarle: 1600 pixel sul lato lungo bastano e fanno pesare il sito molto meno.

### Video di YouTube

```markdown
{{< youtube ID_DEL_VIDEO >}}
```

dove `ID_DEL_VIDEO` è la parte finale dell'indirizzo (`youtube.com/watch?v=ID_DEL_VIDEO`). Il video ha le stesse dimensioni delle immagini (al massimo 400 px, a tutta larghezza sul telefono) e usa `youtube-nocookie.com`, che non imposta cookie finché il visitatore non lo avvia. Lo shortcode è in `layouts/_shortcodes/youtube.html`.

## Etichette

Basta scriverle nel front matter: un'etichetta nuova crea da sola la sua pagina.

```yaml
tags: ["Nuvole", "Città nuove"]
```

- La pagina dell'etichetta è `/search/label/Nome/` (gli spazi diventano trattini: `/search/label/Città-nuove/`).
- Il nome viene mostrato esattamente come lo scrivi; maiuscole e minuscole contano, quindi "Nuvole" e "nuvole" sono due etichette diverse.
- La barra laterale le elenca tutte con il numero dei post.

## Pagine statiche

Stanno in `content/pagine/`, con l'indirizzo nel campo `url` (nello stile di Blogger, `/p/nome.html`):

```
---
title: "Stelle"
url: /p/stelle.html
---

Testo della pagina.
```

Una pagina non compare nel menu da sola: va aggiunta in `hugo.toml`. Le pagine non mostrano la data, nemmeno se nel front matter ce n'è una (che però, se è nel futuro, ne ritarda la pubblicazione come per i post).

## Menu, titolo e barra laterale

In `hugo.toml`:

- `title` e `description` sono il titolo e il motto nella testata;
- il menu in alto è l'elenco `[[menus.main]]`: ogni voce ha `name` (il testo), `url` (o `pageRef` per la home) e `weight` (l'ordine, dal più piccolo);
- `author` in `[params]` è l'autore predefinito dei post.

La barra laterale è in `layouts/_partials/barra.html`:

- **Etichette**, con il numero dei post;
- **Post recenti**: gli ultimi 5 (per cambiarne il numero, modifica `first 5`);
- **Archivio**: gli anni con il numero dei post; un clic porta alla pagina `/archivio/` già posizionata su quell'anno;
- **Ricevi i nuovi post (RSS)**: porta alla pagina `/segui/`, che spiega cos'è un feed, permette di copiarne l'indirizzo e suggerisce qualche lettore. Il feed vero e proprio è `/feed.xml`. Il testo della pagina è in `content/segui.md`, il resto in `layouts/segui.html`.

I colori e i caratteri sono definiti all'inizio di `assets/css/stile.css`.

## Condivisione

Sotto ogni post (nella sua pagina, in home e nelle pagine delle etichette) c'è il blocco **Condividi · Fediverso · Email**, in `layouts/_partials/condividi.html`, senza script né pulsanti di servizi esterni:

- **Condividi** apre sul telefono il menu di condivisione del sistema (Signal, posta, Mastodon…); sul computer copia il link del post.
- **Fediverso** chiede l'istanza del visitatore (es. `mastodon.uno`), la ricorda solo nel suo browser e apre la pagina di condivisione di quell'istanza (Mastodon e server compatibili).
- **Email** apre il programma di posta con titolo e link.

## Icona del sito

`static/favicon.svg`, `static/favicon.ico` e `static/apple-touch-icon.png` (la Z bianca su azzurro), dichiarate in `layouts/baseof.html`. Per cambiarla basta sostituire i tre file con gli stessi nomi; i browser conservano a lungo le icone, quindi per vedere subito quella nuova ricarica con Ctrl+F5.

## Controlli automatici (scheda Actions di GitHub)

- **Pubblica il sito**: parte da sola a ogni push; si può lanciare a mano con *Run workflow* (serve per esempio a far comparire un post programmato).
- **Controlla i link esterni**: verifica i link verso altri siti. Lanciato senza spunta produce solo un rapporto; con la spunta "Sostituisci…" mette al posto dei link morti la copia su archive.org più vicina alla data del post, salva le modifiche e ripubblica. Per scegliere una per una le sostituzioni, lancia in locale `python scripts/link_rotti.py --sostituisci`, poi `git add -p content` (`y` tiene, `n` scarta) e `git restore content` per buttare via le altre.
- **Scarica le immagini rimaste su Blogger**: è servita una volta per la migrazione; rilanciarla non fa danni.

Dopo che una Action ha modificato i file, ricordati di fare `git pull` prima di lavorare in locale.
