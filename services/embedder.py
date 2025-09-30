class QueryEmbedder:
    def __init__(self, dense_model_name: str, bm25_model_name: str, late_interaction_model_name: str):
        self.dense_model_name = dense_model_name
        self.bm25_model_name = bm25_model_name  
        self.late_interaction_model_name = late_interaction_model_name
        self._dense_model = None
        self._bm25_model = None
        self._colbert_model = None
    
    @property
    def dense_model(self):
        if self._dense_model is None:
            from fastembed import TextEmbedding
            self._dense_model = TextEmbedding(self.dense_model_name)
        return self._dense_model
    
    @property 
    def bm25_model(self):
        if self._bm25_model is None:
            from fastembed.sparse.bm25 import Bm25
            self._bm25_model = Bm25(self.bm25_model_name)
        return self._bm25_model
    
    @property
    def colbert_model(self):
        if self._colbert_model is None:
            from fastembed.late_interaction import LateInteractionTextEmbedding
            self._colbert_model = LateInteractionTextEmbedding(self.late_interaction_model_name)
        return self._colbert_model
    
    def embed_query(self, query: str):
        # Use as properties que carregam lazy
        dense_embedding = list(self.dense_model.passage_embed([query]))[0].tolist()
        sparse_embedding = list(self.bm25_model.passage_embed([query]))[0].as_object()
        colbert_embedding = list(self.colbert_model.passage_embed([query]))[0].tolist()
        
        return {
            "dense": dense_embedding,
            "sparse": sparse_embedding,
            "colbertv2.0": colbert_embedding,
        }