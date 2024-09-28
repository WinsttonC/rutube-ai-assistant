import chromadb
from chromadb.api.types import EmbeddingFunction, QueryResult
import chromadb.utils.embedding_functions as embedding_functions


class Chroma:
    def __init__(
        self,
        embedding: EmbeddingFunction,
        collection_name: str,
        path: str = './vector_db_bge_3'
    ) -> None:
        """
        Инициализирует класс для работы с ChromaDB. Используется для первоначальной загрузки данных в БД.
        Args:
            embedding (EmbeddingFunction): функция эмбеддинга.
            collection_name (str): название коллекции в ChromaDB.

        """
        self.embedding = embedding
        self.collection_name = collection_name
        self.chroma_client = chromadb.PersistentClient(path=path)

        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding,
            metadata={"hnsw:space": "cosine"} # доступны по дефолту l2 (Squared L2), Inner product (ip), cosine (Cosine similarity)  
        )

    def add_docs(self, data_dict: dict) -> None:
        """
        Adds documents to the ChromaDB.
        
        Args:
            data_dict (dict): Dictionary representing the documents. 
                                Must contain 'docs', cls_1, cls_2, 'sources', 'questions', and 'ids' fields.
        """
        docs = data_dict.get("docs")
        cls_1 = data_dict.get("cls_1")
        cls_2 = data_dict.get("cls_1")
        sources = data_dict.get("sources")
        ids = data_dict.get("ids")

        if not all([docs, sources, ids, cls_1, cls_2]):
            raise ValueError("data_dict must contain 'docs', 'cls_1', 'cls_2', 'sources' and 'ids' fields.")

        metadatas = [
            {"source": sources[i],
             "cls_1": cls_1[i],
             "cls_2": cls_2[i]} for i in range(len(docs))
        ]

        # Batch processing, чтобы все доки за один раз не обрабатывать 
        for start in range(0, len(docs), 100):
            end = start + 100
            self.collection.add(
                documents=docs[start:end],
                metadatas=metadatas[start:end],
                ids=ids[start:end],
            )

    def get_relevant_docs(self, user_query: str):
        """
        Получает документы из ChromaDB, удовлетворяющие пользовательскому запросу.
        Args:
            query (str): пользовательский запрос.
            collection_name (str): название коллекции ChromaDB, где находятся документы.
            embedding_info (dict): информация об эмбеддинге.
        Returns:
            Объект QueryResult с аттрибутами metadatas, documents и distances.
        """
        # user_query = self.embedding(user_query)
                
        if self.collection.count() > 0:
            return self.collection.query(
                query_texts=user_query,
                include=["metadatas", "documents", "distances"],
                n_results=5,
            )
        else:
            return collection.query(
                query_texts=query,
                include=["metadatas", "documents", "distances"],
                n_results=1,
            )