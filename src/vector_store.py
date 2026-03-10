import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self,collection_name="documents"):
        self.client = chromadb.Client(
            Settings(
                persist_directory="./chroma_db",
                is_persistent=True
            )
)
        self.collection = self.client.get_or_create_collection(name = collection_name)
        
    def add_documents(self,documents,embeddings, file_name):
        ids = [f"id_{i}" for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source":file_name} for _ in documents]
        )
        
    def query(self,query_embedding,top_k=3):
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return resules["documents"][0]
    
        