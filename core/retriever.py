from core.embedder import Embedder
from core.vector_store import VectorStore

class Retriever:
    
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        
    def retrieve_context(self,question,top_k=3):
        query_embedding = self.embedder.create_embeddings([question])[0]
        
        results = self.vector_store.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        return documents,metadatas