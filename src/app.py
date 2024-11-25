import streamlit as st
import os
from pages.settings import settings_page

# Initialize session state for embedding model if it doesn't exist
if 'selected_embedding_model' not in st.session_state:
    st.session_state.selected_embedding_model = 'ChromaDB'  # Default value

# Sidebar layout
with st.sidebar:
    # Page selection dropdown in the sidebar
    page_options = ['Chat', 'Database', 'Settings']
    selected_page = st.selectbox("Choose a page", page_options)

    if selected_page == 'Chat':
        # Model selection dropdown in the sidebar
        model_options = ['llama3.1', 'llama2', 'gpt-4o']
        selected_model = st.selectbox("Choose a model", model_options)

# Main app layout
if selected_page == 'Chat':
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
            if selected_model.startswith('gpt-4o'):
                response = ask_gpt(context, selected_model)
            else:
                response = llm(context, selected_model)
            
            st.write(response)
            st.write("**Documents Retrieved:**")
            st.write(documents)
        else:
            st.write("Please enter a question.")
elif selected_page == 'Database':
    st.title("Database")
    st.write("This is the database page.")
    
    def save_uploaded_file(uploaded_file):
        # Set the folder where uploaded files will be saved
        upload_folder = 'data/raw_pdf'
        os.makedirs(upload_folder, exist_ok=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Save the uploaded file to the specified folder
                with open(os.path.join(upload_folder, uploaded_file.name), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Saved file: {uploaded_file.name}")
        st.write("Upload files to save them to the 'data/raw_pdf' folder.") 

    # Function to extract text from PDF
    def extract_text_from_pdf():
        process_pdfs()

    # Function to initialize vector database (Placeholder for ChromaDB or any other vector DB)
    def initialize_vector_db():
        chroma_client = chromadb.PersistentClient(path="data/vdb")
        return chroma_client

    def text_splitter():
        # Read the text from a file
        with open("data/processed_data/combined_text.txt") as f:
            state_of_the_union = f.read()

        # Initialize a text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        # Split the text into chunks

    # Create new collection
    st.subheader("Create New Collection")
    collection_name = st.text_input("Enter collection name")

    # Check if collection_name is not empty before proceeding
    if collection_name:
        try:
            collection = chroma_client.get_or_create_collection(name=collection_name)
            st.success(f"Collection '{collection_name}' has been created or retrieved successfully.")
        except Exception as e:
            st.error(f"Error creating or retrieving the collection: {e}")
    uploaded_files = st.file_uploader("Upload files", type=["pdf","json"], accept_multiple_files=True)
    if st.button("Create Collection") and collection_name and uploaded_files:
        save_uploaded_file(uploaded_files)
        extract_text_from_pdf()
        file_paths = add_document_to_vector_db(collection)
        st.success(f"Text from uploaded files added to collection '{collection_name}' in vector database!")

elif selected_page == 'Settings':
    settings()  # Call the settings_page function