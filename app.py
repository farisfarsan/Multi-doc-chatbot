import streamlit as st
import os
import shutil
from chain import get_chain
from ingest import load_documents, split_documents, create_vectorstore

st.set_page_config(
    page_title='Multi-Doc Chatbot',
    page_icon='📚',
    layout='wide'
)

st.title('📚 Multi-Document Chatbot')
st.caption('Ask questions about your uploaded documents')

DOCS_DIR = 'docs/'
os.makedirs(DOCS_DIR, exist_ok=True)

# ── Sidebar ──
with st.sidebar:
    st.header('📁 Document Manager')

    # Upload
    st.subheader('➕ Upload Documents')
    uploaded_files = st.file_uploader(
        'Upload PDF, TXT, or DOCX files',
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True
    )
    if uploaded_files:
        if st.button('📥 Save & Index Documents', use_container_width=True):
            for file in uploaded_files:
                with open(os.path.join(DOCS_DIR, file.name), 'wb') as f:
                    f.write(file.read())
            with st.spinner('Indexing documents...'):
                docs = load_documents()
                chunks = split_documents(docs)
                create_vectorstore(chunks)
                chain, retriever = get_chain()
                st.session_state.chain = chain
                st.session_state.retriever = retriever
            st.success(f'✅ {len(uploaded_files)} document(s) indexed!')
            st.rerun()

    st.divider()

    # Existing docs
    st.subheader('🗂️ Your Documents')
    allowed = ['.pdf', '.txt', '.docx']
    existing_files = [
        f for f in os.listdir(DOCS_DIR)
        if os.path.splitext(f)[1].lower() in allowed
    ]
    if existing_files:
        for filename in existing_files:
            col1, col2 = st.columns([3, 1])
            with col1:
                ext = os.path.splitext(filename)[1].lower()
                icon = '📄' if ext == '.pdf' else '📝' if ext == '.txt' else '📃'
                st.write(f'{icon} {filename}')
            with col2:
                if st.button('🗑️', key=f'del_{filename}'):
                    os.remove(os.path.join(DOCS_DIR, filename))
                    remaining = [
                        f for f in os.listdir(DOCS_DIR)
                        if os.path.splitext(f)[1].lower() in allowed
                    ]
                    if remaining:
                        with st.spinner('Re-indexing...'):
                            docs = load_documents()
                            chunks = split_documents(docs)
                            create_vectorstore(chunks)
                            chain, retriever = get_chain()
                            st.session_state.chain = chain
                            st.session_state.retriever = retriever
                    else:
                        shutil.rmtree('vectorstore')
                        os.makedirs('vectorstore', exist_ok=True)
                        st.session_state.pop('chain', None)
                        st.session_state.pop('retriever', None)
                    st.rerun()
    else:
        st.info('No documents yet. Upload some above!')

    st.divider()

    # Memory toggle
    st.subheader('🧠 Chat Memory')
    use_memory = st.toggle('Remember conversation', value=True)
    if st.button('🧹 Clear Chat History', use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ── Load chain (only if index files actually exist) ──
if 'chain' not in st.session_state:
    if os.path.exists('vectorstore/index.faiss'):
        with st.spinner('Loading document index...'):
            chain, retriever = get_chain()
            if chain is not None:
                st.session_state.chain = chain
                st.session_state.retriever = retriever

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ── No docs warning ──
if not os.path.exists('vectorstore/index.faiss') or st.session_state.get('chain') is None:
    st.warning('⬅️ Please upload at least one document to get started!')
    st.stop()

# ── Welcome message ──
if len(st.session_state.messages) == 0:
    with st.chat_message('assistant'):
        st.markdown('👋 Hello! I have read your documents. Ask me anything!')

# ── Display chat history ──
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])
        if 'sources' in msg and msg['sources']:
            with st.expander('📎 Sources'):
                for src in msg['sources']:
                    st.caption(f"📄 {src}")

# ── Handle input ──
if prompt := st.chat_input('Ask a question about your documents...'):

    # Build prompt with memory
    if use_memory and st.session_state.chat_history:
        history_text = "\n".join([
            f"User: {h['question']}\nAssistant: {h['answer']}"
            for h in st.session_state.chat_history[-3:]
        ])
        full_prompt = f"Previous conversation:\n{history_text}\n\nNew question: {prompt}"
    else:
        full_prompt = prompt

    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        # Streaming
        response_placeholder = st.empty()
        full_response = ""
        for chunk in st.session_state.chain.stream(full_prompt):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")
        response_placeholder.markdown(full_response)

        # Sources
        docs = st.session_state.retriever.invoke(prompt)
        sources = list(set([
            os.path.basename(doc.metadata.get('source', 'Unknown'))
            for doc in docs
        ]))
        if sources:
            with st.expander('📎 Sources'):
                for src in sources:
                    st.caption(f"📄 {src}")

    # Save to memory
    st.session_state.chat_history.append({
        'question': prompt,
        'answer': full_response
    })
    st.session_state.messages.append({
        'role': 'assistant',
        'content': full_response,
        'sources': sources
    })