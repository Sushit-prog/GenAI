from langchain_cohere import CohereEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

texts = [
    "Hello this is Sushit Lal Pakrashy",
    "Hello your name is YouTube",
    "And you all are very beautiful"
]

vector = embeddings.embed_documents(texts)
print(vector)