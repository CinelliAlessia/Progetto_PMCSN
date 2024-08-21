from math import log
from discrete_event_simulation.rng import random
from discrete_event_simulation.rngs import putSeed

def expovariate(rate):
    return -1 / rate * log(1 - random())


# Parametri della simulazione
TEMPO_SIMULAZIONE = 5 * 60  # 5 minuti in secondi
TASSO_ARRIVO = 1 / 60  # 1 job al minuto
TASSO_SERVIZIO = 1 / (3 * 60)  # 1 job ogni 3 minuti

# Generazione dei tempi di arrivo e di fine servizio
putSeed(123456789)


def service_time(num_job):
    # Prendi tutti i tempi di arrivo e calcola i tempi di fine servizio
    tempo_corrente = 0

    with open('tempi_arrivo.txt', 'r', newline="") as file_arrivi:
        file_arrivi.seek(0)
        with open('tempi_servizio.txt', 'w') as file:
            for i in range(num_job):
                tempo_servizio = expovariate(TASSO_SERVIZIO)
                # somma alla riga i esima del file_arrivi
                tempo_corrente += tempo_servizio + float(file_arrivi.readline())
                print(f'{tempo_corrente:.2f}')
                file.write(f'{tempo_corrente:.2f}\n')


def arrival_time():
    file_arrivi = open('tempi_arrivo.txt', 'w')
    tempo_corrente = 0
    num_job = 0
    while tempo_corrente < TEMPO_SIMULAZIONE:
        tempo_arrivo = expovariate(TASSO_ARRIVO)
        tempo_corrente += tempo_arrivo
        if tempo_corrente < TEMPO_SIMULAZIONE:
            file_arrivi.write(f'{tempo_corrente:.2f}\n')
            num_job += 1
    file_arrivi.close()
    return num_job

num_job = arrival_time()
service_time(num_job)
