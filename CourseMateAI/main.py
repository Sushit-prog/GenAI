from dotenv import load_dotenv
from langchain_groq import ChatMistral
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter



load_dotenv()

data = PyPDFLoader(r"C:\Users\pakra\Desktop\genai\CourseMateAI\documentloaders\deep-learning-material-dept-ece-ase-bir-1.pdf")
docs = data.load()

splitter = RecursiveCharacterTextSplitter(
  chunk_size=1000,
  chunk_overlap=200
)

chunks =splitter.split_documents(docs)

template = ChatPromptTemplate.from_messages(
  [
    ("system", "You are an AI that summarizes the text"),
    ("human", "{data}")
  ]
)

model = ChatMistral(model="mistral-small-2603")

prompt = template.format_messages(data=docs)

response = model.invoke(prompt)
print(response.content)