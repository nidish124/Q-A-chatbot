from pathlib import Path
import sys
import time

from source.config.config import config
from source.document_ingestion.document_preprocessor import DocumentProcessor
from source.vectorstore.vectore_store import VectorStore

def main():
    doc_processor = DocumentProcessor(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP)
    
    vector_store = VectorStore()
    documents = doc_processor.load_files("data")
    vector_store.create_vectorestore(documents, "artifact")

if __name__ == "__main__":
    main()
