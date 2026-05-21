from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
# FIX: Updated import path for modern LangChain versions
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

def build_vector_store(report_pages, embedding_model, persist_dir):
    """
    Takes the parsed (and sanitized) PDF pages, chunks them, 
    and builds a persistent ChromaDB vector store.
    """
    documents = []
    
    # Iterate through the parsed pages
    for page_data in report_pages:
        page_num = page_data.get("page_num") 
        text_content = page_data.get("text", "")
        
        # Create LangChain Document objects with metadata for source tracing
        if text_content.strip():
            doc = Document(
                page_content=text_content, 
                metadata={"page": page_num} 
            )
            documents.append(doc)

    if not documents:
        logger.warning("No documents to process for vector store.")
        return None

    # Chunk the documents to fit into the LLM context window effectively
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=300
    )
    chunks = text_splitter.split_documents(documents)
    
    logger.info(f"Building ChromaDB with {len(chunks)} chunks at {persist_dir}")
    
    # Build and persist ChromaDB
    vectordb = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_model, 
        persist_directory=persist_dir
    )
    
    return vectordb