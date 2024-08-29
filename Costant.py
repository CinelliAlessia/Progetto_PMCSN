# Prelievi e Versamenti -> 45% di probabilità
    # Sportello -> 45% di probabilità
    # ATM -> 55% di probabilità
# Operazione Unica -> 40% di probabilità
# Spedizione e Ritiri -> 15% di probabilità

# Prenotazioni Online
# Migliorativo - Locker pacchi, a fronte di una spesa iniziale (Pacchi grandi NO)


# Parametri della simulazione
SEED = 123456789
CLOSE_THE_DOOR_TIME = 8 * 60  # 8 ore
SIMULATION_JOB_NUM = 1000

# -------------------- Indici dei serventi --------------------

MULTI_SERVER_INDEX = [0, 1, 2, 3, 4, 5]
SR_SERVER_INDEX = [6]
ATM_SERVER_INDEX = [7]
# Numero di serventi TOTALI -> 6 sportelli + Sportello Spedizione e Ritiri + 1 ATM
SERVER_NUM = len(MULTI_SERVER_INDEX) + len(SR_SERVER_INDEX) + len(ATM_SERVER_INDEX)


# -------------------- Indici delle code associate ai serventi --------------------
MULTI_SERVER_QUEUES = [0, 1, 2]  # Indici delle code servite dal multiserver
SR_SERVER_QUEUES = [3, 4, 5]  # Indici delle code servite dal server Spedizioni e ritiri
ATM_SERVER_QUEUES = [6, 7]  # Indici delle code servite dal server ATM
QUEUES_NUM = len(MULTI_SERVER_QUEUES) + len(SR_SERVER_QUEUES) + len(ATM_SERVER_QUEUES)  # Numero di code TOTALI


#  Priorità (Multi server)
# La coda # 1 è per le prenotazioni online OC
# La coda # 2 è per le persone in difficoltà OC
# La coda # 3 è per le persone OC

#  Priorità (Single server)
# La coda # 4 è per Spedizione e Ritiri online
# La coda # 5 è per Spedizione e Ritiri in difficoltà
# La coda # 6 è per Spedizione e Ritiri

#  Priorità (Single server)
# La coda # 7 è per il Bancomat in difficoltà
# La coda # 8 è per il Bancomat

# -------------------- Tempi di Arrivo --------------------

LAMBDA = 1 / 1.5    # Tempo di interarrivo medio 1.5 minuti
LAMBDA_ON = 1 / 15  # Tempo di interarrivo medio 15 minuti prenotazioni Online

# -------------------- Tempi di Servizio --------------------

MU_OC = 1 / 13     # Tempo di servizio medio 13 minuti PV Sportello
MU_SR = 1 / 6       # Tempo di servizio medio 6 minuti
MU_ATM = 1 / 2     # Tempo di servizio medio 2 minuti PV ATM

# -------------------- Stream Index --------------------

CLASSIC_ONLINE_STREAM = 0
CLASSIC_DIFF_STREAM = 1
CLASSIC_STREAM = 2

SR_ONLINE_STREAM = 3
SR_STREAM = 5
SR_DIFF_STREAM = 4

ATM_DIFF_STREAM = 6
ATM_STREAM = 7

CLASSIC_SERVICE_STREAM = 8
SR_SERVICE_STREAM = 9
ATM_SERVICE_STREAM = 10

# -------------------- Probabilità --------------------

P_DIFF = 0.15  # Probabilità di persona in difficoltà

# Probabilità di scelta dell'operazione
P_OC = 0.5      # Probabilità di Operazione Classica
P_ATM = 0.35    # Probabilità di ATM
P_SR = 0.15     # Probabilità di Spedizione e Ritiri

# Probabilità di scelta dell'operazione online
P_OC_ON = 0.65  # Probabilità di Operazione Classica online
P_SR_ON = 0.35  # Probabilità di Spedizione e Ritiri online

P_MAX_LOSS = 0.8    # Probabilità di perdita massima
MAX_PEAPLE = 100    # Num. di persone per cui si ha p_loss max

# -------------------- Frequenza di campionamento --------------------
SAMPLING_TYPE = 0   # Tipo di campionamento (0: min, 1: job)
SAMPLING_RATE_MIN = 20  # Frequenza di campionamento per minuti
SAMPLING_RATE_JOB = 20  # Frequenza di campionamento per job
