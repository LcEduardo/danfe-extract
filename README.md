# danfe-extract

Extrator automático de dados de DANFE (PDF) para JSON estruturado, usando IA.

---

## O problema que isso resolve

A nota fiscal eletrônica (NF-e) existe em dois formatos:

- **XML** — o arquivo oficial, com todos os dados estruturados e legíveis por máquina
- **DANFE** (PDF) — a representação visual da nota, feita para humanos lerem

Na prática, a maioria das empresas trabalha com o DANFE em PDF porque o XML é difícil de abrir e interpretar sem ferramentas específicas. O problema é que dados presos em PDF são difíceis de processar, cruzar com outros sistemas ou analisar em volume.

Este projeto resolve isso: você joga um PDF de DANFE, ele devolve um JSON limpo e estruturado com todos os dados da nota — produtos, impostos, totais, destinatário — prontos para uso.

---

## Como funciona

O processamento ocorre em dois estágios:

```
danfes/ (PDF)
    │
    ▼
[1. Conversão]  converter.py  →  PDF é convertido para texto Markdown
    │
    ▼
extract_markitdown/ (Markdown)
    │
    ▼
[2. Extração]   parser.py    →  Claude lê o texto e extrai os dados como JSON
    │
    ▼
json_extraidos/ (JSON)
```

**Estágio 1 — PDF → Markdown:**
A biblioteca [MarkItDown](https://github.com/microsoft/markitdown) (Microsoft) converte o PDF para texto. O arquivo original é movido para a pasta `processados/` após a conversão bem-sucedida.

**Estágio 2 — Markdown → JSON:**
O texto é enviado para a API do Claude com um prompt que instrui a IA a extrair os dados e retorná-los em um JSON com estrutura fixa. A IA lida com variações de layout entre diferentes emissores de nota, o que tornaria um parser tradicional frágil.

---

## Estrutura do projeto

```
danfe-extract/
├── main.py              # Ponto de entrada — orquestra todo o fluxo
├── config.py            # Caminhos das pastas (configuração centralizada)
├── converter.py         # Estágio 1: PDF → Markdown
├── parser.py            # Estágio 2: Markdown → JSON via Claude API
├── setup.py             # Cria a estrutura de diretórios necessária
├── logger.py            # Configuração do sistema de logs
├── requirements.txt     # Dependências Python
├── .env                 # Chave de API (não versionado)
│
├── danfes/              # Entrada: coloque os PDFs aqui
├── processados/         # PDFs já convertidos (movidos automaticamente)
├── extract_markitdown/  # Saída intermediária em Markdown
├── json_extraidos/      # Saída final em JSON
└── logs/
    └── processamento.log
```

---

## Pré-requisitos

- Python 3.10+
- Conta na [Anthropic](https://console.anthropic.com/) com uma chave de API

---

## Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd danfe-extract

# Instale as dependências
pip install -r requirements.txt

# Configure a chave de API
# Crie um arquivo .env na raiz com o seguinte conteúdo:
ANTHROPIC_API_KEY=sua_chave_aqui
```

---

## Uso

1. Coloque os arquivos PDF de DANFE na pasta `danfes/`
2. Execute:

```bash
python main.py
```

3. Os JSONs extraídos estarão em `json_extraidos/`

---

## Estrutura do JSON gerado

```json
{
  "numero_nota": "002.305.647",
  "chave_acesso": "42 2604 84586205000352 55 000 002305647 1 59751957 0",
  "natureza_operacao": "Venda p/Revenda",
  "destinatario": {
    "cnpj": "12.958.084/0001-50",
    "ie": "256270520"
  },
  "produtos": [
    {
      "codigo": "140422-0",
      "descricao": "BANDEJA SUSPENSAO DIANTEIRA DIREITA",
      "ncm": "87088000",
      "cst": "060",
      "cfop": "6102",
      "unidade": "PC",
      "quantidade": 2,
      "valor_unitario": 196.185,
      "valor_total": 392.37,
      "bc_icms": null,
      "valor_icms": null,
      "valor_ipi": null,
      "aliq_icms": 12.0,
      "aliq_ipi": null
    }
  ],
  "totais": {
    "base_calculo_icms": 479.85,
    "valor_icms": 57.25,
    "base_calculo_icms_st": null,
    "valor_icms_st": null,
    "valor_ipi": null,
    "valor_frete": null,
    "valor_seguro": null,
    "desconto": null,
    "outras_despesas": null,
    "valor_total_produtos": 479.85,
    "valor_total_nota": 479.85
  }
}
```

Campos numéricos não encontrados no documento retornam `null`. Campos de texto não encontrados retornam `""`.

---

## Módulos

### `main.py`
Orquestrador. Chama os módulos na sequência correta: cria as pastas, configura o logger, converte os PDFs e extrai os dados.

### `config.py`
Define os caminhos de todas as pastas do projeto em um único lugar. Altere aqui para mudar onde os arquivos são lidos e salvos.

### `converter.py`
Recebe os PDFs de `danfes/`, valida se são PDFs reais (verifica o header `%PDF-`) e usa o MarkItDown para converter o conteúdo para texto Markdown. PDFs processados com sucesso são movidos para `processados/`.

### `parser.py`
Lê os arquivos Markdown de `extract_markitdown/`, envia cada um para a API do Claude com um system prompt que define a estrutura JSON esperada, e salva o resultado em `json_extraidos/`. Inclui a função `testar_conexao()` para validar a chave de API antes do processamento.

### `logger.py`
Configura um logger nomeado `leitorDANFe` que escreve em `logs/processamento.log` com timestamp, nível e mensagem.

### `setup.py`
Cria todas as pastas necessárias caso não existam. Seguro para rodar múltiplas vezes.

---

## Dependências

| Pacote | Uso |
|---|---|
| `anthropic` | SDK oficial da Anthropic para chamar a Claude API |
| `markitdown` | Conversão de PDF para Markdown (Microsoft) |
| `python-dotenv` | Carregamento do `.env` com a chave de API |

---

## Logs

Todos os eventos são registrados em `logs/processamento.log`:

```
2026-05-02 14:23:01 INFO  Convertendo: nota-scherer.pdf
2026-05-02 14:23:03 INFO  Markdown salvo: extract_markitdown/nota-scherer.md
2026-05-02 14:23:03 INFO  Extraindo dados de: nota-scherer.md
2026-05-02 14:23:07 INFO  JSON salvo: json_extraidos/nota-scherer.json
```

Erros são registrados com nível `ERROR` e incluem o nome do arquivo e a mensagem da exceção.

---

## Limitações conhecidas

- **Qualidade do PDF:** DANFEs gerados por scan (foto/imagem) têm extração degradada porque o MarkItDown não faz OCR — ele lê texto embutido no PDF.
- **Custo de API:** Cada nota consome tokens da Claude API. Para volumes grandes, considere usar `claude-haiku-4-5` no `parser.py` para reduzir custos.
- **Campos opcionais:** Nem toda DANFE contém todos os campos do schema (ex: IPI, ICMS-ST). Nesses casos o valor retornado é `null`.
