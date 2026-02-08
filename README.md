# DocAssist

# 🍳 Overview
DocAssist is a document-based question answering system built using Retrieval-Augmented Generation (RAG).
It enables users to upload documents (PDFs) and interact with them using natural language queries.
Instead of relying on generic LLM knowledge, DocAssist retrieves relevant document chunks and generates responses strictly grounded in the uploaded content, reducing hallucinations and improving answer accuracy.
<br>

# 📌 Problem Statement
Large documents are difficult to manually search and understand.
Traditional keyword-based search fails to capture semantic meaning, and generic LLMs cannot reliably answer questions about private documents.

# ❔ Solution
DocAssist solves this by combining vector-based semantic search with large language models.
Relevant document sections are retrieved using embeddings and passed as context to the LLM, ensuring responses are accurate, explainable, and source-aware.

# 🔑 Key Features
• Upload and process PDF documents
• Semantic search using vector embeddings
• Context-aware question answering
• Reduced hallucination through retrieval grounding
• Modular RAG pipeline (ingestion, retrieval, generation)
• Scalable design for future extensions
