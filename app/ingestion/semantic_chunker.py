from langchain_experimental.text_splitter import SemanticChunker
from app.embeddings.hf_embeddings import HFEmbeddings


def create_semantic_chunks(documents):

    embeddings = HFEmbeddings()

    splitter = SemanticChunker(
        embeddings,
        breakpoint_threshold_type="percentile"
    )

    chunks = splitter.split_documents(documents)

    return chunks