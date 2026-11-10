# zerzura.it

Il blog *Zerzura*, costruito con [Hugo](https://gohugo.io) e pubblicato su GitHub Pages all'indirizzo https://www.zerzura.it/.

Come è stato migrato da Blogger: vedi [MIGRAZIONE.md](MIGRAZIONE.md).

## Com'è fatto il progetto

```
content/posts/AAAA/nome-del-post.md   i post, uno per file, divisi per anno
content/pagine/                       le pagine statiche (Nuvole, Stelle…)
content/archivio.md                   la pagina /archivio/
static/images/                        le immagini
layouts/                              i modelli delle pagine
assets/css/stile.css                  l'aspetto del sito
hugo.toml                             configurazione: titolo, menu, indirizzi
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

```markdown
---
title: "Titolo del post"
date: 2026-11-15T10:00:00+01:00
tags: ["Nuvole"]
---

Primo paragrafo del post.

Secondo paragrafo.
```

**Indirizzo.** Viene da anno e mese della data e dal nome del file: il file sopra diventa `/2026/11/titolo-del-post.html`, nello stesso stile dei post di Blogger. Usa nomi di file in minuscolo, senza spazi né accenti (`perche-no.md`, non `Perché no.md`). Per scegliere un indirizzo diverso aggiungi nel front matter `url: /2026/11/altro-nome.html`.

**Data.** Un post con data futura non compare finché quella data non arriva *e* il sito non viene ripubblicato: per programmare un post bisogna quindi fare un push (o lanciare a mano "Pubblica il sito") dopo l'ora indicata. Il fuso è quello italiano: `+01:00` d'inverno, `+02:00` d'estate.

**Bozze.** `draft: true` nel front matter tiene il post nascosto; si vede solo con `hugo server -D`. Toglilo per pubblicarlo.

**Autore.** Non serve indicarlo: la riga "Pubblicato da" usa `author` di `hugo.toml`. Si può scrivere `author: "Nome"` per un post scritto da un'altra persona.

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

Funzionano anche due spazi a fine riga (molti post importati li usano), ma sono invisibili e alcuni editor li cancellano salvando: se due righe si fondono, sostituisci gli spazi con `\`.

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

Con didascalia, in HTML (come nei post importati):

```html
<figure>
  <a href="/images/foto.jpg"><img src="/images/foto.jpg" alt="Descrizione" loading="lazy"></a>
  <figcaption>La didascalia</figcaption>
</figure>
```

Riduci le foto prima di caricarle: 1600 pixel sul lato lungo bastano e fanno pesare il sito molto meno.

### Video di YouTube

```markdown
{{< youtube ID_DEL_VIDEO >}}
```

dove `ID_DEL_VIDEO` è la parte finale dell'indirizzo (`youtube.com/watch?v=ID_DEL_VIDEO`).

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

```markdown
---
title: "Stelle"
url: /p/stelle.html
---

Testo della pagina.
```

Una pagina non compare nel menu da sola: va aggiunta in `hugo.toml`.

## Menu, titolo e barra laterale

In `hugo.toml`:

- `title` e `description` sono il titolo e il motto nella testata;
- il menu in alto è l'elenco `[[menus.main]]`: ogni voce ha `name` (il testo), `url` (o `pageRef` per la home) e `weight` (l'ordine, dal più piccolo);
- `author` in `[params]` è l'autore predefinito dei post.

La barra laterale (etichette, archivio, feed) è in `layouts/_partials/barra.html`; i colori e i caratteri sono definiti all'inizio di `assets/css/stile.css`.

## Controlli automatici (scheda Actions di GitHub)

- **Pubblica il sito**: parte da sola a ogni push; si può lanciare a mano con *Run workflow* (serve per esempio a far comparire un post programmato).
- **Controlla i link esterni**: verifica i link verso altri siti. Lanciato senza spunta produce solo un rapporto; con la spunta "Sostituisci…" mette al posto dei link morti la copia su archive.org più vicina alla data del post, salva le modifiche e ripubblica. Per scegliere una per una le sostituzioni, lancia in locale `python scripts/link_rotti.py --sostituisci`, poi `git add -p content` (`y` tiene, `n` scarta) e `git restore content` per buttare via le altre.
- **Scarica le immagini rimaste su Blogger**: è servita una volta per la migrazione; rilanciarla non fa danni.

Dopo che una Action ha modificato i file, ricordati di fare `git pull` prima di lavorare in locale.
