from source.state.RAGState import RAGState
from langgraph.prebuilt import create_react_agent
from langchain.tools import Tool
from typing import List
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage

from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class RAGNodes:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm
        self.agent = None

    def retrieve_docs(self, state: RAGState):
        docs = self.retriever.invoke(state.query)
        return RAGState(
            query=state.query,
            retrieved_doc=docs,
            history=state.history
        )

    def Build_agent_tools(self):
        def retriver_toll_func(query: str) -> str:
            docs: List[Document] = self.retriever.invoke(query)
            if not docs:  
                return "No documents found."
            merged = []
            for i, d in enumerate(docs[:8], start=1):
                meta = d.metadata if hasattr(d, "metadata") else {}
                title = meta.get("title") or meta.get("source") or f"doc_{i}"
                merged.append(f"[{i}] {title}\n{d.page_content}")
            return "\n\n".join(merged)

        wiki = WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(top_k_results = 3, lang= "en")
        )

        retriver_tool = Tool(name = "retriever", description= "Fetch passages from indexed corpus.", func= retriver_toll_func)
        wiki_tool = Tool(name = "wikipedia", description= "Search Wikipedia for general knowledge.", func= wiki.run)

        tools = [retriver_tool,wiki_tool]

        return tools

    def build_agent(self):
        tools = self.Build_agent_tools()
        system_prompt = ("You are a helpful RAG agent. "
            "Prefer 'retriever' for user-provided docs; use 'wikipedia' for general knowledge. "
            "Return only the final useful answer."
            )
            
        self.agent = create_react_agent(self.llm, tools = tools, prompt=system_prompt)
        return self.agent

    def generate_answer(self, state: RAGState):
        if self.agent is None:
            self.agent = self.build_agent()
        messages = []
        if state.history:
            for turn in state.history:
                messages.append(HumanMessage(content=turn['query']))
                messages.append(AIMessage(content= turn['answer']))
        messages.append(HumanMessage(content = state.query))
        result = self.agent.invoke({"messages": messages})
        
        messages_out = result.get("messages", [])
        answer: str = ''
        if messages_out:
            answer_msg = messages_out[-1]
            #answer = getattr(answer_msg, "content", None)
            answer = answer_msg.content
        new_history = (state.history or []) + [{"query":state.query, "answer": answer}]
        return RAGState(
            query=state.query,
            retrieved_doc=state.retrieved_doc,
            answer = answer or "could not found the answer.",
            history=new_history
        )

        
        