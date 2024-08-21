from libs.rngs import putSeed, getSeed, plantSeeds, selectStream
from libs.rvgs import Exponential


# Parametri della simulazione
TEMPO_SIMULAZIONE = 8 * 60  # 8 ore
TASSO_ARRIVO = 0.5   # 0.5 job al minuto
TASSO_SERVIZIO = 1 / 9   # 1 job ogni 9 minuti


def service_time(num_job):
    # Prendi tutti i tempi di arrivo e calcola i tempi di fine servizio
    tempo_corrente = 0

    with open('tempi_arrivo.txt', 'r', newline="") as file_arrivi:
        file_arrivi.seek(0)
        with open('tempi_servizio.txt', 'w') as file:
            for i in range(num_job):
                tempo_servizio = Exponential(1/TASSO_SERVIZIO)
                # somma alla riga i esima del file_arrivi
                tempo_corrente += tempo_servizio + float(file_arrivi.readline())
                print(f'{tempo_corrente:.2f}')
                file.write(f'{tempo_corrente:.2f}\n')


def arrival_time():
    file_arrivi = open('tempi_arrivo.txt', 'w')
    tempo_corrente = 0
    while tempo_corrente < TEMPO_SIMULAZIONE:
        tempo_arrivo = Exponential(1/TASSO_ARRIVO)
        tempo_corrente += tempo_arrivo
        if tempo_corrente < TEMPO_SIMULAZIONE:
            file_arrivi.write(f'{tempo_corrente:.2f}\n')
    file_arrivi.close()


def count_jobs():
    with open('tempi_arrivo.txt', 'r', newline="") as file:
        return len(file.readlines())


# Generazione dei tempi di arrivo e di fine servizio
plantSeeds(123456789)
selectStream(0)
arrival_time()

num_job = count_jobs()

selectStream(1)
service_time(num_job)
