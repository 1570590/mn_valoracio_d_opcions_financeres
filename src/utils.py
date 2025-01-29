"""
utils
"""

import os
import yaml
import numpy as np
import pandas as pd

from typing import Tuple

from src.logger import logger


def interval_acotat(
    variable: np.ndarray, equacio: np.ndarray, min_val: float, max_val: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Retorna els intervals de valors acotats d'una variable i la seva equació
    corresponent.

    Aquesta funció troba els valors dins dels límits especificats
    (mínim i màxim) i retorna una secció de la variable i l'equació
    corresponent.

    Parameters
    ----------
    variable : np.ndarray
        Array que conté els valors de la variable a acotar.
    equacio : np.ndarray
        Array que conté els valors de l'equació evaluada corresponent.
    min_val : float
        Valor mínim per acotar.
    max_val : float
        Valor màxim per acotar.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        Tupla que conté els arrays acotats de la variable i l'equació.
    """
    # Trobem l'índex on la variable supera el valor mínim i màxim
    inici = np.searchsorted(variable, min_val, side="left")
    final = np.searchsorted(variable, max_val, side="right")

    return variable[inici:final], equacio[inici:final, :]


def desfer_canvi_variable_t(T: float, tau: float, sigma: float) -> float:
    """
    Calcula el valor de t després de desfer el canvi de variable temporal.

    Parameters
    ----------
    T : float
        Temps final.
    tau : float
        Pas de temps.
    sigma : float
        Volatilitat.

    Returns
    -------
    float
        Valor de t després de desfer el canvi de variable.
    """
    return T - (2 * tau / sigma**2)


def R_H(T: float, x: np.ndarray) -> np.ndarray:
    """
    Calcula la funció R per a l'equació H.

    Aquesta funció aplica la fórmula per calcular R en funció de T i x.

    Parameters
    ----------
    T : float
        Temps final.
    x : np.ndarray
        Array que conté els valors de la variable x.

    Returns
    -------
    np.ndarray
        Array que conté els resultats de R_H per als valors de x.
    """
    return np.exp(x) * T


def R_W(T: float, x: np.ndarray) -> np.ndarray:
    """
    Calcula la funció R per a l'equació W.

    Aquesta funció aplica la fórmula per calcular R en funció de T i x.

    Parameters
    ----------
    T : float
        Temps final.
    x : np.ndarray
        Array que conté els valors de la variable x.

    Returns
    -------
    np.ndarray
        Array que conté els resultats de R_W per als valors de x.
    """
    return np.exp(x) / T


def taula_H(
    x: np.ndarray, tau: np.ndarray, H: np.ndarray, filename: str = None
) -> pd.DataFrame:
    """
    Genera una taula amb els valors de H(x, tau) i la guarda en
    un fitxer CSV opcional.

    Aquesta funció crea un DataFrame amb les dades de H per a cada
    valor de x i tau. També permet guardar aquesta taula en un fitxer CSV
    si es proporciona un nom de fitxer.

    Parameters
    ----------
    x : np.ndarray
        Array que conté els valors de x.
    tau : np.ndarray
        Array que conté els valors de tau.
    H : np.ndarray
        Matriu de valors de H.
    filename : str, optional
        Nom del fitxer on es guardarà la taula en format CSV.
        Per defecte és None.

    Returns
    -------
    pd.DataFrame
        DataFrame que conté la taula amb els valors de H(x, tau).
    """
    dades = [(xi, t, H[i, j]) for j, t in enumerate(tau) for i, xi in enumerate(x)]

    # Creem un dataframe
    taula = pd.DataFrame(dades, columns=["x", "tau", "H(x, tau)"])

    # Guardar en un arxiu CSV
    if filename:
        taula.to_csv(filename, index=False)
        logger.log(f"Taula guardada en: {filename}", "info")

    return taula


def taula_W(
    x: np.ndarray, tau: np.ndarray, W: np.ndarray, filename: str = None
) -> pd.DataFrame:
    """
    Genera una taula amb els valors de W(x, tau) i la guarda en
    un fitxer CSV opcional.

    Aquesta funció crea un DataFrame amb les dades de W per a
    cada valor de x i tau. També permet guardar aquesta taula en
    un fitxer CSV si es proporciona un nom de fitxer.

    Parameters
    ----------
    x : np.ndarray
        Array que conté els valors de x.
    tau : np.ndarray
        Array que conté els valors de tau.
    W : np.ndarray
        Matriu de valors de W.
    filename : str, optional
        Nom del fitxer on es guardarà la taula en format CSV.
        Per defecte és None.

    Returns
    -------
    pd.DataFrame
        DataFrame que conté la taula amb els valors de W(x, tau).
    """
    dades = [(xi, t, W[i, j]) for j, t in enumerate(tau) for i, xi in enumerate(x)]

    # Creem un dataframe
    taula = pd.DataFrame(dades, columns=["x", "tau", "W(x, tau)"])

    # Guardar en un arxiu CSV
    if filename:
        taula.to_csv(filename, index=False)
        logger.log(f"Taula guardada en: {filename}", "info")

    return taula


def coeficientB(x: np.ndarray, sigma: float, r: float, T: float) -> np.ndarray:
    """
    Calcula el coeficient B per a l'equació.

    Aquesta funció aplica la fórmula per calcular el coeficient B en funció
    dels valors de x, sigma, r i T.

    Parameters
    ----------
    x : np.ndarray
        Array que conté els valors de x.
    sigma : float
        Volatilitat.
    r : float
        Taxa d'interès.
    T : float
        Temps final.

    Returns
    -------
    np.ndarray
        Array que conté els valors del coeficient B per a cada valor de x.
    """
    return (2 / (sigma**2)) * (r - np.exp(x) / T)


def carregar_configuracio(path: str) -> dict:
    """
    Carrega la configuració des d'un fitxer YAML.

    Aquesta funció llegeix el fitxer YAML especificat i retorna
    el contingut com un diccionari.

    Parameters
    ----------
    path : str
        Ruta del fitxer YAML que conté la configuració.

    Returns
    -------
    dict
        Diccionari amb la configuració carregada des del fitxer YAML.
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)


def path_grafic(esquema: str, equacio: str, nom_fitxer_2d: str) -> Tuple[str, str]:
    """
    Genera les rutes dels fitxers per guardar els gràfics, creant les carpetes
    necessàries si no existeixen.

    Paràmetres
    ----------
    esquema : str
        El nom de l'esquema (ex: "Crank-Nicolson", "Explicit").
    equacio : str
        El nom de l'equació (ex: "Black-Scholes", "Heat Equation").
    nom_fitxer_2d : str
        El nom del fitxer 2D a generar (ex: "grafico.png").

    Retorns
    -------
    Tuple[str, str]
        Una tupla amb la ruta de la carpeta i la ruta completa del fitxer 2D.
    """
    carpeta = os.path.join("..", "data", "grafics", esquema, equacio)

    # Creem la carpeta si no existeix
    os.makedirs(carpeta, exist_ok=True)

    # Ruta per al fitxer 2D
    ruta_fitxer_2d = os.path.join(carpeta, nom_fitxer_2d)

    return carpeta, ruta_fitxer_2d
