import streamlit as st
from langchain_groq import ChatGroq


st.set_page_config(page_title="My AI Chat", layout="centered")


st.title("🤖 The Groq Chatbot")
st.write("A fully integrated, memory-enabled AI assistant.")


# --- 1. THE SIDEBAR (API Key Security) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    user_api_key = st.text_input("Enter Groq API Key:", type="password")
    st.info("Your key is required to wake up the AI brain.")


# --- 2. THE MEMORY VAULT ---
# Initialize the chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- 3. DISPLAY HISTORY ---
# Redraw all past messages every time the page reruns
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- 4. THE CHAT INPUT & LOGIC ---
# If the user types a message and hits Enter...
if user_query := st.chat_input("Message the AI..."):

    if not user_api_key:
        st.error("Please enter your API Key in the sidebar first!")
    else:
        # A. Save and display the user's message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # B. Initialize the Brain
        llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.3-70b-versatile",
            api_key=user_api_key
        )

        # C. Call the AI (Showing a loading spinner while it thinks)
        with st.spinner("AI is thinking..."):
            # Notice how we pass the ENTIRE vault history to the LLM!
            response = llm.invoke(st.session_state.messages)
            bot_answer = response.content

        # D. Save and display the AI's response
        st.session_state.messages.append({"role": "assistant", "content": bot_answer})
        with st.chat_message("assistant"):
            st.markdown(bot_answer)
