from discrete_event_simulation.rngs import putSeed
from discrete_event_simulation.ssq4 import Exponential

# Parametri della simulazione
TEMPO_SIMULAZIONE = 5 * 60  # 5 minuti in secondi
TASSO_ARRIVO = 1 / 60  # 1 job al minuto
TASSO_SERVIZIO = 1 / (3 * 60)  # 1 job ogni 3 minuti

# Liste per memorizzare i tempi di arrivo e di fine servizio
arrival_times = []
service_end_times = []

# Generazione dei tempi di arrivo e di fine servizio
putSeed(42)
tempo_corrente = 0
while tempo_corrente < TEMPO_SIMULAZIONE:
    tempo_arrivo = Exponential(TASSO_ARRIVO)
    tempo_corrente += tempo_arrivo
    if tempo_corrente < TEMPO_SIMULAZIONE:
        arrival_times.append(tempo_corrente)

# Prendi tutti i tempi di arrivo e calcola i tempi di fine servizio
tempo_corrente = 0
for tempo_arrivo in arrival_times:
    tempo_servizio = Exponential(TASSO_SERVIZIO)
    tempo_corrente = max(tempo_arrivo, tempo_corrente) + tempo_servizio
    service_end_times.append(tempo_corrente)

# Confronto dei tempi di arrivo e di fine servizio
with open('tempi_servizio.txt', 'w') as file:
    for i in range(len(arrival_times)):
        if i < len(service_end_times):
            file.write(f'Job {i+1}: Arrivo = {arrival_times[i]:.2f}, Fine Servizio = {service_end_times[i]:.2f}\n')
        else:
            file.write(f'Job {i+1}: Arrivo = {arrival_times[i]:.2f}, Fine Servizio = Non Servito\n')