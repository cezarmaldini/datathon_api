# test_llm_local.py

from config.settings import Settings
from services.embedder import QueryEmbedder
from services.retriever import QdrantRetriever
from services.llm_service import LLMService
from models.api import OpenAIRequest

def main():
    # Carregar configurações
    settings = Settings()

    # Criar instâncias
    embedder = QueryEmbedder(
        dense_model_name=settings.dense_model_name,
        bm25_model_name=settings.bm25_model_name,
        late_interaction_model_name=settings.late_interaction_model_name,
    )

    retriever = QdrantRetriever(settings=settings)
    llm_service = LLMService(settings=settings)

    # Simular payload que viria do Streamlit
    request = OpenAIRequest(
        query="Liste os pontos fortes dos candidatos para Engenheiro de Software Sênior",
        collection_name="Engenheiro de Software - Sênior - Presencial - PJ",
        limit=5,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        max_output_tokens=settings.openai_max_output_tokens,
    )

    try:
        print("\n=== 1. Gerando embeddings ===")
        query_embeddings = embedder.embed_query(request.query)
        print("Embeddings gerados com sucesso")

        print("\n=== 2. Buscando documentos no Qdrant ===")
        context_documents = retriever.search_documents(
            collection_name=request.collection_name,
            embeddings=query_embeddings,
            limit=request.limit,
        )
        print(f"Documentos encontrados: {len(context_documents)}")

        print("\n=== 3. Chamando OpenAI ===")
        answer = llm_service.generate_response(
            query=request.query,
            context_documents=context_documents,
            model=request.model,
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        )
        print("\n=== RESPOSTA FINAL ===")
        print(answer)

    except Exception as e:
        print("\n❌ Erro durante a execução:")
        print(str(e))


if __name__ == "__main__":
    main()
