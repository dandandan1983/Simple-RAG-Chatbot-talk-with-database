import chromadb
from chromadb import Settings

from config import CHROMADB_COLLECTION_NAME, CHROMADB_DIR

class ChromaDBManager:
    def __init__(self):
        self.set_path_to_db(CHROMADB_DIR)
        self.client = chromadb.Client(Settings(allow_reset=True))
        self.create_or_set_collection_name(CHROMADB_COLLECTION_NAME)

    def set_path_to_db(self, path="./chroma_db"):
        chromadb.PersistentClient(path=path)

    def create_or_set_collection_name(self, collection="pdf_chunks"):
        self.collection = self.client.get_or_create_collection(collection)


    def add_documents(self, chunks, metadata=None):
        """Add document chunks to the vector database."""
        if metadata is None:
            metadata = [{}] * len(chunks)

        self.collection.add(
            documents=chunks,
            ids=[f"doc_{i}" for i in range(len(chunks))],
            metadatas=metadata
        )

    def search_documents(self, query, n_results=3):
        """Search for relevant documents based on query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def clear_db(self):
        self.client.reset()
        self.create_or_set_collection_name(CHROMADB_COLLECTION_NAME)
