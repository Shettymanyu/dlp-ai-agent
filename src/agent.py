import google.generativeai as genai
from src.config import Config

# Gemini API ko configure karo
genai.configure(api_key=Config.GOOGLE_API_KEY)

def get_ai_response(vectorstore, user_query):
    """
    Gemini API use karke user ke sawaal ka jawab dene ke liye.
    """
    try:
        # 1. Vectorstore se similar documents nikaalo
        print("📚 Documents search kar rahe hain...")
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(user_query)
        
        # 2. Context banao
        context = "\n".join([doc.page_content for doc in docs])
        
        # 3. Prompt banao with context
        system_prompt = f"""Tum ek DLP (Data Loss Prevention) AI agent ho. 
Niche diye gaye document ke context se user ke sawaal ka jawab do.
Hamesha English mein concise answer do.

Context:
{context}

---
"""
        
        full_prompt = system_prompt + f"\nUser: {user_query}\nAssistant:"
        
        print("💭 Gemini se jawab le rahe hain...")
        
        # 4. Gemini API call - fast generation (using gemini-1.5-flash)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=200
            )
        )
        
        answer = response.text.strip()
        
        return answer if answer else "Samajh nahi aaya"

    except Exception as e:
        return f"Error: {str(e)}"