from pathlib import Path
from markitdown import MarkItDown

pastas_necessarias = ["danfes", "processados", "saida_json"]

for pasta in pastas_necessarias:
    Path(pasta).mkdir(exist_ok=True)

def converter_pdfs_para_markdown(origem: str = "danfes", destino: str = "saida_json", processados: str = "processados"):
    pdfs = list(Path(origem).glob("*.pdf"))

    if not pdfs:
        print(f"Nenhum PDF encontrado na pasta {origem}.")
        return

    md = MarkItDown()
    for pdf in pdfs:
        resultado = md.convert(str(pdf))
        arquivo_destino = Path(destino) / (pdf.stem + ".md")
        arquivo_destino.write_text(resultado.text_content, encoding="utf-8")
        pdf.rename(Path(processados) / pdf.name)
        print(f"Convertido: {pdf.name} -> {arquivo_destino}")


converter_pdfs_para_markdown()