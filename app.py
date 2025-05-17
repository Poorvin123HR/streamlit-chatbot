import streamlit as st
st.title("Streamlit chatbot")
import os
os.environ["GOOGLE_API_KEY"]=st.secrets["GOOGLE_API_KEY"]
import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Set page config
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful assistant.")
    ]

st.title("💬 Gemini Chatbot")
st.write("Ask me anything. Type `quit` to end the chat.")

# Input box for user message
user_input = st.chat_input("Say something...")

if user_input:
    if user_input.lower() == "quit":
        st.stop()

    # Append user message
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from LLM
    try:
        result = llm.invoke(st.session_state.chat_history)
        ai_response = result.content
    except Exception as e:
        ai_response = f"⚠️ Error: {str(e)}"

    # Append AI response
    st.session_state.chat_history.append(AIMessage(content=ai_response))

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

# Show full conversation history
for msg in st.session_state.chat_history[1:]:  # Skip system message
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)
