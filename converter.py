import logging
from pathlib import Path
from markitdown import MarkItDown
from config import PASTA_ORIGEM, PASTA_PROCESSADOS, PASTA_DESTINO

logger = logging.getLogger("leitorDANFe")


def _is_valid_pdf(path: Path) -> bool:
    with open(path, "rb") as f:
        return f.read(5) == b"%PDF-"


def converter_pdfs_para_markdown(origem: str = PASTA_ORIGEM, destino: str = PASTA_DESTINO, processados: str = PASTA_PROCESSADOS):
    pdfs = list(Path(origem).glob("*.pdf"))

    if not pdfs:
        logger.info("Nenhum PDF encontrado na pasta %s.", origem)
        print(f"Nenhum PDF encontrado na pasta {origem}.")
        return

    md = MarkItDown()
    for pdf in pdfs:
        if not _is_valid_pdf(pdf):
            logger.warning("Arquivo ignorado (não é um PDF válido): %s", pdf.name)
            print(f"AVISO: {pdf.name} foi ignorado pois não é um PDF válido.")
            continue

        logger.info("Iniciando processamento: %s", pdf.name)
        try:
            resultado = md.convert(str(pdf))
            arquivo_destino = Path(destino) / (pdf.stem + ".md")
            arquivo_destino.write_text(resultado.text_content, encoding="utf-8")
            logger.info("Convertido: %s -> %s", pdf.name, arquivo_destino)

            pdf.replace(Path(processados) / pdf.name)
            logger.info("Movido para processados: %s", pdf.name)

            print(f"Convertido: {pdf.name} -> {arquivo_destino}")
        except Exception as e:
            logger.error("Falha ao processar %s: %s", pdf.name, e)
            print(f"ERRO ao processar {pdf.name}: {e}")
