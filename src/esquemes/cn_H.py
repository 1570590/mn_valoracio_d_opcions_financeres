"""
Esquema de Crank Nicolson per l'equacio H
"""
import numpy as np


def esquema_crank_nicolson_H(
    M: int,
    N: int,
    x_min: float,
    x_max: float,
    T: float,
    sigma: float,
    r: float,
    opcio: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Resol l'EDP (3.9) usant l'esquema de Crank-Nicolson (4.2) amb condicions
    de frontera i inicials per una opció call o put.

    Aquesta funció resol l'equació diferencial parcial per a una opció
    financera utilitzant el mètode de Crank-Nicolson en un domini espacial
    i temporal discretitzat.

    Parameters
    ----------
    M : int
        Nombre de punts espacials (x) en el domini.
    N : int
        Nombre de passos temporals (tau).
    x_min : float
        Valor mínim del domini espacial.
    x_max : float
        Valor màxim del domini espacial.
    T : float
        Temps de maduració (opció asiàtica).
    sigma : float
        Volatilitat del subministrament.
    r : float
        Tipus d'interès lliure de risc.
    opcio : str
        Tipus d'opció, pot ser 'call' o 'put'.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        - x : np.ndarray
            Punts espacials.
        - tau : np.ndarray
            Punts temporals.
        - H : np.ndarray
            Matriu que conté la solució aproximada H(x, tau) per a cada
            punt en x i tau.
    """
    # Mida dels passos
    h = (x_max - x_min) / M
    k = ((sigma**2 * T) / 2) / N

    # Malla espacial i temporal
    x = np.linspace(x_min, x_max, M)
    tau_max = (sigma**2) / 2 * T
    tau = np.linspace(0, tau_max, N + 1)

    # Inicialitzem la matriu H[x, tau]
    H = np.zeros((M, N + 1))

    # Condicions inicials
    if opcio == "call":
        H[:, 0] = np.maximum(1 - np.exp(x), 0)
    elif opcio == "put":
        H[:, 0] = np.maximum(np.exp(x) - 1, 0)

    # Definim mu com el coeficient de la discretització temporal i espacial
    mu = k / (h**2)
    lamb = k / h

    # Construcció de les matrius A i B per a Crank-Nicolson
    A = np.zeros((M, M))
    B = np.zeros((M, M))

    # Construcció de les matrius A i B
    for m in range(1, M - 1):
        # Termes d'acord amb l'esquema de Crank-Nicolson
        A_m = (1 / (2 * sigma**2)) * (np.exp(-x[m]) / T - r - sigma**2 / 2)

        # Matriu A (coeficients implícits)
        A[m, m] = 1 + mu
        A[m, m - 1] = -mu / 2 + lamb * A_m
        A[m, m + 1] = -mu / 2 - lamb * A_m

        # Matriu B (coeficients explícits)
        B[m, m] = 1 - mu
        B[m, m - 1] = mu / 2 - lamb * A_m
        B[m, m + 1] = mu / 2 + lamb * A_m

    # Condicions de frontera
    A[0, 0], A[-1, -1] = 1, 1
    B[0, 0], B[-1, -1] = 1, 1

    # Resolució del sistema pas a pas
    for n in range(N):
        # Producte matriu-vector per H^n
        b = B @ H[:, n]

        # Condicions de frontera per al pas temporal
        b[0] = H[0, n]  # Condició de frontera per x -> -∞
        b[-1] = (
            0 if opcio == "call" else np.exp(x_max) - 1
        )  # Condició de frontera per x -> ∞

        # Resolució del sistema lineal
        H[:, n + 1] = np.linalg.solve(A, b)

    return x, tau, H
