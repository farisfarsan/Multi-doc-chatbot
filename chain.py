import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

def get_chain():
    embeddings = OpenAIEmbeddings()

    # Check if vectorstore index exists before loading
    if not os.path.exists("vectorstore/index.faiss"):
        return None, None

    vectorstore = FAISS.load_local(
        'vectorstore', embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(
        search_type='mmr',
        search_kwargs={'k': 10, 'fetch_k': 20}
    )
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, streaming=True)

    prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question based only on the context below.
If the answer is not in the context, say "I don't know based on the uploaded documents."

Context:
{context}

Question: {question}

Answer:
""")

    def format_docs(docs):
        formatted = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get('source', 'Unknown')
            formatted.append(f"[Source {i+1}: {source}]\n{doc.page_content}")
        return "\n\n".join(formatted)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever