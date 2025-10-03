from langgraph.graph import StateGraph, END
from source.node.ReActnode import RAGNodes
from source.state.RAGState import RAGState
from langgraph.checkpoint.memory import MemorySaver


class GraphBuilder:
    def __init__(self, retriever, llm):
        self.node = RAGNodes(retriever, llm)
        self.graph = None

    def build(self):
        
        memory  = MemorySaver()
        builder = StateGraph(RAGState)
        
        builder.add_node("retriever", self.node.retrieve_docs)
        builder.add_node("generator", self.node.generate_answer)

        builder.set_entry_point("retriever")
        builder.add_edge("retriever","generator")
        builder.add_edge("generator", END)

        self.graph = builder.compile(checkpointer= memory)

        return self.graph

    def run(self, question:str, history):
        if self.graph is None:
            self.graph = self.build()
        configuration = {"configurable": {"thread_id": "1"}}
        initial_state = RAGState(query=question, history=history)
        
        return self.graph.invoke(initial_state, config=configuration)
