import logging
from config import PASTA_LOGS


def configurar_logger():
    logger = logging.getLogger("leitorDANFe")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.FileHandler(f"{PASTA_LOGS}/processamento.log", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
