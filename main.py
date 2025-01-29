"""
main pipeline
"""
import math  # type: ignore
from typing import Callable, Literal

from src.esquemes.cn_H import esquema_crank_nicolson_H
from src.esquemes.cn_W import esquema_crank_nicolson_W
from src.esquemes.explicit_H import esquema_explicit_H
from src.esquemes.explicit_W import esquema_explicit_W
from src.grafics.grafic_H import grafic_H
from src.grafics.grafic_H_R import grafic_H_R
from src.grafics.grafic_W import grafic_W
from src.grafics.grafic_W_R import grafic_W_R
from src.logger import logger
from src.utils import (R_H, carregar_configuracio, desfer_canvi_variable_t,
                       interval_acotat)


class ResolutorEquacio:
    """
    Classe per a resoldre equacions diferencials parcials utilitzant esquemes numèrics.

    Aquesta classe permet resoldre les equacions H i W mitjançant els esquemes explícit i 
    Crank-Nicholson, generar gràfics dels resultats i aplicar acotacions als intervals 
    de les solucions.

    Attributes
    ----------
    config : dict
        Configuració carregada des d'un fitxer YAML amb els paràmetres necessaris per a la resolució.
    equacio : {'H', 'W'}
        Tipus d'equació a resoldre. Pot ser 'H' o 'W'.
    run_explicit : bool
        Si és True, executa l'esquema explícit per a l'equació seleccionada.
    run_crank_nicolson : bool
        Si és True, executa l'esquema Crank-Nicholson per a l'equació seleccionada.

    Methods
    -------
    resoldre_equacio()
        Resol l'equació especificada aplicant els esquemes numèrics seleccionats i genera els gràfics.
    _resoldre_esquema_numeric(opcio, esquema, graficar_no_acotat=False)
        Aplica un esquema numèric específic per a l'opció i l'equació seleccionades.
    _generar_grafic(x, tau, H, opcio, esquema, canvi_variable=True, acotat=False)
        Genera gràfics en 2D i 3D dels resultats obtinguts.
    """

    def __init__(
        self,
        config: dict,
        equacio: Literal["H", "W"],
        run_explicit: bool = True,
        run_crank_nicolson: bool = True,
    ) -> None:
        """
        Inicialitza una instància de la classe ResolutorEquacio.

        Parameters
        ----------
        config : dict
            Configuració carregada des d'un fitxer YAML amb els paràmetres necessaris per a 
            la resolució.
        equacio : {'H', 'W'}
            Tipus d'equació a resoldre. Pot ser 'H' o 'W'.
        run_explicit : bool, optional
            Si és True, executa l'esquema explícit per a l'equació seleccionada. 
            Per defecte és True.
        run_crank_nicolson : bool, optional
            Si és True, executa l'esquema Crank-Nicholson per a l'equació seleccionada. 
            Per defecte és True.

        Returns
        -------
        None
        """
        self.config = config
        self.equacio = equacio
        self.run_explicit = run_explicit
        self.run_crank_nicolson = run_crank_nicolson
        self.logger = logger

    def _generar_grafic(
        self,
        x: list[float],
        tau: float,
        H: float,
        opcio: Literal["call", "put"],
        esquema: Literal["explicit", "cn"],
        canvi_variable: bool = True,
        acotat: bool = False,
    ) -> None:
        """
        Genera un gràfic 2D i 3D segons els paràmetres donats.

        Parameters
        ----------
        x : list of float
            Valors de l'eix x utilitzats per al gràfic.
        tau : float
            Valor de tau (paràmetre temporal) per al càlcul.
        H : float
            Valor de H (constant o paràmetre específic del problema).
        opcio : {'call', 'put'}
            Tipus d'opció: 'call' o 'put'.
        esquema : {'explicit', 'cn'}
            Esquema utilitzat: 'explicit' o 'cn' (Crank-Nicholson).
        canvi_variable : bool, optional
            Indica si s'ha aplicat el canvi de variable. El valor per defecte és True.
        acotat : bool, optional
            Indica si s'utilitzen valors acotats per als gràfics. El valor per defecte és False.

        Returns
        -------
        None
            Aquesta funció no retorna cap valor. Genera gràfics i els guarda en fitxers.

        Notes
        -----
        La funció utilitza diferents funcions gràfiques basades en els paràmetres 
        `self.equacio` i `canvi_variable`.

        Examples
        --------
        >>> self._generar_grafic([0.1, 0.2, 0.3], 0.5, 1.0, 'call', 'explicit', True, acotat=True)
        Genera un gràfic acotat amb canvi de variable per l'equació definida a `self.equacio`,
        amb esquema explícit i opció 'call'.
        """
        self.logger.log(
            (
                f"Generant gràfic per a l'esquema {esquema} de l'opció {opcio} "
                f"amb l'equació {self.equacio}."
            ),
            "info",
        )
        # Determinar la funció de gràfic
        func_grafic: Callable = {
            ("H", True): grafic_H,
            ("H", False): grafic_H_R,
            ("W", True): grafic_W,
            ("W", False): grafic_W_R,
        }[(self.equacio, canvi_variable)]

        # Determinem l'etiqueta de l'esquema
        esquema_etiqueta = f"{esquema}_{self.equacio}"

        # Determinem els noms dels fitxers basats en l'opció i si és acotat
        sufix_acotat: str = "_acotat" if acotat else ""
        fitxer_3d: str = f"{opcio}_3d{sufix_acotat}.png"
        fitxer_2d: str = f"{opcio}_2d{sufix_acotat}.png"

        # Cridem la funció de gràfic
        func_grafic(x, tau, H, opcio, esquema_etiqueta, fitxer_3d, fitxer_2d)

    def _resoldre_esquema_numeric(
        self,
        opcio: Literal["call", "put"],
        esquema: Literal["explicit", "cn"],
        graficar_no_acotat: bool = False,
    ) -> None:
        """
        Resol numèricament l'esquema especificat i genera els gràfics corresponents.

        Parameters
        ----------
        opcio : {'call', 'put'}
            Tipus d'opció financera: 'call' o 'put'.
        esquema : {'explicit', 'cn'}
            Esquema numèric a utilitzar: 'explicit' (explícit) o 'cn' (Crank-Nicholson).
        graficar_no_acotat : bool, optional
            Indica si es generen gràfics per a les solucions no acotades. 
            El valor per defecte és False.

        Returns
        -------
        None
            Aquesta funció no retorna cap valor. Genera gràfics per a solucions acotades i 
            no acotades.

        Notes
        -----
        La funció utilitza esquemes numèrics específics segons l'equació (`self.equacio`) i 
        el tipus d'opció.
        També realitza canvis de variable i ajustos per obtenir solucions acotades.

        Examples
        --------
        >>> self._resoldre_esquema_numeric('call', 'explicit', graficar_no_acotat=True)
        Resol l'esquema explícit per a una opció 'call' i genera els gràfics corresponents, 
        incloent-hi gràfics no acotats.
        """
        try:
            self.logger.log(
                f"Resolent esquema {esquema} per a l'equació {self.equacio} i l'opció {opcio}.",
                "info",
            )
            func_esquema: Callable = {
                ("H", "explicit"): esquema_explicit_H,
                ("H", "cn"): esquema_crank_nicolson_H,
                ("W", "explicit"): esquema_explicit_W,
                ("W", "cn"): esquema_crank_nicolson_W,
            }[(self.equacio, esquema)]

            # valor = self.equacio(x, tau)
            x, tau, valor = func_esquema(
                self.config["M"],
                self.config["N"],
                self.config["x_min"],
                self.config["x_max"],
                self.config["T"],
                self.config["sigma"],
                self.config["r"],
                opcio,
            )
            if graficar_no_acotat:
                # Gràfiques per a l'equació
                self._generar_grafic(
                    x,
                    tau,
                    valor,
                    opcio,
                    esquema,
                    canvi_variable=True,
                    acotat=False,
                )

            # Acotem intervals
            x_acotat, H_acotat = interval_acotat(
                x,
                valor,
                eval(self.config["acotacions"][f"{esquema}_{opcio}"][0]),
                eval(self.config["acotacions"][f"{esquema}_{opcio}"][1]),
            )
            # Gràfiques per a l'equació acotada
            self._generar_grafic(
                x_acotat,
                tau,
                H_acotat,
                opcio,
                esquema,
                canvi_variable=True,
                acotat=True,
            )

            # Desfem canvis de variable per a les solucions
            t = desfer_canvi_variable_t(self.config["T"], tau, self.config["sigma"])
            nou_x_acotat, nou_H_acotat = x_acotat, H_acotat = interval_acotat(
                x,
                valor,
                eval(self.config["acotacions"][f"canvi_{esquema}_{opcio}"][0]),
                eval(self.config["acotacions"][f"canvi_{esquema}_{opcio}"][1]),
            )
            R1_acotat = R_H(self.config["T"], nou_x_acotat)
            self._generar_grafic(
                R1_acotat,
                t,
                nou_H_acotat,
                opcio,
                esquema,
                canvi_variable=False,
                acotat=True,
            )
            return None
        except Exception as e:
            self.logger.log(
                f"Error en resoldre esquema {esquema} per a l'equació {self.equacio} i "
                f"l'opció {opcio}: {str(e)}",
                "error",
            )

        self.logger.log(
            f"Finalitzada la resolució de l'esquema {esquema} per a l'equació {self.equacio} i "
            f"l'opció {opcio}.",
            "info",
        )

    def resoldre_equacio(self) -> None:
        """
        Resol l'equació donada aplicant esquemes numèrics i genera els gràfics corresponents.

        Parameters
        ----------
        equacio : {'H', 'W'}
            Tipus d'equació a resoldre. Pot ser 'H' o 'W'.

        Returns
        -------
        None
            Aquesta funció no retorna cap valor. Executa els esquemes numèrics i genera els gràfics.

        Notes
        -----
        - Aquesta funció executa dos tipus d'esquemes numèrics:
        1. Esquema explícit.
        2. Esquema Crank-Nicholson (CN).
        - Els esquemes es resolen tant per a opcions 'call' com 'put'.
        - Si l'opció `grafic_no_acotat` està activada en la configuració (`self.config`), 
            es generen gràfics per a valors no acotats.

        Examples
        --------
        >>> self.resoldre_equacio('H')
        Resol l'equació 'H' amb els esquemes explícit i Crank-Nicholson per a opcions 
        'call' i 'put'.
        """
        try:
            if self.run_explicit:
                self._resoldre_esquema_numeric(
                    "call", "explicit", self.config["grafic_no_acotat"]
                )
                self._resoldre_esquema_numeric(
                    "put", "explicit", self.config["grafic_no_acotat"]
                )

            if self.run_crank_nicolson:
                self._resoldre_esquema_numeric("call", "cn")
                self._resoldre_esquema_numeric("put", "cn")
        except Exception as e:
            self.logger.log(
                f"Error en la resolució de l'equació {self.equacio}: {str(e)}", "error"
            )
        self.logger.log(
            f"Finalitzada la resolució de l'equació {self.equacio}.", "info"
        )


def main(
    run_explicit_H: bool = True,
    run_crank_nicolson_H: bool = True,
    run_explicit_W: bool = True,
    run_crank_nicolson_W: bool = True,
) -> None:
    """
    Funció principal per a la resolució de les equacions H i W mitjançant esquemes numèrics.

    Parameters
    ----------
    run_explicit_H : bool, optional
        Si és True, executa l'esquema explícit per a l'equació H. Per defecte és True.
    run_crank_nicolson_H : bool, optional
        Si és True, executa l'esquema Crank-Nicholson per a l'equació H. Per defecte és True.
    run_explicit_W : bool, optional
        Si és True, executa l'esquema explícit per a l'equació W. Per defecte és True.
    run_crank_nicolson_W : bool, optional
        Si és True, executa l'esquema Crank-Nicholson per a l'equació W. Per defecte és True.

    Returns
    -------
    None
        Aquesta funció no retorna cap valor. Configura i resol les equacions H i W 
        amb els esquemes especificats.

    Notes
    -----
    - La configuració es carrega des d'un fitxer YAML ubicat a `config/main.yaml`.
    - Es crea una instància de `ResolutorEquacio` per a cadascuna de les equacions (H i W).
    - La resolució s'efectua segons els paràmetres especificats a la crida de la funció.

    Examples
    --------
    Executar tots els esquemes:
    >>> main()

    Executar només l'esquema explícit per a H i Crank-Nicholson per a W:
    >>> main(run_explicit_H=True, run_crank_nicolson_H=False, run_explicit_W=False,
        run_crank_nicolson_W=True)
    """
    logger.log("Iniciant el pipeline...", "info")

    # Carreguem la configuració des del fitxer YAML
    config = carregar_configuracio("config/main.yaml")

    try:
        # Creem instància del resolutor per a l'equació H
        if run_explicit_H or run_crank_nicolson_H:
            logger.log("Iniciant resolució de l'equació H.", "info")
            resolutor_H = ResolutorEquacio(
                config=config["H_equacio"],
                equacio="H",
                run_explicit=run_explicit_H,
                run_crank_nicolson=run_crank_nicolson_H,
            )
            resolutor_H.resoldre_equacio()

        if run_explicit_W or run_crank_nicolson_W:
            logger.log("Iniciant resolució de l'equació W.", "info")
            resolutor_W = ResolutorEquacio(
                config=config["W_equacio"],
                equacio="W",
                run_explicit=run_explicit_W,
                run_crank_nicolson=run_crank_nicolson_W,
            )
            resolutor_W.resoldre_equacio()

    except Exception as e:
        logger.log(f"Error en la resolució de les equacions: {str(e)}", "error")

    logger.log("Finalitzada la resolució de les equacions.", "info")


if __name__ == "__main__":
    main(
        run_explicit_H=True,
        run_crank_nicolson_H=True,
        run_explicit_W=True,
        run_crank_nicolson_W=True,
    )
