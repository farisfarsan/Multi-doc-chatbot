# 📚 Multi-Document Chatbot

A Streamlit-based web application that allows users to upload multiple documents (PDF, TXT, DOCX) and converse with them. Powered by LangChain, OpenAI's Large Language Models, and FAISS for efficient similarity search.

## ✨ Features

- **Document Management:** Upload, index, and manage multiple documents (PDF, TXT, DOCX) from the application sidebar.
- **Retrieval Augmented Generation (RAG):** Ask questions, and the chatbot answers based on the context of your uploaded documents.
- **Source Snippets:** The chatbot provides citations, indicating exactly which document generated the particular response.
- **Streaming Responses:** Get real-time response streaming for a better user experience.
- **Conversation Memory:** The chatbot retains context of the conversation using chat memory.
- **Local Vector Storage:** Uses FAISS to save indexed documents locally, so you don't need to re-index items after restarting the application.

## 🚀 Getting Started

### Prerequisites

You will need Python 3.8+ installed on your system.

### 1. Clone or Download the Repository

Make sure all files (`app.py`, `chain.py`, `ingest.py`, and `requirements.txt`) are in a single directory.

### 2. Set Up a Virtual Environment (Recommended)

```bash
python -m venv multivenv
source multivenv/bin/activate  # On Windows use: multivenv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages using:

```bash
pip install -r requirements.txt
```

### 4. Configuration

The application requires an OpenAI API key. Create a `.env` file in the root directory and add your key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Running the Application

Start the Streamlit application by running the following command:

```bash
streamlit run app.py
```

## 🧠 Application Structure

- `app.py`: The main Streamlit web application frontend. Handles the UI, document upload sidebar, and chat interface.
- `chain.py`: Configures the LangChain retrieval and conversation logic using OpenAI and FAISS.
- `ingest.py`: Handles loading documents, chunking the content (with `RecursiveCharacterTextSplitter`), and creating/saving the local FAISS vector store.
- `docs/`: Directory where uploaded user documents are temporarily stored.
- `vectorstore/`: Directory where FAISS saves its local index data.
