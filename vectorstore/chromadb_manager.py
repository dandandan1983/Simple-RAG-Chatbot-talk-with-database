import chromadb
from chromadb import Settings

from config import CHROMADB_COLLECTION_NAME, CHROMADB_DIR

class ChromaDBManager:
    def __init__(self):
        self.set_path_to_db(CHROMADB_DIR)
        self.client = chromadb.Client(Settings(allow_reset=True))
        # self.create_or_set_collection_name(CHROMADB_COLLECTION_NAME)
        self.create_or_check_collection(CHROMADB_COLLECTION_NAME)

    def set_path_to_db(self, path="./chroma_db"):
        chromadb.PersistentClient(path=path)

    def create_or_set_collection_name(self, collection):
        self.collection = self.client.get_or_create_collection(collection)

    def create_or_check_collection(self, collection_name):
        """Check if a collection exists, and create it if it doesn't."""
        existing_collections = self.client.list_collections()  # Получаем список всех коллекций

        # Проверяем, существует ли коллекция с нужным именем
        for collection in existing_collections:
            if collection.name == collection_name:  # Доступ к имени коллекции через атрибут
                self.collection = self.client.get_collection(collection_name)  # Получаем существующую коллекцию
                return True

        # Если коллекция не найдена, создаем новую
        self.collection = self.client.create_collection(collection_name)

    def add_documents(self, chunks, metadata=None):
        """Add document chunks to the vector database."""
        if metadata is None:
            metadata = [{}] * len(chunks)

        self.collection.add(
            documents=chunks,
            ids=[f"doc_{i}" for i in range(len(chunks))],
            metadatas=metadata
        )

    def search_documents(self, query, n_results=5):
        """Search for relevant documents based on query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def clear_db(self):
        self.client.reset()
        self.create_or_set_collection_name(CHROMADB_COLLECTION_NAME)

    def get_all_documents(self):
        """Retrieve all documents from the collection."""
        # Указываем пустой запрос или используем специальные параметры
        results = self.collection.query(
            query_texts=[""],  # Пустой текст для запроса
            n_results=self.collection.count()  # Получаем общее количество записей
        )
        return results

    def get_total_records(self):
        total_records = self.collection.count()
        return total_records