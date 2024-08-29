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



"Simulazione guidata da tracce" -> Si hanno dati reali 
"Simulazione guidata da distribuzioni" -> Se i dati non sono disponibili o se al variare dei dati come si comporta il sistema (Gen. numeri)
"Simulazione guidata da eventi" ->

Arrivi contemporanei con probabilità cosi bassa che li consideriamo impossibili. NO eventi simultanei. No bulk. 

## Struttura
### Identificazione operazioni
1. Spedizione e Ritiro
2. 

## Librerie 
- rng.py include il random di Lehmer, putSeed, getSeed


- plantSeeds(x) prende un valore iniziale x e lo utilizza per inizializzare tutti i 256 stream di generatori di numeri casuali in modo coerente. Ogni stream successivo viene derivato dal seed del precedente, creando una serie di stream indipendenti ma deterministici. Questo è utile in applicazioni di simulazione o in altri contesti dove è importante avere sequenze di numeri casuali riproducibili su più stream indipendenti.
- Per cambiare lo stream utilizzato per la generazione di numeri casuali, utilizzi la funzione selectStream(index). Questa funzione seleziona lo stream specificato dall'indice index, che può variare da 0 a 255 (perché ci sono 256 stream disponibili).