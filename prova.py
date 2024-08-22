from Server import Server
from libs.rngs import putSeed, getSeed, plantSeeds, selectStream
from libs.rvgs import Exponential


# Parametri della simulazione
TEMPO_SIMULAZIONE = 8 * 60  # 8 ore
TASSO_ARRIVO = 0.25
TASSO_SERVIZIO = 0.75

def processing_job(num_job):
    server1 = Server(1)
    server2 = Server(2)

    file_arrivi = open('tempi_arrivo.txt', 'r', newline="")
    file_arrivi.seek(0)

    file_servizio = open('tempi_servizio.txt', 'r', newline="")
    file_servizio.seek(0)

    for i in range(num_job):
        tempo_arrivo = float(file_arrivi.readline())
        tempo_servizio = float(file_servizio.readline())

        if server1.get_current_time() <= tempo_arrivo:
            tempo_fine = server1.process_job(tempo_arrivo, tempo_servizio)
            print(f'Fine Servente 1: {tempo_fine:.2f}')
        elif server2.get_current_time() <= tempo_arrivo:
            tempo_fine = server2.process_job(tempo_arrivo, tempo_servizio)
            print(f'Fine Servente 2: {tempo_fine:.2f}')
        else:
            # Se entrambi i server sono occupati, si può decidere di attendere o gestire diversamente
            pass


def generate_arrival_time():
    file_arrivi = open('tempi_arrivo.txt', 'w')
    tempo_corrente = 0
    while tempo_corrente < TEMPO_SIMULAZIONE:
        tempo_arrivo = Exponential(1 / TASSO_ARRIVO)
        tempo_corrente += tempo_arrivo
        if tempo_corrente < TEMPO_SIMULAZIONE:
            file_arrivi.write(f'{tempo_corrente:.2f}\n')
    file_arrivi.close()


def count_jobs():
    with open('tempi_arrivo.txt', 'r', newline="") as file:
        file.seek(0)
        return len(file.readlines())


def generate_service_time():
    file_servizio = open('tempi_servizio.txt', 'w')
    num_job = count_jobs()
    for i in range(num_job):
        tempo_servizio = Exponential(1 / TASSO_SERVIZIO)
        file_servizio.write(f'{tempo_servizio:.2f}\n')
    file_servizio.close()



# Generazione dei tempi di arrivo e di fine servizio
plantSeeds(123456789)
selectStream(0)
generate_arrival_time()

selectStream(1)
generate_service_time()

processing_job(count_jobs())