import streamlit as st

def settings_p():
    st.title("Settings")
    # Embedding model selection dropdown
    embedding_model_options = ['ChromaDB', 'LLM2VEC']
    
    # Initialize session state for embedding model if it doesn't exist
    if 'selected_embedding_model' not in st.session_state:
        st.session_state.selected_embedding_model = embedding_model_options[0]  # Default value

    selected_embedding_model = st.selectbox(
        "Choose an embedding model", 
        embedding_model_options, 
        index=embedding_model_options.index(st.session_state.selected_embedding_model)
    )

    # Update session state when a new embedding model is selected
    st.session_state.selected_embedding_model = selected_embedding_model

    st.write(f"Selected embedding model: {st.session_state.selected_embedding_model}")