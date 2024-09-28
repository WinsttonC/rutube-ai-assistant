import pandas as pd
from db import Chroma
from language_model import llm_validation, llm_rag


EMBEDDING_MODEL = "deepvk/USER-bge-m3"
df = pd.read_csv('../data/concat_data.csv')

embedding = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)

data = prepare_data_for_vectorstore(df)
vectorstore = Chroma(
    embedding = embedding, 
    collection_name='qa_data'
)

vectorstore.add_docs(data)


def get_answer(query):
    docs = get_docs(query, vectorstore)

    cls_1 = docs['metadatas'][0]['cls_1']
    cls_2 = docs['metadatas'][0]['cls_2']

    str_docs = "\n".join(docs['documents'])
    validated_docs = llm_validation(query, str_docs)
    answer = llm_rag(query, str_docs)

    result = {
        "answer": answer, 
        "class_1": cls_1, 
        "class_2": cls_2
        }

    return result


def prepare_data_for_vectorstore(df):
    df['ids'] = [f"id_{i}" for i in range(len(df))]
    df['sources'] = [f"link_{i}" for i in range(len(df))]

    data = {
        "docs": df["concat"].tolist(),
        "cls_1": df["Классификатор 1 уровня"].tolist(),,
        "cls_2": df["Классификатор 2 уровня"].tolist(),,
        "sources": df["sources"].tolist(),
        "ids": df["ids"].tolist()
    }

    return data


def get_docs(query, vectorstore, threshold=0.7):
    result = vectorstore.get_relevant_docs(user_query=query)
    docs = {
        "metadatas": [meta for meta, dist in zip(data["metadatas"], data["distances"]) if dist < threshold],
        "documents": [doc for doc, dist in zip(data["documents"], data["distances"]) if dist < threshold],
    }
    return docs