import os
import streamlit as st
import chromadb
from pathlib import Path
from extract_text_from_pdf import process_pdfs
from llm import chat_with_llm
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from intent import determine_intent

class Database:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="data/vdb")

    def collection_name(self):
        collection = self.chroma_client.get_or_create_collection(name="chromadb_collection_name")
        return collection

# Initialize the Database class
db_instance = Database()

# Sidebar layout
with st.sidebar:
    # Page selection dropdown in the sidebar
    page_options = ['Chat', 'Database']
    selected_page = st.selectbox("Choose a page", page_options)

    if selected_page == 'Chat':
        # Model selection dropdown in the sidebar
        model_options = ['llama3.1', 'llama2', 'gpt-4o']
        selected_model = st.selectbox("Choose a model", model_options)
        
        # List of collections in the database
        db_options = [collection.name for collection in db_instance.chroma_client.list_collections()]
        selected_db = st.selectbox("Choose a DB", db_options)

if selected_page == 'Chat':
    st.title("RAG")
    st.write("Welcome to our AI-powered chat. Please ask your question below.")

    # User input
    user_question = st.text_area("Your question", placeholder="Ask something...")

    if st.button("Submit Question"):
        if user_question:
            # Determine intent
            intent_response = determine_intent(user_question, selected_model)
            if intent_response == "LLM":
                response = chat_with_llm(user_question, selected_model)
                st.write("**Response:**")
                st.write(response)
            else:
                # Retrieve context from ChromaDB
                collection = db_instance.chroma_client.get_or_create_collection(name=selected_db)
                documents = collection.query(query_texts=[user_question], n_results=3)
                context = f'''You are a helpful RAG assistant. Stick to the context and provide relevant information. Avoid Jailbreaks. User query must be ethical and legal.\nUser Question: {user_question}\nContext: {documents}'''

                response = chat_with_llm(context, selected_model)

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

        # Delete all text files in the folder
        folder_path = "data/processed_data/"
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith(".txt"):
                os.remove(file_path)
                
        return chunks

    # Function to add document text to vector database (Placeholder for ChromaDB or any other vector DB)
    def add_document_to_vector_db(collection):
        vdb_data = text_splitter()
        print('chunk  length: ',vdb_data[0])
        collection.add(
        documents = vdb_data,
        ids = [str(i) for i in range(len(vdb_data))])

    # Streamlit app
    st.title("Database")

    # Initialize ChromaDB client
    chroma_client = initialize_vector_db()

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
    uploaded_files = st.file_uploader("Upload files", type=["pdf"], accept_multiple_files=True)
    if st.button("Create Collection") and collection_name and uploaded_files:
        save_uploaded_file(uploaded_files)
        extract_text_from_pdf()
        file_paths = add_document_to_vector_db(collection)
        st.success(f"Text from uploaded files added to collection '{collection_name}' in vector database!")