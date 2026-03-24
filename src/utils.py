import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import Config

def process_pdf():
    """
    Will load the pdf, split it into chunks and create a Vector Store.      
    """
    if not os.path.exists(Config.PDF_PATH):
        raise FileNotFoundError(f"⚠️ Error: {Config.PDF_PATH} not found kindly check the path and try again.")

    print(f"Loading... {Config.PDF_PATH}")
    
    # 1. PDF Load karein
    loader = PyPDFLoader(Config.PDF_PATH)
    documents = loader.load()
    
    # 2. Text ko chunks mein divide karein (Context Window manage karne ke liye)
    # chunk_size=1000 ka matlab hai ek baar mein 1000 characters read honge
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150  # Thoda overlap taaki context miss na ho
    )
    docs = text_splitter.split_documents(documents)
    print(f" Dividing {len(docs)} in chunks ")
    
    # 3. Embeddings aur Vector Store banayein
    # Embeddings text ko numbers (vectors) mein convert karti hain
    embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
    
    print(" Creating Vector Database  (ChromaDB)...")
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings,
        persist_directory="./chroma_db"  
    )
    
    print("✅ Vector Database ready hai!")
    return vectorstore