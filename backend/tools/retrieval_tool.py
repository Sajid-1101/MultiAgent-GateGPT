import os
import sys

# Ensure backend directory is in python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from src.search_db import search_query

def get_context_and_sources(query: str):
    """
    Uses the existing FAISS vector database search_query logic to find relevant chunks.
    Formats the context string and lists unique sources with page numbers.
    
    Returns:
        (context_string, sources_list)
    """
    try:
        docs = search_query(
            query,
            doc_types=["book", "notes", "solved"]
        )
        concept_docs = []

        for doc in docs:
            if doc.metadata.get("type") in ["book", "notes", "solved"]:
                concept_docs.append(doc)

        docs = concept_docs

        context = ""
        sources = []
        for doc in docs:
            context += doc.page_content + "\n\n"
            source_path = doc.metadata.get("source", "Unknown")
            source_name = os.path.basename(source_path)
            # Pages are often 0-indexed in loaders; display as 1-indexed for users
            page = doc.metadata.get("page", 0) + 1
            source_info = f"{source_name} (Page {page})"
            if source_info not in sources:
                sources.append(source_info)
        return context, sources
    except Exception as e:
        return "", [f"Error loading FAISS index or retrieving context: {str(e)}"]
