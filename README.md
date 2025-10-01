# DATATHON API | PÓS TECH

![Status](https://img.shields.io/badge/STATUS-CONCLUÍDO-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)

## 📋 Índice
- [Introdução](#-introdução)
- [Objetivo](#🎯-objetivo)
- [Funcionalidades](#✨-funcionalidades)
- [Tecnologias](#🛠-tecnologias)
- [Organização do Projeto](#📁-organização-do-projeto)
- [Instalação e Uso](#🚀-instalação-e-uso)
- [Variáveis de Ambiente](#🔧-variáveis-de-ambiente)
- [Documentação da API](#📚-documentação-da-api)

## 🏁 Introdução

Este projeto foi desenvolvido como parte do **Datathon da Pós Tech**, uma iniciativa que desafia participantes a criar soluções inovadoras usando tecnologias modernas.

Com base no estudo de caso da empresa Decision, especializada em recrutamento no setor de TI, desenvolvemos um MVP para otimizar processos de seleção, utilizando **Vector Search, RAG e LLM**.

A API serve como backend para um sistema completo de recrutamento e seleção inteligente, incorporando técnicas avançadas de RAG (Retrieval-Augmented Generation) e processamento de linguagem natural.

O sistema é capaz de analisar currículos, comparar candidatos com vagas específicas e fornecer recomendações inteligentes através de modelos de IA, revolucionando o processo tradicional de recrutamento.

## 🎯 Objetivo

Fornecer uma API robusta e escalável para:
- **Gestão completa de vagas** (CRUD)
- **Busca semântica** em bancos de dados de currículos
- **Análise inteligente** de compatibilidade candidato-vaga
- **Processamento de documentos** (PDF, DOCX) com extração de informações
- **Geração de insights** através de modelos de LLM (OpenAI)

## ✨ Funcionalidades

### 👥 Gestão de Vagas
- Criação, listagem, atualização e exclusão de vagas
- Campos detalhados: requisitos técnicos, habilidades comportamentais, nível de senioridade

### 🔍 Busca Híbrida Avançada
- **Embeddings densos**: `all-MiniLM-L6-v2` para similaridade semântica
- **BM25**: Busca textual tradicional otimizada
- **ColBERT**: Reranking por interação tardia para precisão
- Combinação dos três métodos para resultados superiores

### 🤖 Análise com IA
- Análise de compatibilidade com OpenAI GPT-4
- Respostas contextualizadas com fontes de referência

## 🛠 Tecnologias

### Backend Principal
- **Python 3.12** - Linguagem principal
- **FastAPI** - Framework web moderno e rápido
- **SQLAlchemy** - ORM e gerenciamento de banco de dados
- **Pydantic** - Validação de dados e configurações

### Banco de Dados & Vector Store
- **PostgreSQL** - Banco de dados relacional
- **Qdrant** - Vector database para buscas semânticas

### Processamento de Dados & IA
- **FastEmbed** - Geração de embeddings otimizada
- **OpenAI API** - Modelos de linguagem para análise

### Infraestrutura
- **Docker** - Containerização
- **Digital Ocean** - Deploy e hospedagem
- **Uvicorn** - Servidor ASGI

## 📁 Organização do Projeto
```
datathon_api/
├── config/
│ ├── settings.py # Configurações
│ └── clients.py # Clients
├── models/
│ ├── schema_vagas.py # Schemas Pydantic para vagas
│ └── embeddings.py # Modelos de embeddings
├── routers/
│ ├── vaga_routers.py # Endpoints de gestão de vagas
│ ├── search.py # Endpoints de busca semântica
│ └── llm.py # Endpoints de análise com IA
├── services/
│ ├── crud.py # Operações de banco de dados
│ ├── embedder.py # Geração de embeddings
│ ├── retriever.py # Busca no Qdrant
│ └── llm_service.py # Integração com OpenAI
├── requirements.txt # Dependências do projeto
└── Dockerfile # Configuração do container
└── main.py # Inicialização da API
```

## 💻 Acesso a API

Documentação API: https://datathon-api-ljhdg.ondigitalocean.app/docs

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.12
- PostgreSQL
- Qdrant Cloud ou local

### 📥 Instalação Local

1. **Clone o repositório**
```bash
git clone https://github.com/cezarmaldini/datathon_api.git
cd datathon_api
```

2. **Crie um ambiente virtual**

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```
cp .env.example .env
# Edite o .env com suas configurações
```

5. **Execute a aplicação**
```
uvicorn app.main:app --reload --port 8001
```

## 🔧 Variáveis de Ambiente

**Banco de Dados**
```
# PostgreSQL
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=port
POSTGRES_DATABASE=database
```

**Qdrant Vector Store**
```
QDRANT_URL=sua_url_do_qdrant
QDRANT_API_KEY=sua_chave_api
```

**OpenAI & LLM**
```
OPENAI_API_KEY=sk-sua_chave_openai
```

**Modelos de Embedding**
```
DENSE_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
BM25_MODEL_NAME=Qdrant/bm25
LATE_INTERACTION_MODEL_NAME=colbert-ir/colbertv2.0
```

## 📚 Documentação da API

A API está dividida em três grupos principais de endpoints:

### 👥 Gestão de Vagas (`/vagas`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/vagas/` | Lista vagas |
| `POST` | `/vagas/` | Cria nova vaga |
| `GET` | `/vagas/{id}` | Obtém vaga específica |
| `PUT` | `/vagas/{id}` | Atualiza vaga existente |
| `DELETE` | `/vagas/{id}` | Exclui vaga |

### 🔍 Busca e Análise (`/search`, `/llm`)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/search` | Busca semântica em currículos |
| `POST` | `/llm/` | Análise de candidatos com IA |
| `POST` | `/llm/test` | Teste de funcionalidade LLM |

### 📊 Exemplos de Uso

**Criar uma vaga:**
```python
import requests

url = "http://localhost:8001/vagas/"
data = {
    "titulo_vaga": "Engenheiro de Dados Pleno",
    "tipo_contratacao": "CLT",
    "cidade": "São Paulo",
    "estado": "SP",
    "nivel_profissional": "Pleno",
    "nivel_academico": "Superior",
    "areas_atuacao": ["TI", "Dados"],
    "principais_atividades": "Processar e analisar grandes volumes de dados",
    "competencias_tecnicas": ["Python", "SQL", "Spark"],
    "habilidades_comportamentais": ["Comunicação", "Trabalho em equipe"],
    "modalidade": "Híbrido"
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Resposta: {response.json()}")
```

**Buscar candidatos com IA:**
```python
import requests

url = "http://localhost:8001/llm/"
data = {
    "query": "Analise os candidatos para Engenheiro de Dados considerando experiência com Python e Spark",
    "collection_name": "Engenheiro de Dados Pleno",
    "limit": 5,
    "model": "gpt-4"
}

response = requests.post(url, json=data)
print(f"Status: {response.status_code}")
print(f"Resposta: {response.json()}")
```

**Listar todas as vagas:**
```python
import requests

url = "http://localhost:8001/vagas/"
response = requests.get(url)
vagas = response.json()

print(f"Total de vagas: {vagas['total']}")
for vaga in vagas['vagas']:
    print(f"- {vaga['titulo_vaga']} | {vaga['nivel_profissional']} | {vaga['cidade']}")
```

## 👥 Autor
- Cezar Maldini

- GitHub: @cezarmaldini

- Projeto: [Datathon Pós Tech]

---

⭐️ Se este projeto foi útil, considere dar uma estrela no repositório!