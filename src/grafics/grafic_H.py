"""
Generació dels gràfics per l'equacio H
"""
import os

import matplotlib.pyplot as plt
import numpy as np

from src.utils import path_grafic


def grafic_H(
    x: np.ndarray,
    tau: np.ndarray,
    H: np.ndarray,
    opcio: str,
    esquema: str,
    nom_fitxer_3d: str,
    nom_fitxer_2d: str,
) -> None:
    """
    Funció per a crear i guardar el gràfic de la solució H(x, tau)
    en 3D i en 2D utilitzant l'esquema explícit o de Crank-Nicolson.

    Parameters
    ----------
    x : np.ndarray
        Malla espacial de valors de x.
    tau : np.ndarray
        Malla temporal de valors de tau.
    H : np.ndarray
        Matriu amb la solució de l'EDP per a cada combinació de x i tau.
    opcio : str
        Tipus d'opció, pot ser 'call' o 'put'.
    esquema : str
        Esquema utilitzat per a la solució ('explicit', 'cn', etc.).
    nom_fitxer_3d : str
        Nom del fitxer base per al gràfic 3D (sense extensió).
    nom_fitxer_2d : str
        Nom del fitxer per al gràfic 2D (amb extensió, com per exemple '.png').

    Returns
    -------
    None
        Aquesta funció guarda els gràfics generats en arxius en
        el directori especificat.

    Raises
    ------
    ValueError
        Si algun paràmetre d'entrada no és vàlid.
    """
    # Ruta relativa per a la carpeta
    carpeta, ruta_fitxer_2d = path_grafic(esquema, "H(x,tau)", nom_fitxer_2d)

    # Gràfic 3D amb diferents perspectives
    fig1 = plt.figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(111, projection="3d")

    # Malla
    X, T = np.meshgrid(x, tau)

    # Grafiquem la superfície
    ax1.plot_surface(X, T, H.T, cmap="viridis", alpha=0.5)
    ax1.set_xlabel("x")
    ax1.set_ylabel("τ")
    ax1.set_zlabel("H(x,τ)")
    if opcio == "call":
        ax1.set_title("Solució de H(x,τ) per una opció de compra")
    elif opcio == "put":
        ax1.set_title("Solució de H(x,τ) per una opció de venda")

    # Eliminem les graelles del gràfic 3D
    ax1.grid(False)

    # Guardem la perspectiva per defecte
    ruta_fitxer_3d_default = os.path.join(carpeta, nom_fitxer_3d + "_default.png")
    plt.savefig(ruta_fitxer_3d_default, dpi=300)

    # Generem diferents perspectives
    perspectives = [
        {"elev": 30, "azim": 45, "suffix": "_perspectiva1.png"},
        {"elev": 60, "azim": 90, "suffix": "_perspectiva2.png"},
        {"elev": 15, "azim": 180, "suffix": "_perspectiva3.png"},
        {"elev": 45, "azim": 270, "suffix": "_perspectiva4.png"},
    ]

    for p in perspectives:
        ax1.view_init(elev=p["elev"], azim=p["azim"])
        ruta_fitxer_3d = os.path.join(carpeta, nom_fitxer_3d + p["suffix"])
        plt.savefig(ruta_fitxer_3d, dpi=300)

    plt.close(fig1)

    # Gràfic 2D
    fig2 = plt.figure(figsize=(10, 7))
    ax2 = fig2.add_subplot(111)

    # Fem la gràfica de l'evolució de H per a diversos valors de tau
    step = max(len(tau) // 3, 1)
    for t_idx in range(0, len(tau), step):
        ax2.plot(x, H[:, t_idx], label=f"τ = {tau[t_idx]:.2f}")

    ax2.set_xlabel("x")
    ax2.set_ylabel("Valor de H")
    if opcio == "call":
        ax2.set_title(
            "Evolució de H(x,τ) per una opció de compra per a diferents valors de τ"
        )
    elif opcio == "put":
        ax2.set_title(
            "Evolució de H(x,τ) per una opció de venda per a diferents valors de τ"
        )

    ax2.legend()

    # Guardem el gràfic 2D
    plt.savefig(ruta_fitxer_2d, dpi=300)
    plt.close(fig2)
