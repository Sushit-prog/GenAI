# load the pdf
# split into chunks
# create the embeddings
# store into chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

data = PyPDFLoader(r"C:\Users\pakra\Desktop\genai\CourseMateAI\documentloaders\deep-learning-material-dept-ece-ase-blr-1.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

embedding_model = CohereEmbeddings(
    model="embed-english-v3.0"
)

vectorstore = Chroma.from_documents(   # ✅ Capital C
    documents=chunks,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)

print(f"✅ Done! {len(chunks)} chunks stored in ChromaDB.")