from fastembed import TextEmbedding
from fastembed.sparse.bm25 import Bm25
from models.embeddings import QueryEmbeddings, SparseVector
from fastembed.late_interaction import LateInteractionTextEmbedding


class QueryEmbedder:
    def __init__(
        self,
        dense_model_name: str,
        bm25_model_name: str,
        late_interaction_model_name: str,
    ):
        self.dense_embedding_model = TextEmbedding(dense_model_name)
        self.bm25_embedding_model = Bm25(bm25_model_name)
        self.late_interaction_model = (LateInteractionTextEmbedding(late_interaction_model_name))

    def embed_query(self, query: str) -> QueryEmbeddings:
        dense_vector = next(self.dense_embedding_model.embed(query)).tolist()

        sparse_vector = next(self.bm25_embedding_model.embed(query))

        late_vector = next(self.late_interaction_model.embed(query)).tolist()

        return QueryEmbeddings(
            dense=dense_vector,
            sparse_bm25=SparseVector(**sparse_vector.as_object()),
            late=late_vector,
        )