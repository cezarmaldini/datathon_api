from fastapi import APIRouter, Depends, HTTPException
from models.api import OpenAIRequest, OpenAIResponse
from services.retriever import QdrantRetriever
from services.embedder import QueryEmbedder
from services.llm_service import LLMService
from config.settings import Settings
import logging
import time

# 🔧 Configurar logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/llm", tags=["llm"])


def get_settings():
    return Settings()


def get_embedder(settings: Settings = Depends(get_settings)):
    return QueryEmbedder(
        dense_model_name=settings.dense_model_name,
        bm25_model_name=settings.bm25_model_name,
        late_interaction_model_name=settings.late_interaction_model_name,
    )


def get_retriever(settings: Settings = Depends(get_settings)):
    return QdrantRetriever(settings=settings)


def get_openai_service(settings: Settings = Depends(get_settings)):
    return LLMService(settings=settings)


@router.post("", response_model=OpenAIResponse)
async def generate_openai_response(
    request: OpenAIRequest,
    embedder: QueryEmbedder = Depends(get_embedder),
    retriever: QdrantRetriever = Depends(get_retriever),
    openai_service: LLMService = Depends(get_openai_service),
):
    start_time = time.time()
    
    try:
        # 🔧 LOG INICIAL
        logger.info(f"🚀 Iniciando LLM para coleção: {request.collection_name}")
        logger.info(f"📝 Query: {request.query[:100]}...")
        logger.info(f"🔢 Limit: {request.limit}")

        # 1. GERAR EMBEDDINGS
        logger.info("🔧 Gerando embeddings da query...")
        query_embeddings = embedder.embed_query(request.query)
        logger.info("✅ Embeddings gerados com sucesso")

        # 2. BUSCAR NO QDRANT
        logger.info(f"🔍 Buscando documentos no Qdrant...")
        context_documents = retriever.search_documents(
            collection_name=request.collection_name, 
            embeddings=query_embeddings, 
            limit=request.limit
        )
        logger.info(f"✅ {len(context_documents)} documentos encontrados")

        # 3. GERAR RESPOSTA COM OPENAI
        logger.info("🤖 Chamando OpenAI...")
        answer = openai_service.generate_response(
            query=request.query,
            context_documents=context_documents,
            model=request.model,
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        )
        logger.info("✅ Resposta OpenAI gerada com sucesso")

        # 🔧 LOG FINAL
        tempo_total = time.time() - start_time
        logger.info(f"⏰ LLM concluído em {tempo_total:.2f} segundos")

        return OpenAIResponse(answer=answer, source_documents=context_documents)

    except HTTPException:
        # Re-lança exceções HTTP que já sabemos
        raise
        
    except Exception as e:
        # 🔧 LOG DE ERRO DETALHADO
        tempo_total = time.time() - start_time
        logger.error(f"💥 ERRO NO ENDPOINT LLM:")
        logger.error(f"   ⏰ Tempo até erro: {tempo_total:.2f}s")
        logger.error(f"   📝 Query: {request.query}")
        logger.error(f"   🗂️ Coleção: {request.collection_name}")
        logger.error(f"   🚨 Erro: {str(e)}")
        logger.error(f"   📋 Tipo: {type(e).__name__}")
        
        import traceback
        logger.error(f"   🔍 Stack trace: {traceback.format_exc()}")
        
        raise HTTPException(
            status_code=500, 
            detail=f"Erro no processamento LLM: {str(e)}"
        )


# 🔧 ENDPOINT DE TESTE SIMPLES
@router.post("/test")
async def test_llm_endpoint():
    """Endpoint simples para testar se o LLM está funcionando"""
    try:
        logger.info("🧪 Testando endpoint LLM...")
        
        # Teste mínimo
        settings = get_settings()
        embedder = get_embedder(settings)
        
        # Apenas gera embeddings de um texto simples
        test_embedding = embedder.embed_query("Teste de funcionamento")
        logger.info("✅ Teste LLM concluído com sucesso")
        
        return {
            "status": "success",
            "message": "LLM endpoint está funcionando",
            "embedding_size": len(test_embedding.dense) if hasattr(test_embedding, 'dense') else "N/A"
        }
        
    except Exception as e:
        logger.error(f"💥 Teste LLM falhou: {str(e)}")
        raise HTTPException(500, f"Teste falhou: {str(e)}")