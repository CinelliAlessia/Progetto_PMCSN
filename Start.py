from Costant import *
from Simulation import start_simulation
from libs.rngs import *

NUM_RUN = 1

seed_used = [SEED]
for i in range(NUM_RUN):
    print("Simulation starting seed: ", getSeed())
    start_simulation(seed_used[-1])
    seed_used.append(getSeed())
    print("Simulation ending seed: ", getSeed())

# Steady-state statistics (stazionario) ----> Infinit horizon simulation
# Vista tradizionale: Sono più importanti perchè: più comprensibili
# Sono quelle statistiche, se esistono, che vengono prodotte simulando operazioni di un sistema stazionario per
# un periodo di tempo assimilabile all'infinito
# Una simulazione a orizzonte finito ad eventi discreti è tale per cui il tempo di simulazione è finito
# Una simulazione ad orizzonte infinito è tale per cui il tempo di simulazione è infinito

# Transient statistics (transitorio) -----> Finit horizon simulation
# Vista pragmatica: Sono più importanti perchè: più simili alla realtà
# Sono quelle statistiche che vengono prodotte simulando operazioni di un sistema per un periodo di tempo finito
# Le condizioni iniziali ovviamente influiscono sulle statistiche transitorie (uguale per tutti i run di simulazione)
#
#---------------- DISCORSO SU SLIDE senza titolo ---------------
# Se una simulazione ad eventi discreti è ripetuta, cambiando SOLO il seed iniziale del rngs, ogni sun viene chiamato:
# replication
# Tutte le replicazioni insieme sono chiamate ensemble
# Le replicazioni sono usate per generare ESTIMATES delle statistiche TRANSITORIE
# Utilizzare il seme finale di ogni replicazione come seme iniziale per la successiva replicazione



