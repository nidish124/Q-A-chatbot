# Q-A Chatbot 🤖

A **Retrieval-Augmented Generation (RAG)** based Question–Answering chatbot built using **LangChain, LangGraph, FAISS, Azure AI Services, FastAPI, and Docker**.

This system answers **domain-specific queries** by retrieving relevant context from internal documents and generating **accurate, structured responses** using LLMs.

---

## 📌 Features

- **Retrieval-Augmented Generation (RAG)**  
  Combines vector embeddings and FAISS-based similarity search with LLM reasoning.

- **Multi-step Agent Workflow**  
  Deterministic **LangGraph** pipeline for query parsing, retrieval, reasoning, and response generation.

- **FastAPI Backend**  
  RESTful APIs for real-time question answering.

- **Dockerized Deployment**  
  Fully containerized for consistent local and cloud deployment.

- **Azure Integration**  
  Uses **Azure AI Services** for embeddings and inference.

- **Scalable Architecture**  
  Supports large document sets with chunking, embeddings, and relevance scoring.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Frameworks:** FastAPI, LangChain, LangGraph  
- **Vector Store:** FAISS  
- **Cloud Services:** Azure AI Services, Azure Blob Storage  
- **Deployment:** Docker, GitHub Actions (CI/CD)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker
- Azure AI Services account (for embeddings and inference)

---

### Installation

```bash
# Clone the repository
git clone https://github.com/nidish124/Q-A-chatbot.git
cd Q-A-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### RUN Locally
```
# Start FastAPI server
uvicorn app.main:app --reload
```

### Run with Docker
```
# Build Docker image
docker build -t qachatbot .

# Run container
docker run -p 8000:8000 qachatbot
```

## 📂 Project Structure

```
Q-A-chatbot/
│── app/
│   ├── main.py          # FastAPI entry point
│   ├── retrieval.py     # FAISS + LangChain retrieval logic
│   ├── agent.py         # LangGraph workflow
│── data/                # Source documents for embeddings
│── requirements.txt     # Python dependencies
│── Dockerfile           # Container configuration
│── README.md            # Project documentation
```

## 🎯 Use Cases

Internal knowledge base Q&A

Insurance and finance document retrieval

Customer support automation

Policy interpretation using LLM reasoning

## 👤 Author

Nidish M
AI / ML Engineer

LinkedIn: Add link

Email: Add email