from langgraph.graph import StateGraph, END
from source.node.ReActnode import RAGNodes
from source.state.RAGState import RAGState

class GraphBuilder:

    def __init__(self, retriever, llm):
        self.node = RAGNodes(retriever, llm)
        self.graph = None

    def build(self):
        
        builder = StateGraph(RAGState)
        
        builder.add_node("generator", self.node.generate_answer)

        builder.set_entry_point("retriever")
        builder.add_edge("retriever","generator")
        builder.add_edge("generator", END)

        self.graph = builder.compile()

        return self.graph

    def run(self, question:str):
        if self.graph is None:
            self.graph = self.build()
        initial_state = RAGState(query=question)
        return self.graph.invoke(initial_state)
