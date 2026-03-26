import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.config import Config

def process_pdf():
    """
    Will load one or multiple PDFs, split them into chunks and create a Vector Store.      
    """
    # 1. PDF paths ko comma-separated list se split karo
    pdf_paths = [path.strip() for path in Config.PDF_PATH.split(",")]
    
    all_documents = []
    
    # 2. Har PDF ko load karo
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"⚠️ Error: {pdf_path} not found kindly check the path and try again.")
        
        print(f"📄 Loading... {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        all_documents.extend(documents)
    
    print(f"✅ Total documents loaded: {len(all_documents)}")
    
    # 3. Text ko chunks mein divide karein (Context Window manage karne ke liye)
    # chunk_size=1000 ka matlab hai ek baar mein 1000 characters read honge
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150  # Thoda overlap taaki context miss na ho
    )
    docs = text_splitter.split_documents(all_documents)
    print(f"📚 Dividing into {len(docs)} chunks")
    
    # 4. Embeddings aur Vector Store banayein (HuggingFace - free!)
    # Embeddings text ko numbers (vectors) mein convert karti hain
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("🔄 Creating Vector Database (ChromaDB)...")
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings,
        persist_directory="./chroma_db"  
    )
    
    print("✅ Vector Database ready hai!")
    return vectorstore