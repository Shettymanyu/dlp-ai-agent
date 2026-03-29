import streamlit as st
from src.utils import process_pdf
from src.agent import get_ai_response

# 1. Page Configuration
st.set_page_config(page_title="DLP AI Agent", page_icon="🛡️")
st.title("DLP AI Agent")
st.caption("AI Assistant")

# 2. Vector Database Load karna
@st.cache_resource
def init_db():
    with st.spinner("Database loading..."):
        return process_pdf()

vectorstore = init_db()

# 3. Chat History Initialize karna
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your DLP AI Agent. What would you like to know about DLP?"}
    ]

# 4. Puraani Chat History Dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input Box
if user_query := st.chat_input("Please Ask your questions (e.g., What is DLP?)..."):
    
    # User message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("💭 Thinking..."):
            ai_response = get_ai_response(vectorstore, user_query)
            st.markdown(ai_response)
            
    # Save response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})