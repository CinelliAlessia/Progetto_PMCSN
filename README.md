# Progetto_PMCSN

## Descrizione
Il progetto consiste nell'analisi di un sistema reale con code: Ufficio Postale.

## Struttura
### Identificazione operazioni
1. Spedizione e Ritiro
2. 

## Librerie 
- rng.py include il random di Lehmer, putSeed, getSeed


- plantSeeds(x) prende un valore iniziale x e lo utilizza per inizializzare tutti i 256 stream di generatori di numeri casuali in modo coerente. Ogni stream successivo viene derivato dal seed del precedente, creando una serie di stream indipendenti ma deterministici. Questo è utile in applicazioni di simulazione o in altri contesti dove è importante avere sequenze di numeri casuali riproducibili su più stream indipendenti.
- Per cambiare lo stream utilizzato per la generazione di numeri casuali, utilizzi la funzione selectStream(index). Questa funzione seleziona lo stream specificato dall'indice index, che può variare da 0 a 255 (perché ci sono 256 stream disponibili).