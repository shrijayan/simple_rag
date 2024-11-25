import streamlit as st
import os

def database_page(collection, process_pdfs, add_document_to_vector_db):
    st.title("Database")
    st.write("This is the database page.")
    
    def save_uploaded_file(uploaded_files):
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