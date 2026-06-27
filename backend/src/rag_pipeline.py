from src.search_db import search_query
from src.gemini_llm import ask_gemini



def get_rag_response(question):


    documents = search_query(
        question
    )


    context = ""


    for doc in documents:

        context += doc.page_content + "\n"



    response = ask_gemini(
        context,
        question
    )


    return response