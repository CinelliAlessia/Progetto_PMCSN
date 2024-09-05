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
# ----------------------------------------------
# Prelievi e Versamenti -> 45% di probabilità
    # Sportello -> 45% di probabilità
    # ATM -> 55% di probabilità
# Operazione Unica -> 40% di probabilità
# Spedizione e Ritiri -> 15% di probabilità

# Prenotazioni Online
# Migliorativo - Locker pacchi, a fronte di una spesa iniziale (Pacchi grandi NO)


# Sportello spedizioni e ritiri -> Se non ci sono persone in coda, può servire tutti
# Locker per ritiri (+1 coda per il locker)

# -------------------- PARAMETRI DI CONFIGURAZIONE --------------------
VERBOSE = False
IMPROVED_SIM = False
LOCKER = False

#  -------------------- PARAMETRI DI SIMULAZIONE (dipendenti da parametri di configurazione) --------------------

# Indici dei serventi --------------------
MULTI_SERVER_INDEX = [0, 1, 2, 3, 4]
SR_SERVER_INDEX = [5]
ATM_SERVER_INDEX = [6]
LOCKER_SERVER_INDEX = [7]

#  Indici delle code associate ai serventi --------------------
MULTI_SERVER_QUEUES = [0, 1, 2]     # Indici delle code servite dal multiserver
SR_SERVER_QUEUES = [3, 4, 5]        # Indici delle code servite dal server Spedizioni e ritiri
ATM_SERVER_QUEUES = [6, 7]          # Indici delle code servite dal server ATM
LOCKER_SERVER_QUEUES = [8]

SERVER_NUM = len(MULTI_SERVER_INDEX) + len(SR_SERVER_INDEX) + len(ATM_SERVER_INDEX)
QUEUES_NUM = len(MULTI_SERVER_QUEUES) + len(SR_SERVER_QUEUES) + len(ATM_SERVER_QUEUES)  # Numero di code TOTALI

if IMPROVED_SIM and LOCKER:
    SERVER_NUM += len(LOCKER_SERVER_INDEX)
    QUEUES_NUM += len(LOCKER_SERVER_QUEUES)     # Numero di code TOTALI

# -------------------- Tempi di Arrivo --------------------

LAMBDA_G = 1 / 1.5     # Tempo di interarrivo medio 1.5 minuti (misurazione di 50 persone in 40 minuti -> 1 persona ogni 0.8 minuti)
LAMBDA_ON = 1 / 10      # Tempo di interarrivo medio 10 minuti prenotazioni Online

# CALCOLO DEL TEMPO DI ARRIVO
LAMBDA = LAMBDA_G + LAMBDA_ON
P_ON = LAMBDA_ON / LAMBDA

# -------------------- Tempi di Servizio --------------------
# Base campana: μ±3σ (99.7% dei valori)

MU_OC = 1 / 13      # Tempo di servizio medio 14 minuti PV Sportello
SIGMA_OC = 5 / 3    # Deviazione standard 5 minuti PV Sportello

MU_SR = 1 / 3       # Tempo di servizio medio 4.5 minuti
SIGMA_SR = 1.5 / 3  # Deviazione standard 2 minuti

MU_ATM = 1 / 2.5    # Tempo di servizio medio 2.5 minuti PV ATM
SIGMA_ATM = 1 / 3   # Deviazione standard 1 minuto PV ATM

MU_LOCKER = 1 / 1       # Tempo di servizio medio 1 minuto Locker
SIGMA_LOCKER = 0.25 / 3 # Deviazione standard 0.25 minuti Locker
# -------------------- Stream Index --------------------

# Stream Associati agli arrivi
CLASSIC_ONLINE_STREAM = 0
CLASSIC_DIFF_STREAM = 1
CLASSIC_STREAM = 2

SR_ONLINE_STREAM = 3
SR_STREAM = 5
SR_DIFF_STREAM = 4

ATM_DIFF_STREAM = 6
ATM_STREAM = 7

LOCKER_STREAM = 8

# Stream Associati ai servizi
CLASSIC_SERVICE_STREAM = 9  # I multi-server
SR_SERVICE_STREAM = 10      # Il server Spedizioni e Ritiri
ATM_SERVICE_STREAM = 11     # Lo sportello ATM

if IMPROVED_SIM:
    LOCKER_SERVICE_STREAM = 12  # Il locker

# -------------------- Probabilità --------------------

P_DIFF = 0.15  # Probabilità di persona in difficoltà

# Probabilità di scelta dell'operazione
P_OC = 0.45      # Probabilità di Operazione Classica
P_ATM = 0.35    # Probabilità di ATM
P_SR = 0.2     # Probabilità di Spedizione e Ritiri

# Probabilità di scelta dell'operazione online
P_OC_ON = 0.6  # Probabilità di Operazione Classica online
P_SR_ON = 0.4  # Probabilità di Spedizione e Ritiri online

P_MAX_LOSS = 0.8    # Probabilità di perdita massima
MAX_PEOPLE = 100    # Num. di persone per cui si ha p_loss max

P_LOCKER = 0.5      # Probabilità che una operazione di tipo spedizione e ritiri vada al locker

# -------------------- CSV FILE NAME --------------------
DIRECTORY_FINITE_H = "./finite_horizon/"
DIRECTORY_INFINITE_H = "./infinite_horizon/"

CSV_UTILIZATION = "utilization.csv"
CSV_DELAY = "delay.csv"       # Tempo di attesa in coda
CSV_WAITING_TIME = "waiting_time.csv"     # Tempo di risposta (Tempo di attesa + Tempo di servizio)

CSV_END_WORK_TIME_FINITE = "end_work_time_finite.csv"   # Tempo di fine lavoro

