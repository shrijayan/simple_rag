from openai import OpenAI
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def llm(question, content):

  # Point to the local server
  client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

  passlllm = f'Question:{question}\n Content:{content}'
  print(passlllm)

  completion = client.chat.completions.create(
    model="TheBloke/Llama-2-7B-Chat-GGUF",
    messages=[
      {"role": "system", "content": "You are a Q&A Chatbot intracting with real-world customers to their questions. Only answer based on the content provided. Do not provide any information that is not in the content. Answer in a intercative way"},
      {"role": "user", "content": passlllm}
    ],
    temperature=0.7,
  )

  return completion.choices[0].message.content


reader = PdfReader("../data/12th_Computer-Science_EM - www.tntextbooks.in.pdf")

with open('extracted_text.txt', "w", encoding="utf-8") as output_file:
    for page in reader.pages:
        page_text  = page.extract_text()
        output_file.write(page_text)
        output_file.write("\n")
        

# Read the text from a file
with open("extracted_text.txt") as f:
    state_of_the_union = f.read()

# Initialize a text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split the text into chunks
chunks = text_splitter.create_documents([state_of_the_union])

# Extract the page content from each chunk
vdb_data = [chunk.page_content for chunk in chunks]

import chromadb
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="rag-system")

collection.add(
    documents = vdb_data,
    ids = [str(i) for i in range(len(vdb_data))]
)

question = "who is the founder of python"

results = collection.query(
    query_texts=[question], # Chroma will embed this for you
    n_results=8 # how many results to return
)
vdb_answer = results['documents'][0]