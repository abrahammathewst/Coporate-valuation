from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader

def load_pdf(file_path: str):
    pdf_file = Path(file_path)
    if not pdf_file.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()

    if not documents:
        raise ValueError(f"No documents were loaded from the file {file_path}.")
    return documents