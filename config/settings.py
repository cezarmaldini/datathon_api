import os
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # API
    api_title: str = 'DATATHON | PÓS TECH'
    api_description: str = 'Datathon'
    api_version: str = '1.0'
    api_url_local: str = 'http://localhost:8001'

    # Qdrant
    qdrant_url: str = os.getenv('QDRANT_URL')
    qdrant_api_key: str = os.getenv('QDRANT_API_KEY')
    qdrant_timeout: float = 60.0
    qdrant_prefetch_limit: int = 25

    # Models
    dense_model_name: str = ("sentence-transformers/all-MiniLM-L6-v2")
    dense_model_max_tokens: int = 384
    bm25_model_name: str = "Qdrant/bm25"
    late_interaction_model_name: str = "colbert-ir/colbertv2.0-mini"

    # Postgres Supabase
    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD')
    postgres_host: str = os.getenv('POSTGRES_HOST')
    postgres_port: str = os.getenv('POSTGRES_PORT')
    postgres_database: str = os.getenv('POSTGRES_DATABASE')

    # OpenAI
    openai_api_key: str = os.getenv('OPENAI_API_KEY')
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.5
    openai_max_output_tokens: int = 4096
    openai_system_prompt: str = """
    Você é um especialista em Recursos Humanos e análise de currículos. 
    Analise os candidatos com base nas informações fornecidas e selecione os 3 mais adequados para a vaga.

    VAGA EM ANÁLISE:
    {query}

    CURRÍCULOS DISPONÍVEIS:
    {context}

    INSTRUÇÕES:
    1. Analise cada currículo em relação aos requisitos da vaga
    2. Selecione até 3 candidatos mais adequados
    3. Para cada candidato selecionado, justifique a escolha destacando:
    - Compatibilidade técnica
    - Experiência relevante  
    - Habilidades comportamentais
    - Potencial de adaptação
    4. Se nenhum candidato for adequado, explique o motivo
    5. Baseie-se APENAS nas informações fornecidas

    Retorne a análise de forma estruturada e objetiva."""