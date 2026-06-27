# from langchain_community.document_loaders import PyPDFLoader

# import os


# def load_all_pdfs(folder_path):

#     documents = []

#     failed_files = []


#     for file in os.listdir(folder_path):

#         if file.endswith(".pdf"):

#             try:

#                 pdf_path = os.path.join(
#                     folder_path,
#                     file
#                 )


#                 print(
#                     "Loading:",
#                     file
#                 )


#                 loader = PyPDFLoader(
#                     pdf_path
#                 )


#                 pages = loader.load()


#                 print(
#                     "Pages:",
#                     len(pages)
#                 )


#                 documents.extend(
#                     pages
#                 )


#             except Exception as e:

#                 print(
#                     "Skipping corrupted PDF:",
#                     file
#                 )

#                 failed_files.append(file)


#     print("\nFailed PDFs:")

#     for file in failed_files:

#         print(file)


#     return documents
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader
import os


def load_all_pdfs(folder_path):
    documents = []
    failed_files = []

    # Folder name -> metadata type
    folder_type_map = {
        "Books": "book",
        "ShortNotes": "notes",
        "PyqSubjectWise": "pyq_subject",
        "PyqYearWise": "pyq_year",
        "SolvedPaper": "solved"
    }

    # Walk through every subfolder recursively
    for root, _, files in os.walk(folder_path):

        folder_name = os.path.basename(root)
        doc_type = folder_type_map.get(folder_name, "unknown")

        for file in files:

            if not file.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(root, file)

            try:
                print(f"Loading: {file}")

                loader = PyPDFLoader(pdf_path)
                pages = loader.load()

                print(f"Pages: {len(pages)}")

                # Attach metadata to every page
                for page in pages:

                    page.metadata["type"] = doc_type
                    page.metadata["source"] = file

                    # Store category for later use
                    page.metadata["category"] = folder_name

                documents.extend(pages)

            except Exception as e:

                print(f"Skipping corrupted PDF: {file}")
                print(e)
                failed_files.append(file)

    print("\nFailed PDFs:")

    for file in failed_files:
        print(file)

    return documents