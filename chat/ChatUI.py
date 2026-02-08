import streamlit as st
import os
from IngestionPipeline.main1 import IngestionPipelineModel
from RetrievalPipeline.main2 import RetrievalPipelineModel

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(
    page_title="DocAssist",
)

# -------------------------------
# Title
# -------------------------------
st.title("📄Wellcome to DocAssist")
st.divider()

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("DocAssist")
st.sidebar.caption("✔ Upload PDFs")
st.sidebar.caption("✔ Index documents")
st.sidebar.caption("✔ Ask questions from PDFs")
st.sidebar.divider()

# -------------------------------
# Session State Init
# -------------------------------
if "db_ready" not in st.session_state:
    st.session_state.db_ready = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# PDF Upload
# -------------------------------
pdf_doc = st.sidebar.file_uploader(
    label="Upload PDF",
    type=["pdf"],
    help="Only PDF files are supported"
)

if pdf_doc:
    os.makedirs("Docs", exist_ok=True)
    file_path = os.path.join("Docs", pdf_doc.name)

    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(pdf_doc.getbuffer())
        st.sidebar.success("PDF uploaded successfully")
    else:
        st.sidebar.success("Start Chat")

# -------------------------------
# INGESTION (RUNS ONCE)
# -------------------------------
if st.sidebar.button("Confirm") and not st.session_state.db_ready:

    with st.spinner("Indexing documents..."):

        ingest = IngestionPipelineModel()

        documents = ingest.load_documents(file_path="Docs")
        chunks = ingest.text_to_chunks(documents)
        ingest.create_and_persist_chroma_db(chunks)

        st.session_state.db_ready = True

    st.sidebar.success("Documents indexed successfully")

# -------------------------------
# CHAT UI (ALWAYS RUNS)
# -------------------------------
rp = RetrievalPipelineModel()

if st.session_state.db_ready:

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Ask anything from your PDFs...")

    if user_input:
        # Store user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = rp.setting_Up_retrieval(user_input)
                st.markdown(response)

        # Store assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

else:
    st.info("👈 Upload PDFs and click **Confirm** to start chatting.")
