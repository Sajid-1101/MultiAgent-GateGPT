from src.load_pdf import load_all_pdfs

from src.chunk_data import create_chunks

from src.create_vector_db import create_vector_store



print("Loading PDFs...")


docs = load_all_pdfs(
    "data"
)
print("\n========== SAMPLE METADATA ==========")

for i in range(5):
    print(docs[i].metadata)


print(
    "Total pages:",
    len(docs)
)



print("Creating chunks...")


chunks = create_chunks(
    docs
)



print(
    "Total chunks:",
    len(chunks)
)



print(
    "Creating FAISS database..."
)



create_vector_store(
    chunks
)



print(
    "Knowledge Base Created Successfully"
)
