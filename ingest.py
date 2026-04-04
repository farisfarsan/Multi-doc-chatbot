from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def load_documents(docs_dir='docs/'):
    loaders = {
        '.pdf':  PyPDFLoader,
        '.txt':  TextLoader,
        '.docx': Docx2txtLoader,
    }
    all_docs = []
    for filename in os.listdir(docs_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext in loaders:
            path = os.path.join(docs_dir, filename)
            docs = loaders[ext](path).load()
            # Tag each chunk with its source filename
            for doc in docs:
                doc.metadata['source'] = path
            all_docs.extend(docs)
            print(f'Loaded: {filename} ({len(docs)} pages)')
    print(f'Total pages loaded: {len(all_docs)}')
    return all_docs

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = splitter.split_documents(docs)
    print(f'Total chunks created: {len(chunks)}')
    return chunks

def create_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local('vectorstore')
    print(f'Vectorstore saved with {len(chunks)} chunks.')

if __name__ == '__main__':
    docs = load_documents()
    chunks = split_documents(docs)
    create_vectorstore(chunks)
