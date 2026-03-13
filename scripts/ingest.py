from chunker import DocumentChunker
from embedder import Embedder
from vector_store import VectorStore
import os


def ingest_documents(file_path):

    with open(file_path, "r") as f:
        text = f.read()
    file_name = os.path.basename(file_path)
    print("Document loaded")

    chunker = DocumentChunker()
    chunks = chunker.chunk_text(text)

    print("Chunks created:", chunks)

    embedder = Embedder()
    embeddings = embedder.create_embeddings(chunks)

    print("Embeddings created")

    vector_store = VectorStore()

    try:
        vector_store.add_documents(chunks, embeddings,file_name)
        print("Documents stored successfully!")
    except Exception as e:
        print("Error storing documents:", e)


if __name__ == "__main__":
    ingest_documents("data/sample_doc.txt")