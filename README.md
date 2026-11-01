# zerzura.it

Il blog *Zerzura*, migrato da Blogger a [Hugo](https://gohugo.io) e pubblicato con GitHub Pages.

## Com'è fatto

```
content/posts/AAAA/nome-del-post.md   i post, uno per file, divisi per anno
content/pagine/                       le pagine statiche (es. /p/blog-page.html)
static/images/                        le immagini
layouts/  assets/css/stile.css        aspetto del sito
hugo.toml                             configurazione (titolo, menu, indirizzi)
scripts/                              script usati per la migrazione
```

Indirizzi:

- i post importati mantengono l'indirizzo di Blogger grazie al campo `url` nel front matter;
- i post nuovi ricevono automaticamente un indirizzo nello stesso stile, ricavato da anno, mese e nome del file: `content/posts/2026/titolo.md` pubblicato a novembre 2026 diventa `/2026/11/titolo.html`;
- le etichette restano a `/search/label/Nuvole/` e `/search/label/Darash/`;
- l'archivio completo è a `/archivio/`, il feed RSS a `/feed.xml`.

## Scrivere un post

Crea un file `content/posts/2026/titolo-del-post.md`:

```markdown
---
title: "Titolo del post"
date: 2026-11-15T10:00:00+01:00
tags: ["Nuvole"]
---

Testo in Markdown.

Una citazione in epigrafe,
allineata a destra
{.destra}

![Didascalia](/images/foto.jpg)
```

- `draft: true` nel front matter tiene il post nascosto finché non lo togli.
- Un post con data futura non compare finché quella data non arriva (e il sito non viene ricostruito).
- Per un video di YouTube: `{{< youtube ID_DEL_VIDEO >}}`.
- I post importati contengono qualche `<figure>` in HTML per le immagini con didascalia: si può modificare come normale HTML.

Anteprima sul tuo computer, con aggiornamento automatico a ogni salvataggio:

```bash
hugo server
```

poi apri http://localhost:1313. Ogni push su `main` ripubblica il sito in un paio di minuti.

## Messa online (una volta sola)

1. Nell'organizzazione `zerzura-it` crea un repository **pubblico e vuoto** chiamato `zerzura-it.github.io`. Con questo nome il sito è servito alla radice (https://zerzura-it.github.io/) e si può controllare prima di spostare il dominio.
2. Carica il progetto:
   ```bash
   git remote add origin https://github.com/zerzura-it/zerzura-it.github.io.git
   git push -u origin main
   ```
3. Nel repository: *Settings → Pages → Build and deployment → Source: **GitHub Actions***. Poi in *Actions* lancia di nuovo "Pubblica il sito" se il primo tentativo è fallito perché Pages non era ancora attivo.
4. In *Actions* lancia una volta **"Scarica le immagini rimaste su Blogger"** (*Run workflow*). Scarica le 14 immagini che non erano nell'export (vedi sotto) e ripubblica il sito.
5. Controlla il sito su https://zerzura-it.github.io/.

## Spostamento del dominio

Da fare solo quando il sito su `zerzura-it.github.io` ti convince, perché da quel momento www.zerzura.it smette di puntare a Blogger.

1. In Blogger: *Impostazioni → Pubblicazione → Dominio personalizzato*, rimuovi `www.zerzura.it`.
2. Nel pannello DNS del dominio:
   - `www` → record **CNAME** verso `zerzura-it.github.io` (al posto di `ghs.google.com`);
   - dominio senza `www` (`@`) → quattro record **A**: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`;
   - elimina il secondo CNAME che Blogger aveva fatto aggiungere per la verifica (quello con un codice lungo come nome).
3. In GitHub: *Settings → Pages → Custom domain* scrivi `www.zerzura.it` e salva; quando il controllo DNS è verde attiva **Enforce HTTPS** (il certificato può richiedere fino a un'ora).
4. Il blog su Blogger puoi lasciarlo com'è (senza dominio resta su versozerzura.blogspot.com) o renderlo privato. Non cancellarlo prima di aver lanciato il punto 4 della messa online.

## Note sulla migrazione

- Importati 45 post e la pagina *Nuvole*. La pagina in bozza *Stelle* è in `content/pagine/` con `draft: true`, quindi non viene pubblicata.
- I commenti (quasi tutti spam) non sono stati importati.
- Le immagini sono state prese dall'archivio Takeout (39, le più grandi ridotte a 1600 px). Quattordici immagini incollate a suo tempo da Google Docs non erano nell'archivio: i post le richiamano ancora dai server di Google finché non lanci il workflow di scaricamento. Se alcune risultassero non più disponibili, il log del workflow le elenca.
- `scripts/url-originali.json` elenca tutti gli indirizzi originali; `scripts/converti.py` è lo script di conversione, riutilizzabile per altri blog Blogger.
- Il vecchio feed `/feeds/posts/default` non esiste più: chi seguiva il blog via RSS deve usare `/feed.xml`.
