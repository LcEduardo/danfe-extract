import logging
from dotenv import load_dotenv
import anthropic

load_dotenv()

logger = logging.getLogger("leitorDANFe")


def testar_conexao():
    try:
        client = anthropic.Anthropic()
        client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            messages=[{"role": "user", "content": "ping"}],
        )
        logger.info("Conexão com a Anthropic estabelecida com sucesso.")
        print("Conexão com a Anthropic: OK")
    except Exception as e:
        logger.error("Falha ao conectar com a Anthropic: %s", e)
        print(f"ERRO ao conectar com a Anthropic: {e}")
