from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings


_model = None


def get_embedding_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "BAAI/bge-large-en-v1.5",
            device="cuda",
            local_files_only=True
        )

    return _model


class HFEmbeddings(Embeddings):

    def __init__(self):
        self.model = get_embedding_model()

    def embed_documents(self, texts):
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embeddings.tolist()

    def embed_query(self, text):
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()