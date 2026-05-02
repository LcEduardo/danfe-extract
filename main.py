from setup import criar_pastas
from logger import configurar_logger
from converter import converter_pdfs_para_markdown
from parser import testar_conexao, extrair_danfe_para_json

criar_pastas()
configurar_logger()
# testar_conexao()
converter_pdfs_para_markdown()
extrair_danfe_para_json()
