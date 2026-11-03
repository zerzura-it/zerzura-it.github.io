---
title: "Entropia e significato"
date: 2018-04-25T05:00:00+02:00
lastmod: 2018-04-26T12:19:32+02:00
url: /2018/04/entropia-e-significato.html
author: "Emanuele"
tags: ["Nuvole"]
---

Non è facile dare una definizione di [casualità](/2016/05/il-caso-non-esiste.html) nemmeno per i matematici. Come esempio basti considerare che anche la successione di cifre decimali di pi greco passa tutti i test che misurano la distribuzione casuale delle cifre, per cui potrebbe [apparire casuale](/2017/12/numeri-caso.html), ma non lo è poiché esiste ovviamente un algoritmo per calcolarla.

<figure><a href="/images/Andrej_Nikolajewitsch_Kolmogorov.jpg"><img src="/images/Andrej_Nikolajewitsch_Kolmogorov.jpg" alt="" loading="lazy"></a><figcaption><a href="https://it.wikipedia.org/wiki/Andrej_Nikolaevi%C4%8D_Kolmogorov">Andrej Nikolaevič Kolmogorov</a></figcaption></figure>

Secondo la teoria della complessità di Andrej Nikolaevič Kolmogorov si può sostenere che una sequenza è casuale quando non può essere “compressa”, cioè ricondotta in qualche modo a una sequenza più corta. Anche una definizione del genere presenta almeno un problema poiché la complessità di una sequenza non risulta in generale computabile (solo in alcuni casi).

Questo significa in parole povere che, come non si riesce a dimostrare in modo diretto che qualcosa è impossibile, così non possiamo mai sapere con certezza se esiste un modo di “comprimere” una sequenza che riteniamo essere casuale. Nel momento in cui qualcuno scoprisse il modo di comprimerla, tale sequenza cesserebbe di esserlo.

La questione ebbe origine con Claude Elwood Shannon padre della [teoria matematica dell’informazione](https://web.archive.org/web/20180329003105/http://math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), che pensò di misurar quest'ultima come entropia negativa, ovvero l’opposto della casualità. In breve una sequenza di segni casuale è caratterizzata da un alto livello di entropia, mentre un messaggio contenente informazione presenta un basso livello di entropia.

<figure><a href="/images/ClaudeShannon_MFO3807.jpg"><img src="/images/ClaudeShannon_MFO3807.jpg" alt="" loading="lazy"></a><figcaption><a href="https://it.wikipedia.org/wiki/Claude_Shannon">Claude Elwood Shannon</a></figcaption></figure>

Per mostrare concretamente questo approccio egli descrisse un semplice esperimento in cui si costruiscono delle sequenze di caratteri scelti in modo casuale dalle 26 lettere dell’alfabeto più lo spazio. le sequenze vengono costruite però con dei gradi crescenti di approssimazione alla lingua inglese.

Nella prima sequenza, di grado zero, ogni carattere ha uguale probabilità. Nella seconda sequenza, di grado uno, si utilizza la frequenza con cui un carattere segue il precedente nella lingua inglese. Nella sequenza di grado tre un carattere rispetta la frequenza con cui segue i due precedenti, mentre in quella di grado quattro dei tre precedenti.

Si può riprodurre l’esperimento aprendo a caso un libro (usato come campionatura casuale) e scorrendo fino a trovare la coppia o la terna dei caratteri precedenti, osservando quindi quello che li segue nel libro e aggiungendolo alla nostra sequenza.

Nella sequenza di grado cinque Shannon per semplificare applica lo stesso metodo alle parole invece che ai caratteri. Il risultato è il seguente.

Ordine zero di approssimazione per caratteri: XFOML RXKHRJFFJUJ ZLPWCFWKCYJ FFJEYVKCQSGHYD QPAAMKBZAACIBZLHJQD

Primo ordine di approssimazione per caratteri: OCR0 HLI RGWR NMIELWIS EU LL NBNESEBYA TH EEI ALHENH’ITPA OOBTTVA NAH BRL

Secondo ordine di approssimazione per caratteri: ON IE ANTSOUTINYS ARE T INCTORE ST BE S DEAMY ACHIN D ILONASIVE TUCOOWE AT TEASONARE FUSO TIZIN ANDY TOBE SEACE CTISBE

Terzo ordine di approssimazione per caratteri: IN NO IST LAT WHEY CRATICT FROURE BIRS GROCID PONDENOME OF DEMONSTURES OF THE REPTAGIN IS REGOACTIONA OF CRE

Primo ordine di approssimazione per parole: REPRESENTING AND SPEEDILY IS AN GOOD APT OR COME CAN DIFFERENT NATURAL HERE HE THE A IN CAME THE TO OF TO EXPERT GRAY COME TO FURNISHES THE LINE MESSAGE HAD BE THESE.

Secondo ordine di approssimazione per parole: THE HEAD AND IN FRONTAL ATTACK ON AN ENGLISH WRITER THAT THE CHARACTER OF THIS POINT IS THEREFORE ANOTHER METHOD FOR THE LETTERS THAT THE TIME OF WHO EVER TOLD THE PROBLEM FOR AN UNEXPECTED

Shannon fa notare come una sequenza di quattro o più parole successive estratte dall’ultimo risultato ottenuto potrebbe tranquillamente far parte di una frase senza alcuna stranezza.

> The particular sequence of ten words “attack on an English writer that the character of this” is not at all unreasonable. It appears then that a sufficiently complex stochastic process will give a satisfactory representation of a discrete source.

Poco dopo aggiunge:

> It would be interesting if further approximations could be constructed, but the labor involved becomes enormous at the next stage.

Oggi molti avranno notato che la tastiera di uno smartphone ci suggerisce le parole successive basandosi su una misura statistica di questo genere, per cui procedere a dei livelli di approssimazioni successivi sarebbe molto facile, grazie proprio ai progressi che anche queste idee di Shannon ci hanno fatto compiere in ambito tecnologico.

Ho sempre avuto questo dubbio: la misura dell’entropia (del disordine) forse coglie solo l’assenza di regole fonetiche, grammaticali e sintattiche, senza sfiorare l’aspetto più sottile del senso. E ancora: la poesia generata da un algoritmo è poesia?

La crittografia introduce in questo problema un ulteriore elemento di riflessione. Dato un messaggio, è possibile con un algoritmo crittografico trasformarlo in una sequenza di caratteri incomprensibile, e quindi apparentemente non distinguibile da una sequenza quasi casuale.

Certo, potrà essere una distribuzione non equiprobabile dei segni, ma sarà una situazione analoga a quella degli ordini di approssimazione esemplificati precedentemente. Quindi paradossalmente data una sequenza apparentemente casuale di segni, non possiamo escludere a priori che esistano un algoritmo e una chiave di decifratura che la trasformino in un messaggio di senso compiuto.

La conclusione che si può trarre è che un messaggio contenente informazione si differenzia da una sequenza casuale solo se esiste un destinatario in grado di estrarne un senso, cioè di decifrarlo. Messaggi in una lingua o codice che non conosco mi appaiono invece come rumore per mia incapacità. Questa posizione sembra oltretutto in linea con le idee di Bruno De Finetti che (diversamente da Kolmogorov) dava alla probabilità un significato soggettivo invece che oggettivo.

In definitiva con l’entropia dell’informazione sembra che possiamo solo misurare la nostra incapacità di leggere un ordine nelle cose. Ma questo non ci può mai garantire che un ordine, sebbene celato ai nostri occhi, esista.

Questa preziosa incertezza è ciò che rende affascinante il lavoro di interpretazione di qualunque testo: che si tratti del grande libro della natura, cui si accostò Galileo seguito da tutti gli scienziati, o della Bibbia su cui rabbini ed esegeti continuano a ragionare. Ogni interpretazione è ricerca e costruzione di un senso plausibile.

Tuttavia il senso di un testo appartiene ad un altro ordine di questioni. Bisogna rifarsi all’estetica Wabi-Sabi, alla mamma di Proust che passeggiando nel giardino spezzava un rametto per introdurre delle irregolarità intenzionali che lo rendessero “più naturale”.

Incalcolabile (frutto di un mio limite previsionale) o imponderabile (prodotto dalla libertà di Dio o dei viventi)?
