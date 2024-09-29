import pandas as pd
from db import ChromaDB
from language_model import llm_validation, llm_rag
from chromadb.utils import embedding_functions
import config

# Initialize embedding and vector store
embedding = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=config.EMBEDDING_MODEL_NAME)

vectorstore = ChromaDB(
    embedding=embedding,
    collection_name=config.COLLECTION_NAME,
    db_path=config.DB_PATH
)


def get_answer(query: str):
    docs = get_docs(query, vectorstore=vectorstore)
    
    if not docs or not docs['documents']:
        return {
            "answer": "К сожалению, в представленных документах я не нашел релевантного ответа. Уточните, пожалуйста, Ваш запрос",
            "class_1": None,
            "class_2": None
        }
    try:
        # clean_chunks = docs['metadatas'][0].get('docs_clean')
        cls_1 = docs['metadatas'][0].get('cls_1')
        cls_2 = docs['metadatas'][0].get('cls_2')
        str_docs = "\n".join(docs['documents'])
        # validated_docs = llm_validation(answer, str_docs)
        answer = llm_rag(query, str_docs) 
        answer =  llm_validation(answer, str_docs) # validated_docs
        result = {
            "answer": answer, 
            "class_1": cls_1, 
            "class_2": cls_2
        }
    except Exception as e:
        result = {
            "answer": "Произошла ошибка при обработке запроса",
            "class_1": None, 
            "class_2": None
        }

    return result

def prepare_data_for_vectorstore(df: pd.DataFrame):
    df['ids'] = [f"id_{i}" for i in range(len(df))]
    df['sources'] = [f"link_{i}" for i in range(len(df))]

    data = {
        "docs": df["concat"].tolist(),
        # "docs_clean": df["Ответ из БЗ"].tolist(),
        "cls_1": df["Классификатор 1 уровня"].tolist(),
        "cls_2": df["Классификатор 2 уровня"].tolist(),
        "sources": df["sources"].tolist(),
        "ids": df["ids"].tolist()
    }
    return data

def get_docs(query: str, vectorstore: ChromaDB, threshold: float = 0.45):
    result = vectorstore.get_relevant_docs(user_query=query)
    
    if not result:
        return {
            "metadatas": [],
            "documents": []
        }

    distances = result["distances"][0]
    metadatas = result["metadatas"][0]
    documents = result["documents"][0]

    # filtered_docs = {
    #     "metadatas": [meta for meta, dist in zip(result["metadatas"][0], result["distances"][0]) if dist < threshold],
    #     "documents": [doc for doc, dist in zip(result["documents"][0], result["distances"][0]) if dist < threshold],
    # }
    # return filtered_docs
    
    filtered_docs = {
        "metadatas": [meta for meta, dist in zip(metadatas, distances) if dist < threshold],
        "documents": [doc for doc, dist in zip(documents, distances) if dist < threshold],
    }
    return filtered_docs
