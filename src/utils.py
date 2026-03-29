import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.config import Config

def process_pdf():
    """
    PDF load karega, split karega, aur Vector Store banayega/load karega.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    persist_dir = "./chroma_db"

    # Agar DB pehle se hai, toh usko load karo
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        print("🔄 Existing Vector Database load kar rahe hain...")
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
        return vectorstore

    # Naya DB banane ka logic
    pdf_paths = [path.strip() for path in Config.PDF_PATH.split(",")]
    all_documents = []
    
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"⚠️ Error: {pdf_path} not found.")
        
        print(f"📄 Loading... {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        all_documents.extend(documents)
    
    print(f"✅ Total documents loaded: {len(all_documents)}")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150 
    )
    docs = text_splitter.split_documents(all_documents)
    print(f"Dividing into {len(docs)} chunks")
    
    print("Creating new Vector Database")
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings,
        persist_directory=persist_dir  
    )
    
    print("Vector Database is ready")
    return vectorstore