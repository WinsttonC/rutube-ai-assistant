import pandas as pd
from chromadb.utils import embedding_functions
from db import ChromaDB
from utils import prepare_data_for_vectorstore
import config
import os

os.environ["TOKENIZERS_PARALLELISM"] = "true"


def main():
    # Load data from CSV
    df = pd.read_csv(config.DATA_FILE_PATH)

    # Initialize embedding function
    embedding = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=config.EMBEDDING_MODEL)

    # Initialize ChromaDB
    vectorstore = ChromaDB(embedding=embedding, collection_name=config.COLLECTION_NAME, db_path=config.DB_PATH)
    # Prepare and add documents to vector store
    data = prepare_data_for_vectorstore(df)
    vectorstore.add_documents(data)
    print(f"Added documents to the collection '{config.COLLECTION_NAME}'.")


if __name__ == "__main__":
    main()
