from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from typing import List

class VectorStore:
    def __init__(self):
        self.retriever = None
        self.vectorstore = None
        self.embedding = OpenAIEmbeddings()
        self.MAX_DOC_RETIVAL = 3

    def create_vectorestore(self, document: List[Document], path):
        self.vectorstore = FAISS.from_documents(documents=document, embedding=self.embedding)
        self.vectorstore.save_local(path)

    def load_vectorestore(self, path):
        self.load_vect = FAISS.load_local(path, self.embedding, allow_dangerous_deserialization=True)
        self.retriever = self.load_vect.as_retriever(search_kwarg = {"k":self.MAX_DOC_RETIVAL}, search_type = "mmr")

    def get_retriever(self):
        if self.retriever == None:
            raise ValueError("Please create the retriever first.")
        else:
            return self.retriever
        
    def retrieve(self, query: str):
        if self.retriever == None:
            raise ValueError("Please create the retriever first.")
        else:
            return self.retriever.invoke(query)