import os
from Simulation import start_simulation
from libs.rngs import *
from Costant import *

# Parametri della simulazione
SEED = 123456789 #123456789 #1359796324 # 1161688905
seed_used = [SEED]  # Lista dei seed utilizzati per ogni replica della simulazione (Per ripetibilità)

# ---------------- INFINITE HORIZON SIMULATION ----------------
INFINITE_HORIZON = False
BATCH_DIM = 512  # Campionamento ogni 512 job (b)
BATCH_NUM = 1024  # Numero di batch da eseguire (k)
INFINITE_HORIZON_TIME = BATCH_DIM * BATCH_NUM

# ---------------- FINITE HORIZON SIMULATION ----------------
FINITE_HORIZON = not INFINITE_HORIZON  # Se non è una simulazione a orizzonte finito allora è a orizzonte infinito
FINITE_HORIZON_TIME = 4 * 60  # 4 ore di simulazione
REPLICATION_NUM = 1
SAMPLING_RATE = 1  # Tempo di campionamento per le statistiche


def finite_horizon_run():
    CLOSE_THE_DOOR_TIME = FINITE_HORIZON_TIME

    # Inizializzazione file csv per le statistiche (Crea il file se non esiste o cancella contenuto se esiste)
    directory = DIRECTORY_FINITE_H
    files = [CSV_UTILIZATION, CSV_DELAY, CSV_WAITING_TIME, CSV_END_WORK_TIME_FINITE]

    # Cancella il contenuto del file
    for file in files:
        with open(os.path.join(directory, file), 'w') as f:
            f.write('')

    plantSeeds(SEED)
    # Esecuzione delle repliche
    for ri in range(REPLICATION_NUM):
        print("Starting replica for finite-horizon simulation, seed: ", getSeed())
        #plantSeeds(getSeed())
        start_simulation(CLOSE_THE_DOOR_TIME, "finite", SAMPLING_RATE)
        selectStream(0)
        seed_used.append(getSeed())
        print(f"Simulation {ri + 1}/{REPLICATION_NUM} ending seed: {getSeed()}")
    print("fine simulazione")
    for s in seed_used:
        print(s)


def infinite_horizon_run():
    print("Starting infinite horizon simulation, seed: ", SEED)
    # CLOSE_THE_DOOR_TIME = INFINITE_HORIZON_TIME

    # Inizializzazione file csv per le statistiche (Crea il file se non esiste o cancella contenuto se esiste)
    directory = DIRECTORY_INFINITE_H
    files = [CSV_UTILIZATION, CSV_DELAY, CSV_WAITING_TIME]

    # Cancella il contenuto del file
    for file in files:
        with open(os.path.join(directory, file), 'w') as f:
            f.write('')

    # Esecuzione della simulazione
    start_simulation(float('inf'), "infinite", BATCH_DIM, BATCH_NUM)
    seed_used.append(getSeed())
    print("Simulation ending seed: ", getSeed())


def main():
    # Inizializza il generatore di numeri casuali
    plantSeeds(SEED)

    if INFINITE_HORIZON:
        infinite_horizon_run()

    elif FINITE_HORIZON:
        finite_horizon_run()
    else:
        raise ValueError("Errore: Nessun orizzonte di simulazione selezionato")


main()

# Steady-state statistics (stazionario) ----> Infinite horizon simulation
# Vista tradizionale: Sono più importanti perché: più comprensibili
# Sono quelle statistiche, se esistono, che vengono prodotte simulando operazioni di un sistema stazionario per
# un periodo di tempo assimilabile all'infinito
# Una simulazione a orizzonte finito ad eventi discreti è tale per cui il tempo di simulazione è finito
# Una simulazione ad orizzonte infinito è tale per cui il tempo di simulazione è infinito
# Per steady state bisogna ottenere POINT ESTIMATES simulando per un tempo infinito
# Come otteniamo intervalli di stima per le statistiche stazionarie? -> Con BATCH MEANS

# ----------------------------------------------------------------------------------------------

# Transient statistics (transitorio) -----> Finite horizon simulation
# Vista pragmatica: Sono più importanti perché: più simili alla realtà
# Sono quelle statistiche che vengono prodotte simulando operazioni di un sistema per un periodo di tempo finito
# Le condizioni iniziali ovviamente influiscono sulle statistiche transitorie (uguale per tutti i run di simulazione)
# ---------- Altra roba per transient statistics: ----------
# Se una simulazione ad eventi discreti è ripetuta, cambiando SOLO il seed iniziale del rngs, ogni sun viene chiamato:
# replication (1000 job per simulazione sembrano andare bene per raggiungere STEADY STATE -> Stazionarietà)
# Tutte le replicazioni insieme sono chiamate ensemble
# Le replicazioni sono usate per generare ESTIMATES delle statistiche TRANSITORIE
# Utilizzare il seme finale di ogni replicazione come seme iniziale per la successiva replicazione

# ------------------------------- Confronto delle stime ----------------------------------------
# Possono le stime transitorie essere usate per fare inferenze sulle stime stazionarie?
# Potrebbero se il numero di job non è piccolo



