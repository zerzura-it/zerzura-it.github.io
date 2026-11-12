# Migrazione da Blogger

Come il blog è passato da Blogger (versozerzura.blogspot.com, con dominio www.zerzura.it) a Hugo su GitHub Pages, nel novembre 2026. Serve come promemoria e come traccia per migrare altri blog allo stesso modo.

## Cosa è stato importato

- **45 post** pubblicati tra il 2013 e il 2024 e le pagine **Nuvole** (`/p/blog-page.html`) e **Stelle**.
- *Stelle* su Blogger era una bozza con indirizzo `/p/paolo-de-benedetti-introduzione-al.html`; dopo la migrazione è stata pubblicata a `/p/stelle.html`.
- Le etichette *Nuvole* e *Darash*.
- **Non importati**: i commenti (quasi tutti spam) e i post nel cestino.

Ogni post importato ha nel front matter il campo `url` con l'indirizzo originale di Blogger, la data di pubblicazione e quella di ultima modifica (convertite all'ora italiana; in seguito la data di pubblicazione è stata riscritta senza fuso orario, vedi sotto), l'autore e le etichette. L'elenco completo degli indirizzi originali è in `scripts/url-originali.json`.

## Indirizzi conservati

| Blogger | Sito nuovo |
|---|---|
| `/AAAA/MM/titolo.html` | identico (campo `url` nei post importati; i post nuovi seguono lo stesso schema) |
| `/p/blog-page.html` | identico |
| `/search/label/Nuvole` | `/search/label/Nuvole/` (GitHub aggiunge da solo la barra finale) |
| archivi `/AAAA/MM/` | non ricreati: c'è un'unica pagina `/archivio/` |
| feed `/feeds/posts/default` | non esiste più: il feed è `/feed.xml` |

Configurazione che lo rende possibile, in `hugo.toml`:

- `disablePathToLower = true`: Blogger distingueva maiuscole e minuscole (`/search/label/Nuvole`);
- `[permalinks.page] posts = "/:year/:month/:contentbasename"` insieme a `[uglyURLs] posts = true`: i post nuovi diventano file `/AAAA/MM/nome.html`. Con il solo permalink terminante in `.html` Hugo avrebbe creato cartelle (`/AAAA/MM/nome.html/`);
- `[permalinks.term] tags = "/search/label/:slug/"` per le etichette;
- `capitalizeListTitles = false`, perché i nomi delle etichette restino come sono scritti.

## Conversione dei contenuti

Lo script `scripts/converti.py` legge l'export di Google Takeout (`Takeout/Blogger/Blogs/<blog>/feed.atom` e gli album in `Takeout/Blogger/Albums/`) e produce i file Markdown. Richiede Python 3, `pandoc`, BeautifulSoup e Pillow.

```bash
python3 scripts/converti.py "Takeout/Blogger/Blogs/<blog>" "Takeout/Blogger/Albums/<blog>" <progetto-hugo>
```

Cosa fa:

- converte l'HTML di Blogger in Markdown con pandoc, dopo averlo ripulito (stili inline, `<span>`, `<div>` usati come righe, che diventano paragrafi con a capo);
- trasforma le tabelle-didascalia di Blogger in `<figure>` con `<figcaption>`;
- trasforma i blocchi allineati a destra (epigrafi) in paragrafi con `{.destra}` sotto; un `<br>` a fine riga dentro un'epigrafe non viene raddoppiato (la prima versione dello script spezzava così l'epigrafe di *Biopolitica e clero*);
- sostituisce i video di YouTube con lo shortcode `{{< youtube >}}`;
- rende relativi i link interni (www.zerzura.it e versozerzura.blogspot.com);
- prende le immagini dagli album di Takeout, cercando prima nell'album del blog e poi negli altri dello stesso account (alcune immagini di Zerzura erano nell'album di Puer Ludens); riduce a 1600 px le foto più grandi.

Verifiche fatte sul risultato: tutti gli indirizzi originali esistono nel sito costruito; il testo di ogni post coincide parola per parola con l'originale; nessun link interno rotto.

### Immagini mancanti nell'export

Quattordici immagini, incollate a suo tempo da Google Docs, non erano negli album di Takeout. Il workflow **"Scarica le immagini rimaste su Blogger"** (`scripts/scarica_immagini.py`) le ha scaricate dai server di Google in `static/images/` e ha aggiornato i post. Per verificare che non ne resti nessuna:

```bash
grep -rnE "googleusercontent\.com|bp\.blogspot\.com" content
```

### Modifiche successive ai contenuti importati

- Ai link esterni scritti in HTML (soprattutto nelle didascalie) sono stati aggiunti `target="_blank" rel="noopener"`; i link in Markdown li ricevono dal render hook `layouts/_markup/render-link.html`.
- Il controllo dei link esterni (`scripts/link_rotti.py`, workflow "Controlla i link esterni") sostituisce i link morti con le copie su archive.org.
- **Date senza fuso orario.** Pages CMS salva le date come `2026-11-10T18:50:00` e non riconosceva quelle importate (`2013-06-24T14:51:00+02:00`): aprendo un post vecchio le sostituiva con l'ora corrente. Il fuso è stato tolto da tutte le date `date:` con
  `sed -i -E 's/^(date: [0-9-]+T[0-9:]+)[+-][0-9]{2}:[0-9]{2}$/\1/' …`.
  Il sito generato è rimasto identico, perché Hugo interpreta le date senza fuso come ora italiana (`timeZone = "Europe/Rome"`).
- L'epigrafe di *Biopolitica e clero* è stata corretta a mano (vedi la nota sullo script qui sopra).
- La pagina *Stelle*, bozza su Blogger, è stata pubblicata a `/p/stelle.html`.

## Ritocchi al sito dopo la migrazione

Rispetto alla prima versione:

- **Navigazione tra i post** in ordine cronologico, con "Post precedente" a sinistra e "Post successivo" a destra (`layouts/page.html`).
- **Barra laterale**: al posto delle tendine di Blogger per anni e mesi, gli ultimi 5 post e gli anni come link alla pagina `/archivio/`, che ha un'àncora per anno.
- **Data ed etichette sopra il titolo**; tolta la riga "Pubblicato da" (l'autore compare solo se diverso da quello del sito). Le pagine non mostrano la data.
- **Immagini e video** al massimo 400 px, come le immagini "grandi" di Blogger, a tutta larghezza sul telefono. Lo shortcode `youtube` di Hugo, che occupava sempre tutta la larghezza, è stato sostituito da `layouts/_shortcodes/youtube.html` (con `youtube-nocookie.com`).
- **Note a piè di pagina** (`enableAutoIDPrefix`, perché le note di più post nella stessa pagina non si confondano) e **link esterni in una nuova scheda** (render hook).
- **Condivisione** in fondo ai post: Condividi (menu di sistema o copia del link), Fediverso, Email. Volutamente niente WhatsApp, Telegram o pulsanti di servizi che tracciano i visitatori.
- **Pagina `/segui/`** al posto del link diretto al feed RSS, che i browser mostrano come codice XML.
- **Icona del sito**: senza, i browser continuavano a mostrare quella di Blogger rimasta in cache.
- **Pages CMS** (`.pages.yml`) per scrivere dal telefono, con il testo in Markdown e `merge: true` per non perdere `url` e gli altri campi dei post importati.
- Tolto il link ad about.me.

## Messa online

1. Organizzazione GitHub `zerzura-it`, repository pubblico **`zerzura-it.github.io`**: con questo nome il sito è servito alla radice di https://zerzura-it.github.io/ e si può controllare prima di spostare il dominio (con un altro nome starebbe in una sottocartella e le immagini, richiamate con `/images/…`, non si vedrebbero).
2. *Settings → Pages → Source: GitHub Actions*. Al primo push GitHub ha lanciato anche la sua pubblicazione automatica con Jekyll ("pages-build-deployment"), che ha sovrascritto il sito: è bastato rilanciare "Pubblica il sito". Con Source su GitHub Actions non si ripresenta.
3. Workflow in `.github/workflows/`:
   - `hugo.yml` (**Pubblica il sito**): Hugo 0.152.2, a ogni push su `main`, a mano, e dopo le due Action che modificano i contenuti (i commit fatti dalle Action non farebbero ripartire la pubblicazione da soli);
   - `scarica-immagini.yml` e `link-rotti.yml`: da lanciare a mano.
   Le Action usate sono nelle versioni per Node 24 (`checkout@v5`, `setup-python@v6`, `configure-pages@v6`, `upload-pages-artifact@v5`, `deploy-pages@v5`).
4. Consigliato: verificare il dominio nelle impostazioni Pages dell'organizzazione (record TXT `_github-pages-challenge-zerzura-it`), così nessun altro può usarlo su GitHub.

## Spostamento del dominio

Ordine seguito, che evita interruzioni:

1. **GitHub**: *Settings → Pages → Custom domain* `www.zerzura.it` (il controllo DNS fallisce finché il DNS punta a Google: è normale). Il file `static/CNAME` contiene lo stesso dominio, ma con la pubblicazione tramite Actions conta l'impostazione.
2. **DNS**:
   - `www`: CNAME cambiato da `ghs.google.com` a `zerzura-it.github.io`;
   - `@`: i record A di Google sostituiti con `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`;
   - il CNAME di verifica di Blogger (nome lungo) lasciato per ora.
3. Quando il controllo DNS di GitHub è verde: **Enforce HTTPS**. Poi una nuova pubblicazione, perché indirizzo canonico e feed usino www.zerzura.it invece di zerzura-it.github.io.
4. **Blogger**: il dominio personalizzato va tolto *dopo* lo spostamento del DNS, non prima (altrimenti il sito resta irraggiungibile finché il DNS non cambia). Finché resta impostato, i vecchi link a versozerzura.blogspot.com reindirizzano a www.zerzura.it, quindi conviene tenerlo ancora per un po'. Quando lo si toglie (*Impostazioni → Pubblicazione → Dominio personalizzato*) si può eliminare anche il CNAME di verifica di Blogger. Il blog su Blogger non va cancellato prima di aver recuperato tutte le immagini.

Per controllare il DNS: `nslookup www.zerzura.it` deve rispondere `zerzura-it.github.io`.

## Da ricordare per altri blog

- Esportare con Google Takeout (Blogger) invece del backup XML dal pannello: contiene anche gli album con le immagini.
- Le bozze e le pagine non pubblicate sono nell'export: decidere caso per caso.
- Controllare gli album di tutti i blog dello stesso account: le immagini non sempre stanno nell'album del blog in cui compaiono.
- Le immagini incollate da Google Docs (`lh*.googleusercontent.com` senza nome di file) non sono negli album: vanno scaricate dai server di Google finché esistono.
- Scrivere le date senza fuso orario fin dalla conversione, se si userà Pages CMS.
- Aggiungere subito un'icona al sito, altrimenti resta quella di Blogger.
