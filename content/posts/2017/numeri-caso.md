---
title: "Numeri a caso"
date: 2017-12-22T21:02:00+01:00
lastmod: 2017-12-22T21:13:34+01:00
url: /2017/12/numeri-caso.html
author: "Emanuele"
tags: ["Nuvole"]
---

Esiste [un libro](https://en.wikipedia.org/wiki/A_Million_Random_Digits_with_100,000_Normal_Deviates), di valore storico per alcuni [esperti](https://www.schneier.com/blog/archives/2006/10/a_million_rando.html) di crittografia, pubblicato per la prima volta nel 1955. Oggi è reperibile una ristampa e su Amazon si trovano più di 600 [commenti](https://www.amazon.com/product-reviews/0833030477) esilaranti dei lettori. A sfogliarlo sembra una cosa assurda, o l'invenzione di un racconto di Borges, poiché contiene un milione di numeri casuali: 400 pagine con 50 righe e per ogni riga 50 numeri (ognuno di 5 cifre).

<figure><a href="/images/numeri-caso-1.png"><img src="/images/numeri-caso-1.png" alt="" loading="lazy"></a><figcaption>Fonte: <a href="https://web.archive.org/web/20171223202538/https://www.wired.com/2012/08/st_randomnumbergenerators/">Wired</a></figcaption></figure>

Per quanto possa sembrare strano, non è così facile generare in modo meccanico lunghe sequenze di numeri casuali. Per capire questo paradosso basta considerare il fatto che un computer, come quasi ogni meccanismo costruito dall’uomo, è progettato solitamente per avere un comportamento rigidamente deterministico, secondo una logica, quindi prevedibile.

Un algoritmo deve produrre un risultato ben preciso a partire dallo stato iniziale, quindi in un certo senso si può dire che la casualità non è computabile per definizione. La conseguenza è che i computer anche oggi generano di solito, per semplicità, sequenze di numeri solo pseudo-casuali, cioè contenenti un errore sistematico, detto bias statistico.

Il sito dell'editore contiene una [pagina](https://www.rand.org/pubs/monograph_reports/MR1418/index2.html) che spiega in modo abbastanza chiaro le ragioni e le difficoltà incontrate a quei tempi nella realizzazione e pubblicazione di questo libro.

> Production from the original machine showed statistically significant biases, and the engineers had to make several modifications and refinements of the circuits before production of apparently satisfactory numbers was achieved. The basic table of a million digits was then produced during May and June of 1947. This table was subjected to fairly exhaustive tests and it was found that it still contained small but statistically significant biases.

Il problema è stato risolto anni dopo attingendo all'ambiente segnali e disturbi generati nel mondo fisico, usati come fonte di casualità attendibile. Esistono dei servizi gratuiti per tutta la comunità informatica, basati su questo metodo e offerti via internet. Quello di RANDOM.ORG, inizialmente realizzato presso il Trinity College di Dublino e oggi erogato da una azienda privata, impiega dei [ricevitori radio](https://www.random.org/faq/#Q1.4) per catturare il rumore atmosferico, che viene quindi usato per generare numeri casuali: in pratica le radio sono sintonizzate sulla posizione tra le stazioni, dove comunemente sentiamo un fruscio. Un servizio analogo è quello di [HotBits](https://www.fourmilab.ch/hotbits/) che si basa invece sul decadimento radioattivo.

<figure><a href="/images/numeri-caso-2.png"><img src="/images/numeri-caso-2.png" alt="" loading="lazy"></a><figcaption>Fonte: <a href="http://random.org/">Random.org</a></figcaption></figure>

Il libro contiene anche delle istruzioni esposte con il tipico linguaggio formale della scienza, ma curiosamente sembrano evocare quelle di un antico incantesimo.

> Use of the Tables  
> The lines of the digit table are numbered from 00000 to 19999. In any use of the table, one should first find a random starting position. A common procedure for doing this is to open the book to an unselected page of the digit table and blindly choose a five-digit number; this number with the first digit reduced modulo 2 determines the starting line; the two digits to the right of the initially selected five- digit number are reduced modulo 50 to determine the starting column in the starting line. To guard against the tendency of books to open repeatedly at the same page and the natural tendency of a person to choose a number toward the center of the page: every five-digit number used to determine a starting position should be marked and not used a second time for this purpose. \[...\]

Di fronte a questo libro alcuni pensieri si insinuano furtivi e insidiosi nella mia mente.

Dal giorno in cui è stato pubblicato quel libro, chi lo possiede è in grado di prevedere ogni cifra successiva a una sequenza sufficientemente lunga da esso estratta. Questo semplice fatto non rende, di per sé, le cifre di quel libro non più casuali?

Oppure, considerato che i numeri irrazionali sono infiniti, supponiamo che un matematico scopra l’esistenza di un numero irrazionale le cui prime 5\*10^6 cifre decimali siano esattamente quelle del libro. In tal caso quei numeri potrebbero essere ancora considerati casuali?

Supponiamo infine che un giorno un matematico dimostri essere vera la congettura seguente: data una qualsiasi sequenza di numeri ritenuta casuale, esiste almeno un numero irrazionale le cui prime cifre decimali replicano quella sequenza. Questa non sarebbe forse la dimostrazione matematica del fatto che [il caso non esiste](/2016/05/il-caso-non-esiste.html)?

<figure><a href="/images/numeri-caso-3.png"><img src="/images/numeri-caso-3.png" alt="" loading="lazy"></a><figcaption>Fonte: <a href="http://dilbert.com/strip/2001-10-25">Dilbert</a></figcaption></figure>
