from source.state.RAGState import RAGState

class RAGNode:

    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def retrieve_docs(self, state: RAGState):
        docs = self.retriever.invoke(state.query)
        return RAGState(
            query= state.query,
            retrieved_doc= docs
        )
    
    def generate_answer(self, state: RAGState):
        context = "\n\n".join(doc.page_content for doc in state.retrieved_doc)

        prompt = f"""
Answer the following question based on the context below.

context: 
{context}

Question: {state.query}

Ansewer:"""
        
        response = self.llm.invoke(prompt)
        
        return RAGState(
            query=  state.query,
            retrieved_doc = state.retrieved_doc,
            answer=response.content
        )