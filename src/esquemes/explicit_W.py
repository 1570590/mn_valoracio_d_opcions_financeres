"""
Esquema de explicit per l'equacio W
"""
import numpy as np

from src.logger import logger


def esquema_explicit_W(
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
    Resol l'EDP (3.11) usant l'esquema explícit (4.3) amb condicions de
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
        - W : np.ndarray
            Matriu que conté la solució aproximada W(x, tau)
            per a cada punt en x i tau.
    """
    # Mida dels passos
    h = (x_max - x_min) / M
    k = (sigma**2 * T / 2) / N
    logger.log(f"k = {k:.16f}, h={h:.16f}", "info")

    # Condicions d'estabilitat
    x = np.linspace(x_min, x_max, M)
    B = np.array([(1 / sigma**2) * (r - np.exp(x_m) / T) for x_m in x])
    diff_max = np.max(np.abs(B - 1))

    # h * |B-1| <= 2
    if h * diff_max > 2:
        h = 2 / diff_max
        # Tornem a calcular M
        M = int(np.ceil((x_max - x_min) / h)) + 1
        h = (x_max - x_min) / (M - 1)
        logger.log(
            f"Ajustem h per tal que sigui estable: nou h = {h:.16f}, nou M = {M}",
            "info"
        )

    # k/h^2 <= 1/2
    if k / (h**2) > 0.5:
        k = 0.5 * h**2
        N = int(np.ceil(T / k))  # Tornem a calcular N
        k = ((sigma**2 * T) / 2) / N
        logger.log(
            f"Ajustem k per tal que sigui estable: nou k = {k:.16f}, nou N = {N}",
            "info"
        )

    # Malla espacial i temporal
    x = np.linspace(x_min, x_max, M)
    tau_max = (sigma**2) / 2 * T
    tau = np.linspace(0, tau_max, N + 1)

    # Inicialitzem la matriu W[x, tau]
    W = np.zeros((M, N + 1))

    # Afegim les condicions inicials
    if opcio == "call":
        W[:, 0] = np.maximum(np.exp(x) - 1, 0)
    elif opcio == "put":
        W[:, 0] = np.maximum(1 - np.exp(x), 0)

    # Definim lambda i mu
    lamb = k / h
    mu = k / (h**2)

    # Escrivim l'esquema
    for n in range(N):
        for m in range(1, M - 1):
            B = (2 / sigma**2) * (r - np.exp(x[m]) / T)
            W[m, n + 1] = (
                (mu + lamb / 2 * (B - 1)) * W[m + 1, n]
                + (1 - 2 * mu - (B * k)) * W[m, n]
                + (mu - lamb / 2 * (B - 1)) * W[m - 1, n]
            )

        # Frontera en x -> - infty
        if opcio == "call":
            # W(x, tau) = 0
            W[0, n + 1] = 0
        elif opcio == "put":
            W[0, n + 1] = np.exp(-2 * r * tau[n + 1] / sigma**2) / T

        # Frontera en x -> infty
        if opcio == "call":
            # W(x, tau) ~ e^x/T
            W[-1, n + 1] = np.exp(x_max) / T
        elif opcio == "put":
            # W(x, tau) = 0
            W[-1, n + 1] = 0

    return x, tau, W
