from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from src.config import Config

def get_ai_response(vectorstore, user_query):
    """
    User ke sawaal ka jawab dene ke liye GPT model ka use karta hai.
    """
    try:
        # 1. GPT Model initialize karein (Config file se key uthayega)
        llm = ChatOpenAI(
            model_name=Config.MODEL_NAME,
            openai_api_key=Config.Config.OPENAI_API_KEY, # .env se load hui key
            temperature=0.2 # Kam temperature matlab zyada accurate aur factual answers
        )
        
        # 2. RAG Chain setup karein
        # Ye chain PDF ke database (vectorstore) se info nikal kar LLM ko degi
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff", # Saari relevant info ko ek saath 'stuff' karke bhejna
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}) # Top 3 matching results
        )
        
        # 3. Answer generate karein
        print("Thinking...")
        response = qa_chain.invoke(user_query)
        
        return response["result"]

    except Exception as e:
        return f"Error: {str(e)}"