from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()

def save_vector_store(text_chunks, source_name="unknown"):
    """Create and save a vector store from text chunks."""
    if not text_chunks:
        print("Error: No text chunks provided for embedding.")
        return False

    try:
        # Convert text chunks to Document objects with metadata
        documents = [Document(page_content=chunk, metadata={"source": source_name}) for chunk in text_chunks]
        
        # Create embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # Create vector store
        vector_store = FAISS.from_documents(documents, embedding=embeddings)
        vector_store.save_local("faiss_index")
        print(f"Vector store saved successfully with {len(text_chunks)} chunks")
        return True
    except Exception as e:
        print(f"Error saving vector store: {e}")
        return False

def load_vector_store():
    """Load the vector store from disk."""
    if not os.path.exists("faiss_index"):
        print("Vector store does not exist!")
        return None
        
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    try:
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        print("Vector store loaded successfully")
        return vector_store
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None