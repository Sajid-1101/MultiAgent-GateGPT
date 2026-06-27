# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import FAISS

from src.embeddings import get_embedding_model


def create_vector_store(chunks):

    embeddings = get_embedding_model()


    vector_db = FAISS.from_documents(
        chunks,
        embeddings
    )


    vector_db.save_local(
        "vector_store/faiss_index"
    )


    return vector_db