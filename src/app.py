import os
import streamlit as st
import chromadb
from openai import OpenAI
from pathlib import Path
from extract_text_from_pdf import process_pdfs
from llm import chat_with_llm
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="data/vdb")
collection = chroma_client.get_or_create_collection(name="chromadb_collection_name")

# Sidebar layout
with st.sidebar:
    # Page selection dropdown in the sidebar
    page_options = ['Chat', 'Database']
    selected_page = st.selectbox("Choose a page", page_options)

    if selected_page == 'Chat':
        # Model selection dropdown in the sidebar
        model_options = ['llama3.1', 'llama2', 'gpt-4o']
        selected_model = st.selectbox("Choose a model", model_options)

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
            
            response = chat_with_llm(context, selected_model)
            
            print(response)
            st.write("**Response:**")
            st.write(response)
            st.write("**Documents Retrieved:**")
            st.write(documents)
        else:
            st.write("Please enter a question.")
            
elif selected_page == 'Database':
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
        chunks = text_splitter.split_text(state_of_the_union)

        # # Extract the page content from each chunk
        # vdb_data = [chunk for chunk in chunks]
        
        return chunks
    
    # Function to list existing collections
    def list_collections(client):
        return client.list_collections()

    # Function to add document text to vector database (Placeholder for ChromaDB or any other vector DB)
    def add_document_to_vector_db():
        vdb_data = text_splitter()
        print('chunk  length: ',vdb_data[0])
        collection = chroma_client.get_or_create_collection(name="chromadb_collection_name")
        collection.add(
        documents = vdb_data,
        ids = [str(i) for i in range(len(vdb_data))])

    # Streamlit app
    st.title("Database")

    # Initialize ChromaDB client
    chroma_client = initialize_vector_db()

    # Streamlit UI
    st.subheader("Existing Collections")
    collections = list_collections(chroma_client)
    print(collection.name)

    # Initialize session state for selected collections if it doesn't exist
    if 'selected_collections' not in st.session_state:
        st.session_state.selected_collections = []

    collections = [collection.name] 

    if collections:
        selected_collections = []
        for collection in collections:
            if st.checkbox(collection, key=collection):
                selected_collections.append(collection)

        # Update session state
        st.session_state.selected_collections = selected_collections
    else:
        st.write("No collections found.")

    # Create new collection
    st.subheader("Create New Collection")
    collection_name = st.text_input("Enter collection name")
    uploaded_files = st.file_uploader("Upload files", type=["pdf"], accept_multiple_files=True)
    if st.button("Create Collection") and collection_name and uploaded_files:
        save_uploaded_file(uploaded_files)
        extract_text_from_pdf()
        file_paths = add_document_to_vector_db()
        st.success(f"Text from uploaded files added to collection '{collection_name}' in vector database!")