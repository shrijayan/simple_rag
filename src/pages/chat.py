import streamlit as st

def chat_page(collection, ask_gpt, llm):
    st.title("RAG")
    st.write("Welcome to our AI-powered chat. Please ask your question below.")

    # User input
    user_question = st.text_area("Your question", placeholder="Ask something...")

    if st.button("Get Answer"):
        if user_question:
            # Retrieve context from ChromaDB
            documents = collection.query(query_texts=[user_question], n_results=2)
            context = f"You are a helpful RAG assistant. Stick to the context and provide relevant information.\nUser Question: {user_question}\nContext: {documents}"
            
            # Generate response based on selected model
            if st.session_state.selected_model.startswith('gpt-4o'):
                response = ask_gpt(context, st.session_state.selected_model)
            else:
                response = llm(context, st.session_state.selected_model)
            
            st.write(response)
            st.write("**Documents Retrieved:**")
            st.write(documents)
        else:
            st.write("Please enter a question.")