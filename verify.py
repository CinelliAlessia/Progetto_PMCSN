import math
from Costant import *

def calcola_P0(rho, k):
    # Calcola la somma
    somma = 0
    for i in range(k):
        somma += ((k * rho) ** i) / math.factorial(i)
    somma += ((k * rho) ** k) / (math.factorial(k) * (1 - rho))
    # Calcola P(0)
    P0 = 1 / somma
    return P0


def calcola_Pq(rho, k):
    # Calcola P(0) usando la funzione esistente
    P0 = calcola_P0(rho, k)

    # Calcola il numeratore di P_q
    P_q = ((k * rho) ** k) / (math.factorial(k) * (1 - rho))
    return P_q * P0


def calcola_ETQi(rho_all, Pq_all, c, k, mu):

    # Calcola E(S)
    E_S = 1 / (k * mu)

    # Calcola il numeratore e il denominatore
    numeratore = (Pq_all[c-1] * E_S )#for i in range(c))

    denominatore_1 = 1 - sum(rho_all[i] for i in range(c-1))
    denominatore_2 = 1 - sum(rho_all[i] for i in range(c))

    # Calcola E[T_q^i]
    E_T_q_i = numeratore / (denominatore_1 * denominatore_2)

    return E_T_q_i


def multi_server():
    l1 = (P_OC_ON * P_ON * LAMBDA) #0.06
    l2 = (P_OC * P_DIFF * (1 - P_ON) * LAMBDA)#0.045
    l3 = (P_OC * (1 - P_DIFF) * (1 - P_ON) * LAMBDA)#0.255

    m = len(MULTI_SERVER_INDEX)
    mu = MU_OC
    es = 1 / (m * mu)

    l_tot = l1 + l2 + l3

    p1 = l1 / l_tot
    p2 = l2 / l_tot
    p3 = l3 / l_tot

    rho = l_tot * es

    rho1 = p1 * rho
    rho2 = p2 * rho
    rho3 = p3 * rho

    rho_all = [rho1, rho2, rho3]

    Pq1 = calcola_Pq(rho1, m)   # 0.0013067154886266313
    Pq2 = calcola_Pq(rho2+rho1, m)   # 0.013858646340606243
    Pq3 = calcola_Pq(rho3+rho2+rho1, m)   # 0.8448017130511031

    Pq_all = [Pq1, Pq2, Pq3]

    e_tq1 = calcola_ETQi(rho_all, Pq_all, 1, m, mu)
    e_tq2 = calcola_ETQi(rho_all, Pq_all, 2, m, mu)
    e_tq3 = calcola_ETQi(rho_all, Pq_all, 3, m, mu)

    return e_tq1, e_tq2, e_tq3


# ATM
def single_server_abstr_priority_ATM():
    l1 = (P_ATM * P_DIFF * (1 - P_ON) * LAMBDA)
    l2 = (P_ATM * (1 - P_DIFF) * (1 - P_ON) * LAMBDA)

    lambda_tot = l1 + l2

    m = len(ATM_SERVER_INDEX)
    mu = MU_ATM
    es = 1 / mu

    es_quadro = 2 / (mu ** 2)

    rho = lambda_tot * es

    p1 = l1 / lambda_tot
    p2 = l2 / lambda_tot

    rho1 = p1 * rho
    rho2 = p2 * rho
    rho_all = [rho1, rho2]

    numeratore = ((lambda_tot/2)*es_quadro)

    uno_meno_rho1 = 1 - rho1
    uno_meno_rho2 = 1 - rho2
    uno_meno_rho = 1 - rho

    e_tq1 = numeratore / uno_meno_rho1
    e_tq2 = numeratore / (uno_meno_rho1 * uno_meno_rho)

    return e_tq1, e_tq2


def single_server_abstr_priority_SER():
    l1 = (P_SR_ON * P_ON * LAMBDA)
    l2 = (P_SR * P_DIFF * (1 - P_ON) * LAMBDA)
    l3 = (P_SR * (1 - P_DIFF) * (1 - P_ON) * LAMBDA)

    lambda_tot = l1 + l2 + l3

    m = len(SR_SERVER_INDEX)
    mu = MU_SR
    es = 1 / mu

    es_quadro = 2 / (mu ** 2)

    rho = lambda_tot * es

    p1 = l1 / lambda_tot
    p2 = l2 / lambda_tot
    p3 = l3 / lambda_tot

    rho1 = p1 * rho
    rho2 = p2 * rho
    rho3 = p3 * rho
    rho_all = [rho1, rho2, rho3]

    numeratore = ((lambda_tot/2)*es_quadro)

    uno_meno_rho1 = 1 - rho1
    uno_meno_rho2 = 1 - rho1 - rho2
    uno_meno_rho = 1 - rho

    e_tq1 = numeratore / uno_meno_rho1
    e_tq2 = numeratore / (uno_meno_rho1 * uno_meno_rho2)
    e_tq3 = numeratore / (uno_meno_rho2 * uno_meno_rho)


    return e_tq1, e_tq2, e_tq3

print("Multi Server")
print(multi_server())
print("Spedizioni e Ritiri")
print(single_server_abstr_priority_SER())
print("ATM")
print(single_server_abstr_priority_ATM())

