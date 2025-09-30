from typing import List
from models.embeddings import Document, QueryEmbeddings
from config.settings import Settings
from config import clients
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Filter, FieldCondition, MatchValue
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class QdrantRetriever:
    def __init__(self, settings: Settings):
        self.client = clients.new_qdrant_client(settings)
        self.prefetch_limit = settings.qdrant_prefetch_limit

    def search_documents(
        self, collection_name: str, embeddings: QueryEmbeddings, limit: int = 5
    ) -> List[Document]:
        # 🔧 LOG INICIAL
        logger.info(f"🔍 INICIANDO BUSCA - Coleção: {collection_name}, Limit: {limit}")
        
        try:
            # 🔧 LOG ANTES DA CONSULTA
            logger.info(f"🎯 Executando query_points no Qdrant...")
            
            # Search using all vector types
            search_result = self.client.query_points(
                collection_name=collection_name,
                # First stage: Get candidates using dense and sparse search
                prefetch=[
                    {
                        "query": embeddings.dense,
                        "using": "dense",
                        "limit": self.prefetch_limit,
                    },
                    {
                        "query": embeddings.sparse_bm25.model_dump(),
                        "using": "sparse",
                        "limit": self.prefetch_limit,
                    },
                ],
                # Second stage: Rerank using late interaction
                query=embeddings.late,
                using="colbertv2.0",
                with_payload=True,
                limit=limit,
            )

            # 🔧 LOG APÓS CONSULTA BEM-SUCEDIDA
            logger.info(f"✅ BUSCA CONCLUÍDA - {len(search_result.points)} documentos encontrados")

            # Convert results to Document objects
            return [
                Document(
                    page_content=point.payload.get("text", ""),
                    metadata=point.payload.get("metadata", {}),
                )
                for point in search_result.points
            ]

        except UnexpectedResponse as e:
            # 🔧 LOG DE ERRO QDRANT
            logger.error(f"💥 ERRO QDRANT - Status: {e.status_code}, Mensagem: {e.content}")
            logger.error(f"📋 Detalhes: {str(e)}")
            
            # Handle Qdrant-specific errors
            logger.error(
                "Qdrant search failed",
                extra={"error": str(e), "collection": collection_name},
            )
            raise HTTPException(
                status_code=503, detail="Search service temporarily unavailable"
            )
        except Exception as e:
            # 🔧 LOG DE ERRO GENÉRICO
            logger.error(f"💥 ERRO INESPERADO - Tipo: {type(e).__name__}")
            logger.error(f"📋 Mensagem: {str(e)}")
            import traceback
            logger.error(f"🔍 Stack Trace: {traceback.format_exc()}")
            
            # Handle any other errors
            logger.error(
                "Unexpected error during search",
                extra={"error": str(e), "collection": collection_name},
            )
            raise HTTPException(status_code=500, detail="Internal server error")