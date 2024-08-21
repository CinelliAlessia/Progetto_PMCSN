from math import log
from discrete_event_simulation.rng import random
from discrete_event_simulation.rngs import putSeed

def expovariate(rate):
    return -1 / rate * log(1 - random())


# Parametri della simulazione
TEMPO_SIMULAZIONE = 5 * 60  # 5 minuti in secondi
TASSO_ARRIVO = 1 / 60  # 1 job al minuto
TASSO_SERVIZIO = 1 / (3 * 60)  # 1 job ogni 3 minuti

# Liste per memorizzare i tempi di arrivo e di fine servizio
arrival_times = []
service_end_times = []

# Generazione dei tempi di arrivo e di fine servizio
putSeed(123456789)
tempo_corrente = 0
num_job = 0
with open('tempi_arrivo.txt', 'w') as file:
    while tempo_corrente < TEMPO_SIMULAZIONE:
        tempo_arrivo = expovariate(TASSO_ARRIVO)
        tempo_corrente += tempo_arrivo
        if tempo_corrente < TEMPO_SIMULAZIONE:
            file.write(f'{tempo_arrivo:.2f}\n')
            num_job += 1


# Prendi tutti i tempi di arrivo e calcola i tempi di fine servizio
tempo_corrente = 0
with open('tempi_servizio.txt', 'w') as file:
    for tempo_arrivo in range(num_job):
        tempo_servizio = expovariate(TASSO_SERVIZIO)
        file.write(f'{tempo_servizio:.2f}\n')

i = 0
# Confronto dei tempi di arrivo e di fine servizio
with open('tempi.txt', 'w') as file:
    for i in range(num_job):
        if i < len(service_end_times):
            file.write(f'Job {i+1}: Arrivo = {arrival_times[i]:.2f}, Fine Servizio = {service_end_times[i]:.2f}\n')
        else:
            file.write(f'Job {i+1}: Arrivo = {arrival_times[i]:.2f}, Fine Servizio = Non Servito\n')