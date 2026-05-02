from setup import criar_pastas
from logger import configurar_logger
from converter import converter_pdfs_para_markdown
from parser import testar_conexao

criar_pastas()
configurar_logger()
testar_conexao()
converter_pdfs_para_markdown()
