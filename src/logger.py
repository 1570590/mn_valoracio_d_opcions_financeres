"""Mòdul de registre per a la consola amb format i colors."""

import logging

import colorama

colorama.init(autoreset=True)


class Logger:  # pylint: disable=too-few-public-methods
    """
    Una classe de registre que proporciona un registre a la consola
    amb format i codis de colors.

    Atributs
    ---------
    COLORS : dict
        Assignació de nivells de registre als seus respectius codis de color.
    logger : logging.Logger
        La instància del logger.
    """

    COLORS = {
        "INFO": colorama.Fore.GREEN,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
    }

    def __init__(self, name: str) -> None:
        """
        Inicialitza la instància del Logger.

        Paràmetres
        ----------
        name : str
            El nom de la instància del logger.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log(self, message: str, level: str = "info") -> None:
        """
        Registra un missatge amb el nivell de severitat especificat.

        Paràmetres
        ----------
        message : str
            El missatge a registrar.
        level : str, opcional
            El nivell de severitat del missatge (per defecte "info").
            Accepta "info", "warning" o "error".
        """
        level = level.upper()
        color = self.COLORS.get(level, "")
        formatted_message = f"{color}{message}{colorama.Style.RESET_ALL}"

        if level == "INFO":
            self.logger.info(formatted_message)
        elif level == "WARNING":
            self.logger.warning(formatted_message)
        elif level == "ERROR":
            self.logger.error(formatted_message)


# Creem una instància global del logger per no crear-ne una a cada fitxer
logger = Logger(__name__)
