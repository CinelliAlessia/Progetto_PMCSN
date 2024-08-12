from math import log

from discrete_event_simulation.rngs import putSeed, random

# Parametri della simulazione
TEMPO_SIMULAZIONE = 5 * 60  # 5 minuti in secondi
TASSO_ARRIVO = 1 / 60  # 1 job al secondo
TASSO_SERVIZIO = 1 / (3 * 60)  # 1 job ogni 3 minuti

# Liste per memorizzare i tempi di arrivo e di fine servizio
arrival_times = []
service_end_times = []

# Funzione per generare tempi esponenziali
def expovariate(rate):
    return -1 / rate * log(1 - random())


# Generazione dei tempi di arrivo e di fine servizio
putSeed(42)
tempo_corrente = 0
while tempo_corrente < TEMPO_SIMULAZIONE:
    tempo_arrivo = expovariate(TASSO_ARRIVO)
    tempo_corrente += tempo_arrivo
    if tempo_corrente < TEMPO_SIMULAZIONE:
        arrival_times.append(tempo_corrente)
        tempo_servizio = expovariate(TASSO_SERVIZIO)
        service_end_times.append(tempo_corrente + tempo_servizio)

# Confronto dei tempi di arrivo e di fine servizio
for i in range(len(arrival_times)):
    if i < len(service_end_times):
        print(f'Job {i+1}: Arrivo = {arrival_times[i]:.2f}, Fine Servizio = {service_end_times[i]:.2f}')
    else:
        print(f'Job {i+1}: Arrivo = {arrival_times[i]:.2f}, Fine Servizio = Non Servito')

# Scrittura dei tempi di arrivo e di fine servizio in un file
with open('tempi_servizio.txt', 'w') as file:
    for i in range(len(arrival_times)):
        if i < len(service_end_times):
            file.write(f'Job {i+1}: Arrivo = {arrival_times[i]:.2f}, Fine Servizio = {service_end_times[i]:.2f}\n')
        else:
            file.write(f'Job {i+1}: Arrivo = {arrival_times[i]:.2f}, Fine Servizio = Non Servito\n')