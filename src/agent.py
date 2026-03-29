# # 1. Zaroori Imports (Yahan 'types' aur 'genai' import ho rahe hain)
# from google import genai
# from google.genai import types
# from src.config import Config

# # 2. Client Initialization (Yahan 'client' define ho raha hai)
# client = genai.Client(api_key=Config.GOOGLE_API_KEY)

# def get_ai_response(vectorstore, user_query):
#     """
#     Naye Gemini SDK ka use karke user ke sawaal ka jawab dene ke liye.
#     """
#     try:
#         # 1. Vectorstore se similar documents nikaalo
#         print("📚 Documents search kar rahe hain...")
#         retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
#         docs = retriever.invoke(user_query)
        
#         # 2. Context banao
#         context = "\n".join([doc.page_content for doc in docs])
        
#         # 3. Prompt define karo (Yahan 'prompt' variable ban raha hai)
#         prompt = f"""You are a highly professional Data Loss Prevention (DLP) AI agent. 
# Analyze the provided Context and answer the User's question accurately.
# CRITICAL RULE: You MUST answer strictly in English, regardless of the language the user asks the question in. Do not use Hindi greetings.
# If the answer is not in the context, say: "The provided document does not contain this information."

# Context:
# {context}

# User Question: {user_query}
# Answer:"""
        
#         print("💭 Gemini generating response...")
        
#         # 4. Gemini API call (Yahan 'client', 'prompt', aur 'types' use ho rahe hain)
#         response = client.models.generate_content(
#             model='gemini-2.5-flash', 
#             contents=prompt,
#             config=types.GenerateContentConfig(
#                 temperature=0.3,
#                 top_p=0.9,
#                 max_output_tokens=1024 # Poora answer aane ke liye limit badha di hai
#             )
#         )
        
#         # 5. Answer return karo
#         if response.text:
#             return response.text.strip()
#         else:
#             return "No response generated."

#     except Exception as e:
#         return f"Error: {str(e)}"# 1. Zaroori Imports (Yahan 'types' aur 'genai' import ho rahe hain)
# from google import genai
# from google.genai import types
# from src.config import Config

# # 2. Client Initialization (Yahan 'client' define ho raha hai)
# client = genai.Client(api_key=Config.GOOGLE_API_KEY)

# def get_ai_response(vectorstore, user_query):
   
#     try:
#         # 1. Vectorstore se similar documents nikaalo
#         print("📚 Documents search kar rahe hain...")
#         retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
#         docs = retriever.invoke(user_query)
        
#         # 2. Context banao
#         context = "\n".join([doc.page_content for doc in docs])
        
#         # 3. Prompt define karo (Yahan 'prompt' variable ban raha hai)
#         prompt = f"""You are a highly professional Data Loss Prevention (DLP) AI agent. 
# Analyze the provided Context and answer the User's question accurately.
# CRITICAL RULE: You MUST answer strictly in English, regardless of the language the user asks the question in. Do not use Hindi greetings.
# If the answer is not in the context, say: "The provided document does not contain this information."

# Context:
# {context}

# User Question: {user_query}
# Answer:"""
        
#         print("💭 Gemini generating response...")
        
#         # 4. Gemini API call (Yahan 'client', 'prompt', aur 'types' use ho rahe hain)
#         response = client.models.generate_content(
#             model='gemini-2.5-flash', 
#             contents=prompt,
#             config=types.GenerateContentConfig(
#                 temperature=0.3,
#                 top_p=0.9,
#                 max_output_tokens=1024 # Poora answer aane ke liye limit badha di hai
#             )
#         )
        
#         # 5. Answer return karo
#         if response.text:
#             return response.text.strip()
#         else:
#             return "No response generated."

#     except Exception as e:
#         return f"Error: {str(e)}"


from google import genai
from google.genai import types
from src.config import Config

# Client Initialization
client = genai.Client(api_key=Config.GOOGLE_API_KEY)

def get_ai_response(vectorstore, user_query):
    try:
        print("Searching Documents")
        # Jyada context fetch karne ke liye k=8 set kiya hai
        retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
        docs = retriever.invoke(user_query)
        
        context = "\n".join([doc.page_content for doc in docs])
        
        prompt = f"""You are a highly professional Data Loss Prevention (DLP) AI agent. 
Analyze the provided Context and answer the User's question accurately.
Note: "DLP" stands for "Data Loss Prevention". Treat them as the same concept.
CRITICAL RULE: You MUST answer strictly in English. Do not use Hindi greetings.
If the answer is not in the context, say: "The provided document does not contain this information."

Context:
{context}

User Question: {user_query}
Answer:"""
        
        print("💭 Gemini generating response...")
        
        response = client.models.generate_content(
            model=Config.MODEL_NAME, 
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                top_p=0.9,
                max_output_tokens=1024 # Pura answer aane ke liye badi limit
            )
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "No response generated."

    except Exception as e:
        return f"Error: {str(e)}"