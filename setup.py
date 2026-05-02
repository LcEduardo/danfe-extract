from pathlib import Path
from config import PASTA_ORIGEM, PASTA_PROCESSADOS, PASTA_DESTINO, PASTA_JSON, PASTA_LOGS


def criar_pastas():
    for pasta in [PASTA_ORIGEM, PASTA_PROCESSADOS, PASTA_DESTINO, PASTA_JSON, PASTA_LOGS]:
        Path(pasta).mkdir(exist_ok=True)
