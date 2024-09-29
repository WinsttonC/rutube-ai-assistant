import chromadb
from chromadb.api.types import EmbeddingFunction
from typing import Dict, List, Any


class ChromaDB:
    def __init__(self, embedding: EmbeddingFunction, collection_name: str, db_path: str = "./vector_db") -> None:
        """
        Initializes the ChromaDB class for interacting with ChromaDB.

        Args:
            embedding (EmbeddingFunction): Embedding function to use.
            collection_name (str): Name of the collection in ChromaDB.
            db_path (str): Path to the ChromaDB database.
        """
        self.embedding = embedding
        self.collection_name = collection_name
        self.chroma_client = chromadb.PersistentClient(path=db_path)

        self.collection = self.chroma_client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding,
            metadata={"hnsw:space": "cosine"},  # Options: 'l2', 'ip', 'cosine'
        )

    def add_documents(self, data_dict: Dict[str, List[Any]]) -> None:
        """
        Adds documents to the ChromaDB.

        Args:
            data_dict (dict): Dictionary containing the documents.
                              Must contain 'docs', 'cls_1', 'cls_2', 'sources', and 'ids' keys.
        """
        required_keys = {"docs", "cls_1", "cls_2", "sources", "ids"}
        if not required_keys.issubset(data_dict.keys()):
            raise ValueError(f"data_dict must contain keys: {required_keys}")

        docs = data_dict["docs"]
        cls_1 = data_dict["cls_1"]
        cls_2 = data_dict["cls_2"]
        sources = data_dict["sources"]
        ids = data_dict["ids"]

        metadatas = [{"source": sources[i], "cls_1": cls_1[i], "cls_2": cls_2[i]} for i in range(len(docs))]

        # Batch processing to avoid processing all documents at once
        batch_size = 100
        for start in range(0, len(docs), batch_size):
            end = start + batch_size
            self.collection.add(
                documents=docs[start:end],
                metadatas=metadatas[start:end],
                ids=ids[start:end],
            )

    def get_relevant_docs(self, user_query: str, n_results: int = 5):
        """
        Retrieves documents from ChromaDB that are relevant to the user's query.

        Args:
            user_query (str): The user's query.
            n_results (int): Number of results to return.

        Returns:
            QueryResult: An object containing metadatas, documents, and distances.
        """

        if self.collection.count() > 0:
            return self.collection.query(
                query_texts=user_query,
                include=["metadatas", "documents", "distances"],
                n_results=n_results,
            )
        else:
            return self.collection.query(
                query_texts=query,
                include=["metadatas", "documents", "distances"],
                n_results=1,
            )
