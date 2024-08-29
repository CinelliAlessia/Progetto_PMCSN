# Progetto_PMCSN

## Descrizione
Il progetto consiste nell'analisi di un sistema reale con code: Ufficio Postale.

Appunti lez 22:
prima parte:
Obiettivo, va preso a prescindere da cosa sappiamo o meno fare.
Gli obiettivi vanno presi in maniera incondizionata. E sono di tipo:
Faccio questo? Si / No
Quanti servono per..? Numero

Conceptual Model: quali variabili di stato ho? Quali mi servono e quali sono inutili
Specification Model: I parametri, come avrà l'input, come sono fatti i dati, come li rappresento a distribuzioni di prob con caratteristiche simili
Computational Model: come faccio
Verification: il modello è corretto? Fa quello che deve fare? e' una verifica del software, bisogna capire se ci sono errori nel codice
Validation: Il modello è valido? Corrisponde al sistema vero? Sono partito dal modello giusto? Al massimo possiamo dire che non abbiamo modo di validarlo, ma deve comparire nella relazione
            Un esperto del sistema, può capire la differenza tra la realtà e quanto simulato.
            Se non abbiamo dati dobbiamo fare dei controlli di consistenza (es. se # tecnici >> -> # macchine guaste <<) 

Il modello deve essere i più semplice possibile, niente di inutile, scegliere il giusto livello di astrazione.

seconda parte:
Esperimenti: Quali valori cambiare? Per le esecuzioni significative, mantenere condizioni iniziali, statistiche(non tutti valori) di output e valori in input. 
Qualsiasi esperimento DEVE essere ripetibile.
Analisi dell'output: Richiede conoscenza statistica.
    Costruire campione in maniera corretta, per dare validità a quanto dedotto.
    Campione, dipende da che analisi sto facendo, transiente o stazionario.
Passare poi alle decisioni basate sui risultati.

appunti 23:
ATTENZIONE A CHIAMARE LE COSE IN MODO GIUSTO: ATTESA IN CODA => DELAY (di)

"Simulazione guidata da tracce" -> Si hanno dati reali 
"Simulazione guidata da distribuzioni" -> Se i dati non sono disponibili o se al variare dei dati come si comporta il sistema (Gen. numeri)
"Simulazione guidata da eventi" ->

Arrivi contemporanei con probabilità cosi bassa che li consideriamo impossibili. NO eventi simultanei. No bulk. 

fare dei test di consistenza sul modello computazionale, facciamo variare un parametro e vediamo se il sistema combia come è ovvio che cambi.
per intervallo di confidenza: tanti run indipendenti ma identicamente distribuiti.
"il throughput è questo blabla con livello di confidenza blabla"

statistiche (campionarie, di quel campione, non la media statistica) mediate sui job: 
tempo di interarrivo (media): somma di tutti gli interarrivi/num job
altre...

statistiche mediate sul tempo:

relazione tra le job averaged e le time: LITTLE
n/cn(ultimo compl) = x (throughput medio) o UTILIZZAZIONE
cn*x = busy time
n*s = busy time
intensità di traffico = (1/r)/(a/s)
quando cn/an = 1, intensità di traffico coincide con utilizzazione (succede quando simul lunga)
Arrivi contemporanei con probabilità cosi bassa che li consideriamo impossibili. NO eventi simultanei. No bulk.
appunti 24:

MAI UNIRE I PUNTINI.

appunti 25:
in alcuni casi esponenziale va bene per i servizi, quindi vedere bene.

appunti 26:
non prendere seeds a caso, perché non c'è garanzia di non sovrapposizione.
introduzione di eventi artificiali per campionare il sistema.
DOBBIAMO FARE ANALISI TRANSITORIO (mostrare come con vari seeds indipendenti ad es: tempo risposta tende allo stazionario
, credo la media teorica con circa 1000 jobs)
: non c'è bisogno su tutti gli indici (è idiota farlo sul tempo servizio o tempo interarrivo)
ha senso fare analisi transitorio sugli indici di prestazione (influenzati da quello che abbiamo fatto)
E STAZIONARIO (se la raggiunge, perché magari studiamo un periodo transitorio, basta dimostrare che per qualche seeds indipendente 
facciamo vedere che al crescere del numero job quell'indice sale)
Intervalli di confidenza! e non un punto insignificante.
Lei vuole vedere nel tempo come si comporta l'indice. es: throughput, tempo risp sale e poi scende ecc...

appunti 28:
dare il valore di infinito agli eventi impossibili se li troviamo
impostare condizione di fine simulazione: t arrival > t end and n = 0
una variabile unif tra 1 e 2, può essere espressa con 2 variabili uniformi tra 0 1.5, la loro somma ha ancora media 1.5, ma una varianza maggiore
questo ha un impatto sulle prestazioni del sistema, quindi non è indifferente -> è sempre una uniforme tra 1 e 2.
Possiamo cambiare il fatto che il sistema parte vuoto.

appunti 29:
campione di 1000 e passa elementi x1, x2 ecc.
utilizzare welford già implementato (uvs) che calcola la media campionaria fino al punto i (per varianza e dev std, senza memorizzare il campione)
per le statistiche sul tempo: non servono gli integrali perchè le funzioni sono stepwise, perciò facciamo solo le somme.
variate: variabili teoriche generate pseudo casualmente

appunti 30:
fare grafico : come vanno le prestazioni al passare del tempo o numero di job che arrivano (per vari seeds)
c'è il programma per fare istogrammi, variate discrete :ddh.py e variate continue :cdh.py
non ha alcun senso: calcolare intervallo confidenza dentro la simulazione, utilizzando come elementi del campione
le osservazioni singola(che non sono iid). Dobbiamo fare un unico grande run e dividerlo (vedremo poi come).
con welford possiamo calcolare media campionaria e dev std
programma estimate automatizza il calcolo degli intervalli di confidenza: n run e generare un campione indipendente:
inizializzando fuori dal ciclo, far andare i generatori nel ciclo cosi avrò lo stesso simulatore con lo stesso seed.
Generare campione ====> La nostra simulazione. Scegliamo intervallo di confidenza e usiamo estimate.py
il senso dell'intervallo di stima è che io sono capace di stimare quale sarà il vero valore(incognito) il 95% delle volte.
quale è questo n per avere la stima voluta? Lei dice che lo possiamo fare in modo semplice sostituendo t* dalla normale, perchè
cosi l'idf della students tende alla normale per n grande. -> possiamo dire che per n>40 si può usare il valore asintotico di t*
(ad esempio per 95%, esce t* = 1.96)
NON fare confidenza 99%. (alpha non deve essere prossimo allo 0)
n = parte inferiore (t* per s / w)^2 +1, dobbiamo andare molto oltre 40 a quanto pare. Dove w = t* per s / sqrt(n-1)
esempio sulle slide... Ancora pi facile, scelgo w 10% di s (non ho una stima affidabile di s), quindi s/w= 10, dalla formula di prima
n = 400 (run da fare).
Corretto dire: se creo abbastanza intervalli, il 95% di essi conterrà il valore vero della media teorica.
dobbiamo capire bene questa parte.

appunti 31:
per troncare le distribuzioni, stare attenti a come lo si fa, va normalizzato il tutto.
capire bene come sono fatte le distribuzioni utilizzata, parametri e grafici, relazioni tra varie distr
per il modello degli arrivi: nella magg gli arrivi sono random -> tempi inter-arrivi esponenziali (modello exp va bene)
se arrivi random -> il numero di arrivi è una poissoniana (modello poisson va bene, attenzione che la moda è 0)

per servizio: uniformi -> abbastanza no.
heavy tail -> vanno bene per tante cose

## Struttura
### Identificazione operazioni
1. Spedizione e Ritiro
2. 

## Librerie 
- rng.py include il random di Lehmer, putSeed, getSeed


- plantSeeds(x) prende un valore iniziale x e lo utilizza per inizializzare tutti i 256 stream di generatori di numeri casuali in modo coerente. Ogni stream successivo viene derivato dal seed del precedente, creando una serie di stream indipendenti ma deterministici. Questo è utile in applicazioni di simulazione o in altri contesti dove è importante avere sequenze di numeri casuali riproducibili su più stream indipendenti.
- Per cambiare lo stream utilizzato per la generazione di numeri casuali, utilizzi la funzione selectStream(index). Questa funzione seleziona lo stream specificato dall'indice index, che può variare da 0 a 255 (perché ci sono 256 stream disponibili).