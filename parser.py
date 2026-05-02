import json
import logging
from pathlib import Path
from dotenv import load_dotenv
import anthropic

from config import PASTA_DESTINO, PASTA_JSON

load_dotenv()

logger = logging.getLogger("leitorDANFe")

_SYSTEM_PROMPT = """Você é um extrator de dados de DANFE (Documento Auxiliar da Nota Fiscal Eletrônica).
Dado o conteúdo de um DANFE convertido para texto, extraia os dados e retorne APENAS um JSON válido, sem explicações ou markdown.

O JSON deve seguir exatamente esta estrutura:
{
  "numero_nota": "",
  "chave_acesso": "",
  "natureza_operacao": "",
  "destinatario": {
    "cnpj": "",
    "ie": ""
  },
  "produtos": [
    {
      "codigo": "",
      "descricao": "",
      "ncm": "",
      "cst": "",
      "cfop": "",
      "unidade": "",
      "quantidade": null,
      "valor_unitario": null,
      "valor_total": null,
      "bc_icms": null,
      "valor_icms": null,
      "valor_ipi": null,
      "aliq_icms": null,
      "aliq_ipi": null
    }
  ],
  "totais": {
    "base_calculo_icms": null,
    "valor_icms": null,
    "base_calculo_icms_st": null,
    "valor_icms_st": null,
    "valor_ipi": null,
    "valor_frete": null,
    "valor_seguro": null,
    "desconto": null,
    "outras_despesas": null,
    "valor_total_produtos": null,
    "valor_total_nota": null
  }
}

Use null para campos numéricos não encontrados e "" para campos de texto não encontrados.
Números decimais devem usar ponto como separador (ex: 196.185, não 196,185)."""


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


def extrair_danfe_para_json(pasta_markdown: str = PASTA_DESTINO, pasta_json: str = PASTA_JSON):
    arquivos = list(Path(pasta_markdown).glob("*.md"))

    if not arquivos:
        logger.info("Nenhum arquivo markdown encontrado em %s.", pasta_markdown)
        print(f"Nenhum arquivo markdown encontrado em {pasta_markdown}.")
        return

    client = anthropic.Anthropic()

    for arquivo in arquivos:
        logger.info("Extraindo dados de: %s", arquivo.name)
        conteudo = arquivo.read_text(encoding="utf-8")

        try:
            resposta = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": conteudo}],
            )

            texto = resposta.content[0].text.strip()

            # Remove bloco de código markdown caso o modelo inclua
            if texto.startswith("```"):
                texto = texto.split("\n", 1)[1]
                texto = texto.rsplit("```", 1)[0].strip()

            dados = json.loads(texto)

            arquivo_json = Path(pasta_json) / (arquivo.stem + ".json")
            arquivo_json.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.info("JSON salvo: %s", arquivo_json)
            print(f"Extraído: {arquivo.name} -> {arquivo_json}")

        except json.JSONDecodeError as e:
            logger.error("Falha ao parsear JSON de %s: %s", arquivo.name, e)
            print(f"ERRO ao parsear JSON de {arquivo.name}: {e}")
        except Exception as e:
            logger.error("Falha ao processar %s: %s", arquivo.name, e)
            print(f"ERRO ao processar {arquivo.name}: {e}")
