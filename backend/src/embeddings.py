# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from dotenv import load_dotenv


# load_dotenv()


# def get_embedding_model():

#     embeddings = GoogleGenerativeAIEmbeddings(
#         model="models/gemini-embedding-001"
#     )


#     return embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os


load_dotenv()


os.environ["HF_TOKEN"] = os.getenv(
    "HF_TOKEN"
)


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_embedding_model():

    return embedding_model