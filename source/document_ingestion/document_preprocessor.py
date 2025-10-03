from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from typing import List, Union
from pathlib import Path
from langchain_community.document_loaders import (
    WebBaseLoader,
    PyPDFDirectoryLoader,
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader
)
import os

class DocumentProcessor:

    def __init__(self, chunk_size, chunk_overlap):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size,
                                                       chunk_overlap = chunk_overlap)
        
    def load_text_file(self, path: str) -> List[Document]:
        loader = TextLoader(path)
        return loader.load()
    
    def load_pdf_file(self, path: str) -> List[Document]:
        loader = PyPDFLoader(path)
        return loader.load()
    
    def load_docx_file(self, path: str) -> List[Document]:
        loader = Docx2txtLoader(path)
        return loader.load()
    
    def load_urls(self, url:str) -> List[Document]:
        loader = WebBaseLoader(url)
        return loader.load()
    
    def load_files(self, path) -> List[Document]:
        docs = []
        all_file = os.listdir(path)
        files_path = [os.path.join(path, file) for file in all_file]

        for file in files_path:
            file_path = Path(file)
            if file_path.suffix.lower() == ".pdf":
                loaded_file = self.load_pdf_file(str(file))
                docs.extend(loaded_file)

            elif file_path.suffix.lower () == ".docx":
                loaded_file = self.load_docx_file(str(file))
                docs.extend(loaded_file)

            elif file_path.suffix.lower() == ".txt":
                loaded_file = self.load_text_file(str(file))
                if "url.txt" in file.lower():
                    for url in loaded_file[0].page_content.split("\n"):
                        if url.startswith("https://") or url.startswith("http://"):
                            loaded_url = self.load_urls(url)
                            docs.extend(loaded_url)
                else:
                    docs.extend(loaded_file)
            else:
                print("this function only includes .pdf, .docx, .txt files")
        return docs
    
    def split_documents(self, document: List[Document]) -> List[Document]:
        """
        This Module splits the documents using RecursiveCharacterTextSplitter function.

        Input: List[Document]

        output: List[Document]


        """
        return self.splitter.split_documents(document)
    
