from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer
import os

class IngestionPipelineModel:

    def load_documents(self, file_path="Docs"):

        if not os.path.exists(file_path):

            raise FileNotFoundError(f"___{file_path} IS MISSING___")

        # loading the Folders + files
        loader = DirectoryLoader(

            path=file_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )

        print("___FILES LOADED SUCCESSFULLY___")

        # Loading the files inside the folders
        documents = loader.load()

        if len(documents) == 0:

            raise FileNotFoundError("___FOLDER CONTAINS NOTHING___")
        
        for i, doc in enumerate(documents):

            print("="*100)
            print(f"\nFile no. {i+1}")
            print(f" \nSource: {doc.metadata['source']}") # File location/Name
            print(f" \ncontent length: {len(doc.page_content)} characters") # total characters inside the text file
            print(f" \ncontent preview: {doc.page_content[:100]}...") # Printing only the first 100 characters from the file
            print(f" \nmetadata: {doc.metadata}")

        return documents
    
    def text_to_chunks(self, document, chunk_size = 800, chunk_overlap = 100):

        print("____GETTING READY OF CHUNKS____")

        # for token count
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

        # Splitting All the texts
        text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunk_size, # splitted upto 800 chars 
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        # We are assigning all the splitted texts inside each chunks
        chunks = text_splitter.split_documents(document)

        if chunks:
            print(len(chunks))
            for i, chunk in enumerate(chunks, 1):

                print("="*100)
                print(f" \nChunk : {i}")
                print(f" \nSource : {chunk.metadata['source']}") # Location 
                tokens = tokenizer.encode(chunk.page_content)
                num_tokens = len(tokens)
                print(f"Tokens in chunk {i} : {num_tokens}") # Tokens in each chunk
                print(f" \nContent:")
                print(f" \n{chunk.page_content}") # Chunk Contents


        return chunks

    def create_and_persist_chroma_db(self, chunks, db_path="db/ChromaDB"):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=db_path,
            collection_metadata={"hnsw:space": "cosine"}
        )

        print("____SUCCESSFUL_____")
        return vector_store