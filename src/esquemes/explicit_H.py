"""
Esquema explicit per l'equacio H
"""
import numpy as np

from src.logger import logger


def esquema_explicit_H(
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
    Resol l'EDP (3.9) usant l'esquema explícit (4.1) amb condicions de
    frontera i inicials per una opció call o put.

    Aquesta funció resol l'equació diferencial parcial per a una opció
    financera utilitzant el mètode explícit en un domini espacial i
    temporal discretitzat.

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
            Matriu que conté la solució aproximada H(x, tau)
            per a cada punt en x i tau.
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

    # Afegim les condicions inicials
    if opcio == "call":
        H[:, 0] = np.maximum(1 - np.exp(x), 0)
    elif opcio == "put":
        H[:, 0] = np.maximum(np.exp(x) - 1, 0)

    # Comprovem l'estabilitat de l'esquema, en cas que aquesta no se satisfaci,
    # forcem que l'esquema sigui estable
    min_k = float("inf")

    for m in range(M):
        A = np.exp(-x[m]) / T - r - (sigma**2 / 2)
        factor_estabilitat = A**2 * h**2
        if factor_estabilitat >= 1:
            # k<= 1/(2*A^2)
            max_k_m = 1 / (2 * A**2)
        else:
            # k<= h^2/2
            max_k_m = 0.5 * h**2

        if max_k_m < min_k:
            min_k = max_k_m

    if k > min_k:
        logger.log(
            f"El valor de k = {k} no satisfà les condicions d'estabilitat. "
            f"Ajustem a k = {min_k:.10f}.", "info"
        )
        k = min_k

    # Definim lambda i mu
    lamb = k / h
    mu = k / h**2

    # Escrivim l'esquema
    for n in range(N):
        for m in range(1, M - 1):
            A = (np.exp(-x[m]) / T) - r - (sigma**2 / 2)
            H[m, n + 1] = (
                (mu + (lamb / sigma**2) * A) * H[m + 1, n]
                + (1 - 2 * mu) * H[m, n]
                + (mu - (lamb / sigma**2) * A) * H[m - 1, n]
            )

        # Establim les condicions de frontera
        # Frontera en x -> - infty
        if opcio == "call":
            H[0, n + 1] = (
                H[0, n]
                + (2 / sigma**2) * k * (np.exp(-x[0]) / T) * (H[1, n] - H[0, n]) / h
            )
        elif opcio == "put":
            # H(x -> -infty, tau) = 0
            H[0, n + 1] = 0

        # Frontera en x -> infty
        if opcio == "call":
            # H(x -> infty, tau) = 0
            H[-1, n + 1] = 0
        elif opcio == "put":
            # H(x -> infty, tau) = infty, prenem el valor màxim
            H[-1, n + 1] = np.exp((-2 / sigma**2) * r * tau[n + 1] + x_max)

    return x, tau, H
