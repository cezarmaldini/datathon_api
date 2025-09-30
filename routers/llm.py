from fastapi import APIRouter, Depends, HTTPException
from models.api import OpenAIRequest, OpenAIResponse
from services.retriever import QdrantRetriever
from services.embedder import QueryEmbedder
from services.llm_service import LLMService
from config.settings import Settings

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
    try:
        query_embeddings = embedder.embed_query(request.query)

        context_documents = retriever.search_documents(
            collection_name=request.collection_name, embeddings=query_embeddings, limit=request.limit
        )

        answer = openai_service.generate_response(
            query=request.query,
            context_documents=context_documents,
            model=request.model,
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        )

        return OpenAIResponse(answer=answer, source_documents=context_documents)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"OpenAI generation failed: {str(e)}"
        )