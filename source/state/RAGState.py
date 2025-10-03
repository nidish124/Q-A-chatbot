from typing import List
from pydantic import BaseModel
from langchain.schema import Document

class RAGState(BaseModel):
    query: str
    retrieved_doc: List[Document] = []
    answer: str = ""
    history: List[dict] = []
