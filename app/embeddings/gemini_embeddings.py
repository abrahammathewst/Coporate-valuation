from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config.settings import GEMINI_API_KEY

def get_gemini_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview", api_key=GEMINI_API_KEY)