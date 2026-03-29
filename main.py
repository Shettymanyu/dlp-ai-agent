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