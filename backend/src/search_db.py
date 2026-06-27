# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import FAISS
from src.embeddings import get_embedding_model


def search_query(query, doc_types=None, k=10):

    embeddings = get_embedding_model()

    db = FAISS.load_local(
        "vector_store/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    # Retrieve a larger pool first
    results = db.similarity_search(query, k=40)

    # Optional metadata filtering
    if doc_types is not None:
        results = [
            doc for doc in results
            if doc.metadata.get("type") in doc_types
        ]

    return results[:k]