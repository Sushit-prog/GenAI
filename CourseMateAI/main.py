from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

data = PyPDFLoader(r"C:\Users\pakra\Desktop\genai\CourseMateAI\documentloaders\GRU.pdf")
docs = data.load()

template = ChatPromptTemplate.from_messages(
  [
    ("system", "You are an AI that summarizes the text"),
    ("human", "{data}")
  ]
)

model = ChatGroq(model="llama-3.1-8b-instant")

prompt = template.format_messages(data=docs)

response = model.invoke(prompt)
print(response.content)