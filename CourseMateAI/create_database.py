# load the pdf
# split into chunks
# create the embeddings
# store into chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import time

load_dotenv()

data = PyPDFLoader(r"C:\Users\pakra\Desktop\genai\CourseMateAI\documentloaders\deep-learning-material-dept-ece-ase-blr-1.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

embedding_model = NVIDIAEmbeddings(
    model="nvidia/nv-embedqa-e5-v5",
    truncate="END"
)

# ── Batched ingestion with rate-limit guard ──────────────────────────────────
BATCH_SIZE = 50        # chunks per API call
SLEEP_SECS = 15        # pause between batches (tune if still hitting limits)

vectorstore = None

for i in range(0, len(chunks), BATCH_SIZE):
    batch = chunks[i : i + BATCH_SIZE]

    if vectorstore is None:
        # First batch — create the vectorstore
        vectorstore = Chroma.from_documents(
            documents=batch,
            embedding=embedding_model,
            persist_directory="./chroma_db"
        )
    else:
        # Subsequent batches — append to existing vectorstore
        vectorstore.add_documents(batch)

    print(f"📦 Stored chunks {i + 1}–{i + len(batch)} / {len(chunks)}")

    # Don't sleep after the last batch
    if i + BATCH_SIZE < len(chunks):
        print(f"⏳ Waiting {SLEEP_SECS}s to respect rate limit...")
        time.sleep(SLEEP_SECS)

print(f"\n✅ Done! {len(chunks)} chunks stored in ChromaDB.")