import os
import sys

# Ensure backend directory is in python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from src.embeddings import get_embedding_model
# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import FAISS

def get_pyq_context_and_sources(query: str, k: int = 5):
    """
    Retrieves previous year question (PYQ) context by running a similarity search
    with a larger pool and prioritizing/filtering for documents indicating exam questions.
    
    Returns:
        (context_string, sources_list)
    """
    try:
        embeddings = get_embedding_model()
        # Relative path from backend directory
        index_path = os.path.join(backend_dir, "vector_store", "faiss_index")
        
        db = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # Search for a larger pool of candidates to filter
        raw_results = db.similarity_search(query, k=50)
        print("\n========== RAW RESULTS ==========\n")

        for i, doc in enumerate(raw_results[:5]):
            print(f"Document {i+1}")
            print(doc.metadata)
            print("-" * 50)
        
        pyq_results = []
        for doc in raw_results:
            # source_path = doc.metadata.get("source", "")
            # filename = os.path.basename(source_path).lower()
            
            # # Identify if it is a PYQ file (either contains 'pyq' or is a year-wise paper like CS2019.pdf)
            # is_pyq = (
            #     "pyq" in filename 
            #     or filename.startswith("cs20") 
            #     or filename.startswith("cs12") 
            #     or filename.startswith("cs22")
            # )
            if doc.metadata.get("type") in ["pyq_subject", "pyq_year"]:
                pyq_results.append(doc)

                if len(pyq_results) >= k:
                    break
            print("\n========== FILTERED PYQ RESULTS ==========\n")

            for i, doc in enumerate(pyq_results):
                print(f"Document {i+1}")
                print(doc.metadata)
                print("-" * 60)        
            
                
        # If no PYQ-specific results are found, fallback to the raw similarity results
        if not pyq_results:
            return "", []
            
        context = ""
        sources = []
        for doc in pyq_results:
            context += doc.page_content + "\n\n"
            source_path = doc.metadata.get("source", "Unknown")
            source_name = os.path.basename(source_path)
            page = doc.metadata.get("page", 0) + 1
            source_info = f"{source_name} (Page {page})"
            if source_info not in sources:
                sources.append(source_info)
        
        return context, sources
        
    except Exception as e:
        return "", [f"Error retrieving PYQ context: {str(e)}"]
