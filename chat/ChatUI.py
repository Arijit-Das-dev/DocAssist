import streamlit as st
import os
from IngestionPipeline.main1 import IngestionPipelineModel

st.title("DocAssist",
         width="stretch",
         text_alignment="center"
         )
st.divider()


st.sidebar.title("DocAssist")
st.sidebar.caption("✔ Start PDF analysis")
st.sidebar.caption("✔ Prepare document for search")
st.sidebar.caption("✔ Process PDF content")
st.sidebar.caption("✔ Build knowledge from PDF")

st.sidebar.divider()

pdf_doc = st.sidebar.file_uploader(

    label="Upload pdf below",
    type=["pdf"],
    help="Only PDF files are supported. Max size depends on your system"
)


st.sidebar.divider()

if pdf_doc:

    file_path = os.path.join("Docs", pdf_doc.name)

    if os.path.exists(file_path):
        pass
    else:
        with open(file_path, "wb") as f:
            f.write(pdf_doc.getbuffer())
            st.sidebar.success(f"File saved successfully")

def main():

    print("\n____________Main Function____________\n")
    ingest = IngestionPipelineModel()

    document = ingest.load_documents(file_path="Docs")

    splitted_chunks = ingest.text_to_chunks(document)

    vector_db = ingest.create_and_persist_chroma_db(splitted_chunks)

    print(vector_db)

if st.sidebar.button("Confirm"):main()