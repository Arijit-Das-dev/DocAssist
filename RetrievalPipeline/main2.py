from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_chroma import Chroma
from RetrievalPipeline.GroqBluePrint import GroqModel


class RetrievalPipelineModel:

    def setting_Up_retrieval(self, query):

        # Initialize LLM with system prompt
        g = GroqModel(prompt_path="prompt.txt")

        # Targeted Vector DB
        target_db = "db/ChromaDB"

        # Embedding model (must match ingestion)
        embedding_model = HuggingFaceBgeEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Load Chroma DB
        db = Chroma(
            persist_directory=target_db,
            embedding_function=embedding_model,
            collection_metadata={"hnsw:space": "cosine"}
        )

        # Retriever (Top-k)
        retriever = db.as_retriever(search_kwargs={"k": 1})

        # Retrieve relevant documents 
        relevant_docs = retriever.invoke(query)

        print(f"\nUSER QUERY:\n{query}")
        print("\nRETRIEVED CONTEXT:\n")

        # Build context 
        # That context is returning top 3 relevent chunks that contains human readable sentences [texts]
        context = "\n\n".join(
            f"[Chunk {i+1}]\n{doc.page_content}"
            for i, doc in enumerate(relevant_docs)
        )

        # Collect streamed tokens
        # That context passes through the LLM for explaination
        final_answer = ""
        for token in g.stream_chat(
            user_message=context
        ):
            final_answer += token

        return final_answer