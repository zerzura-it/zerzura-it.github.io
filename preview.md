Sei su Windows, quindi il modo più semplice è **winget**, già presente in Windows 10 e 11.

**1. Installa Hugo**
In un terminale (PowerShell o Git Bash):
```bash
winget install Hugo.Hugo.Extended
```
Poi **chiudi e riapri** il terminale, così trova il nuovo comando, e verifica:
```bash
hugo version
```

**2. Allinea la versione con quella di GitHub**
Il workflow di pubblicazione usa Hugo **0.152.2**, mentre winget installa l'ultima versione disponibile. Di solito non cambia nulla, ma per essere sicuro che quello che vedi in locale sia identico al sito online hai due possibilità:
- installare la stessa versione: `winget install Hugo.Hugo.Extended --version 0.152.2`. Se winget non la trova, la scarichi da [github.com/gohugoio/hugo/releases](https://github.com/gohugoio/hugo/releases/tag/v0.152.2) come `hugo_extended_0.152.2_windows-amd64.zip`, estrai `hugo.exe` in una cartella e la aggiungi al PATH;
- oppure aggiornare il workflow alla tua versione: in `.github/workflows/hugo.yml` cambi `HUGO_VERSION: 0.152.2` con il numero che ti dà `hugo version`.

**3. Avvia l'anteprima**
Dalla cartella del progetto:
```bash
cd zerzura.it
hugo server
```
Apri http://localhost:1313. La pagina si aggiorna da sola ogni volta che salvi un post, il CSS o un layout. Per fermare il server usa Ctrl+C.

Due opzioni utili:
- `hugo server -D` mostra anche le bozze (`draft: true`), per esempio la pagina *Stelle*;
- `hugo server --disableFastRender` ricostruisce tutto il sito a ogni modifica. Usalo se cambi layout o configurazione e qualche pagina non si aggiorna.

Se vuoi provare la build esattamente come la fa GitHub, lancia `hugo --gc --minify`: il risultato finisce nella cartella `public/`, che è già esclusa da Git tramite `.gitignore`.
