import random

import matplotlib.pyplot as plt

from discrete_event_simulation.rngs import putSeed, random, getSeed
from discrete_event_simulation.ssq2 import GetArrival

RANDOM_SEED = 42
NUM_SPORTELLI_POSTALI = 3
NUM_SPORTELLI_FINANZIARI = 2
INTERVALLO_CLIENTI = 10  # Intervallo medio tra arrivi di clienti
TEMPO_SERVIZIO_POSTALE = 5  # Tempo medio di servizio per i servizi postali
TEMPO_SERVIZIO_FINANZIARIO = 15  # Tempo medio di servizio per i servizi finanziari


def prova_generatore():
    seed = 987654321
    putSeed(seed)
    x = [random()]  # Initialize x with the first random number
    x_coords = []
    y_coords = []

    for i in range(1, 400):  # Start from 1 since x already has one element
        x.append(random())  # Add new random number to x
        x_coords.append(x[i-1])
        y_coords.append(x[i])

    state_seed = getSeed()
    print(state_seed)

    # Crea il grafico a dispersione
    plt.scatter(x_coords, y_coords)
    plt.show()  # Don't forget to show the plot

    seed = 123456789
    putSeed(state_seed)

    x = [random()]  # Initialize x with the first random numberx = [random()]  # Initialize x with the first random number
    x_coords = []
    y_coords = []

    for i in range(1, 400):  # Start from 1 since x already has one element
        x.append(random())  # Add new random number to x
        x_coords.append(x[i-1])
        y_coords.append(x[i])

    #getSeed()
    # Crea il grafico a dispersione
    plt.scatter(x_coords, y_coords)
    plt.show()  # Don't forget to show the plot


def ssq_prova():
    tau = 5000
    l = 0
    t = 0.0
    tc = tau + 1
    ta = GetArrival()
    while(ta < tau) or l > 0:
        t = min(ta, tc)
        if t == ta:
            l += 1


prova_generatore()


def cliente(env, nome, sportelli_postali, sportelli_finanziari, tipo_servizio):
    arrivo = env.now
    print(f'{nome} arriva all\'ufficio postale alle {arrivo:.2f}')

    if tipo_servizio == 'postale':
        with sportelli_postali.request() as richiesta:
            yield richiesta
            inizio_servizio = env.now
            print(f'{nome} inizia il servizio postale alle {inizio_servizio:.2f}')
            yield env.timeout(random.expovariate(1.0 / TEMPO_SERVIZIO_POSTALE))
            print(f'{nome} termina il servizio postale alle {env.now:.2f}')
    elif tipo_servizio == 'finanziario':
        with sportelli_finanziari.request() as richiesta:
            yield richiesta
            inizio_servizio = env.now
            print(f'{nome} inizia il servizio finanziario alle {inizio_servizio:.2f}')
            yield env.timeout(random.expovariate(1.0 / TEMPO_SERVIZIO_FINANZIARIO))
            print(f'{nome} termina il servizio finanziario alle {env.now:.2f}')


def arrivo_clienti(env, sportelli_postali, sportelli_finanziari):
    i = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / INTERVALLO_CLIENTI))
        i += 1
        tipo_servizio = random.choice(['postale', 'finanziario'])
        env.process(cliente(env, f'Cliente {i}', sportelli_postali, sportelli_finanziari, tipo_servizio))


# Setup e avvio del processo di simulazione
#print('Simulazione Ufficio Postale')
#random.seed(RANDOM_SEED)
#env = simpy.Environment()

# Creazione delle risorse (sportelli)
#sportelli_postali = simpy.Resource(env, NUM_SPORTELLI_POSTALI)
#sportelli_finanziari = simpy.Resource(env, NUM_SPORTELLI_FINANZIARI)

# Avvio del processo di arrivo dei clienti
#env.process(arrivo_clienti(env, sportelli_postali, sportelli_finanziari))

# Esecuzione della simulazione
#env.run(until=100)
