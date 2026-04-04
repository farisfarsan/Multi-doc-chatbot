# 📚 Multi-Document Chatbot

A Streamlit web app that lets you upload multiple documents and have a conversation with them. Powered by LangChain, OpenAI, and FAISS for semantic search.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.37.1-red?logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)
![LangChain](https://img.shields.io/badge/LangChain-0.2.16-green)

---

## ✨ Features

- 📄 **Multi-format support** — Upload PDF, TXT, and DOCX files
- 🔍 **RAG (Retrieval Augmented Generation)** — Answers are grounded in your documents
- 📎 **Source citations** — Every answer shows which document it came from
- ⚡ **Streaming responses** — Real-time token-by-token output
- 🧠 **Conversation memory** — Remembers the last 3 exchanges for context
- 💾 **Persistent vector store** — FAISS index survives container restarts
- 🗑️ **Document management** — Add or remove documents from the sidebar

---

## 🖥️ Demo

```
Upload a PDF → Ask a question → Get an answer with sources
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repository

```bash
git clone https://github.com/farisfarsan/Multi-doc-chatbot.git
cd Multi-doc-chatbot
```

### 2. Set up your environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run with Docker

```bash
docker-compose up --build
```

Then open your browser at **http://localhost:8501**

### 4. Stop the app

```bash
docker-compose down
```

---

## 🗂️ Project Structure

```
Multi-doc-chatbot/
├── app.py              # Streamlit UI and chat interface
├── chain.py            # LangChain RAG chain configuration
├── ingest.py           # Document loading, chunking, and FAISS indexing
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose configuration
├── .env.example        # Environment variable template
├── docs/               # Uploaded documents (auto-created, git-ignored)
└── vectorstore/        # FAISS index files (auto-created, git-ignored)
```

---

## ⚙️ How It Works

```
User uploads documents
        ↓
Documents are chunked with RecursiveCharacterTextSplitter
        ↓
Chunks are embedded using OpenAI Embeddings
        ↓
Embeddings are stored in a local FAISS vector store
        ↓
User asks a question
        ↓
Top relevant chunks are retrieved (MMR search)
        ↓
GPT-3.5-turbo generates an answer from the chunks
        ↓
Answer is streamed back with source citations
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | OpenAI GPT-3.5-turbo |
| Embeddings | OpenAI text-embedding-ada-002 |
| Vector Store | FAISS |
| RAG Framework | LangChain |
| Containerization | Docker |

---

## 📦 Running Without Docker

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes |

---

