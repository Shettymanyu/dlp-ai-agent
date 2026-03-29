# from src.utils import process_pdf
# from src.agent import get_ai_response

# def main():
#     print("🚀 DLP AI Agent Started...")
#     print("-" * 50)
    
#     # Step 1: PDF ko process karke Vector Database banao
#     print("Step 1: Processing PDF...")
#     vectorstore = process_pdf()
    
#     # Step 2: User se questions lena aur answers dena
#     print("\n✅ Vector Database ready! Ab aap questions puch sakte hain.")
#     print("(Exit ke liye 'quit' likhin)\n")
    
#     while True:
#         user_query = input("📝 Aapka sawal: ").strip()
        
#         if user_query.lower() == "quit":
#             print("👋 Goodbye!")
#             break
        
#         if not user_query:
#             print("⚠️ Kripaya koi sawal likhin...\n")
#             continue
        
#         # Step 3: AI se jawab mangwa
#         answer = get_ai_response(vectorstore, user_query)
#         print(f"\n🤖 Jawab: {answer}\n")

# if __name__ == "__main__":
#     main()


from src.utils import process_pdf
from src.agent import get_ai_response

def main():
    print("🚀 DLP AI Agent Started...")
    print("-" * 50)
    
    # Vector DB initialize karein
    vectorstore = process_pdf()
    
    print("\n✅ AI Agent Ready!")
    print("(For Exit 'quit' likhein)\n")

    while True:
        user_input = input("📝 Please Ask: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! Agent is shutting down...")
            break
        
        response = get_ai_response(vectorstore, user_input)
        print(f"\n🤖 Answer: {response}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()