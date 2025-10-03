import streamlit as st
from pathlib import Path
import sys
import time

st.write(sys.executable)

sys.path.append(str(Path(__file__).parent))

from source.config.config import config
from source.document_ingestion.document_preprocessor import DocumentProcessor
from source.vectorstore.vectore_store import VectorStore
from source.graph_builder.graph_build import GraphBuilder

st.set_page_config(
    page_title= "🤖 RAG Search",
    page_icon= "🔍",
    layout= "centered"
)
#st.session_state.history = []
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = None
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if 'history' not in st.session_state:
        st.session_state.history = []

@st.cache_resource
def initialize_rag():
    """Initialize the RAG system (cached)"""
    try:
        # Initialize components
        llm = config.get_llm()

        #doc_processor = DocumentProcessor(
        #    chunk_size=config.CHUNK_SIZE,
        #    chunk_overlap=config.CHUNK_OVERLAP
        #)

        vector_store = VectorStore()
        
        # Process documents
        #documents = doc_processor.load_files("data")
        
        # Create vector store
        #vector_store.create_vectorestore(documents)
        
        #load vectorstore
        vector_store.load_vectorestore("artifact")
        
        # Build graph
        graph_builder = GraphBuilder(
            retriever=vector_store.retriever,
            llm=llm, 
        )
        
        graph_builder.build()
        
        return graph_builder
    except Exception as e:
        st.error(f"Failed to initialize: {str(e)}")
        return None

def main():
    """Main application"""
    init_session_state()
    
    # Title
    st.title("🔍 RAG Document Search")
    st.markdown("Ask questions about the loaded documents")
    # Initialize system
    if not st.session_state.initialized:
        with st.spinner("Loading system..."):
            rag_system= initialize_rag()
            if rag_system:
                st.session_state.rag_system = rag_system
                st.session_state.initialized = True
                st.success(f"✅ System ready! ")
    
    st.markdown("---")
    
    # Search interface
    with st.form("search_form"):
        question = st.text_input(
            "Enter your question:",
            placeholder="What would you like to know?"
        )
        submit = st.form_submit_button("🔍 Search")
    
    # Process search
    if submit and question:
        if st.session_state.rag_system:
            with st.spinner("Searching..."):
                start_time = time.time()
                
                # Get answer
                result = st.session_state.rag_system.run(question, history= st.session_state.history)
                
                elapsed_time = time.time() - start_time
                
                print("Streamlit hist before",st.session_state.history)
                # Add to history
                st.session_state.history.append({
                    'query': question,
                    'answer': result['answer'],
                    'time': elapsed_time
                })
                print("Streamlit hist after",st.session_state.history)
                # Display answer
                st.markdown("### 💡 Answer")
                st.success(result['answer'])
                
                # Show retrieved docs in expander
                with st.expander("📄 Source Documents"):
                    for i, doc in enumerate(result['retrieved_doc'], 1):
                        st.text_area(
                            f"Document {i}",
                            doc.page_content[:300] + "...",
                            height=100,
                            disabled=True
                        )
                
                st.caption(f"⏱️ Response time: {elapsed_time:.2f} seconds")
    
    # Show history
    if st.session_state.history:
        st.markdown("---")
        st.markdown("### 📜 Recent Searches")
        
        for item in reversed(st.session_state.history[-3:]):  # Show last 3
            with st.container():
                st.markdown(f"**Q:** {item['query']}")
                st.markdown(f"**A:** {item['answer'][:200]}...")
                st.caption(f"Time: {item['time']:.2f}s")
                st.markdown("")

if __name__ == "__main__":
    main()