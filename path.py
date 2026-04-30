import logging
from pathlib import Path
from markitdown import MarkItDown

pastas_necessarias = ["danfes", "processados", "saida_json", "logs"]

for pasta in pastas_necessarias:
    Path(pasta).mkdir(exist_ok=True)

logger = logging.getLogger("leitorDANFe")
logger.setLevel(logging.INFO)
logger.propagate = False

handler = logging.FileHandler("logs/processamento.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)


def converter_pdfs_para_markdown(origem: str = "danfes", destino: str = "saida_json", processados: str = "processados"):
    pdfs = list(Path(origem).glob("*.pdf"))

    if not pdfs:
        logger.info("Nenhum PDF encontrado na pasta %s.", origem)
        print(f"Nenhum PDF encontrado na pasta {origem}.")
        return

    md = MarkItDown()
    for pdf in pdfs:
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


converter_pdfs_para_markdown()
