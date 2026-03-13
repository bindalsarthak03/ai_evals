class DocumentChunker:
    
    def __init__(self,chunk_size=200):
        self.chunk_size = chunk_size

    def chunk_text(self, text):

        chunks = [line.strip() for line in text.split("\n") if line.strip()]

        return chunks