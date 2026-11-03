La strada più comoda è lanciare la sostituzione **sul tuo computer** invece che nell'Action, e scegliere poi una per una le modifiche da tenere prima del commit. Serve Python 3: su Windows lo installi da python.org o dal Microsoft Store, e da Git Bash lo richiami con `python` oppure `py`.

**1. Prepara e lancia la sostituzione**
```bash
git pull
python scripts/link_rotti.py --sostituisci
```
Lo script modifica i post e stampa lo stesso rapporto che vedresti nell'Action.

**2. Rivedi le modifiche una per una**
```bash
git add -p content
```
Git ti mostra ogni sostituzione (vecchio link in rosso, nuovo in verde) e per ciascuna ti chiede cosa fare: `y` la tiene, `n` la scarta, `q` interrompe la revisione. Se un blocco contiene più link e vuoi decidere separatamente, `s` lo divide in parti più piccole. Se vuoi controllare una copia prima di decidere, aprila nel browser: l'indirizzo `web.archive.org/...` è scritto nella riga verde.

**3. Butta via quelle scartate e pubblica**
```bash
git restore content
git commit -m "Link rotti sostituiti con le copie su archive.org"
git push
```
`git restore` annulla solo le sostituzioni a cui hai risposto `n`; quelle accettate sono già pronte per il commit.

**In alternativa, senza Python**
Lancia l'Action in modalità solo rapporto e sostituisci a mano soltanto i link che ti convincono, copiando l'indirizzo di archive.org dalla tabella del riepilogo dentro il file del post. Con pochi link rotti è altrettanto rapido.

Infine, se hai già fatto la sostituzione con l'Action e una non ti piace, basta aprire il post e rimettere il link originale. Nell'indirizzo di archive.org l'originale compare per intero dopo la data, per esempio `https://web.archive.org/web/20160526…/http://motherboard.vice.com/…`. Lo script non toccherà più quel link solo finché il sito risponde; se torna a dare errore, alla prossima esecuzione lo riproporrà.
