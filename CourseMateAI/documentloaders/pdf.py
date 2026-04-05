from langchain_community.document_loaders import PyPDFLoader

data = PyPDFLoader(r"C:\Users\pakra\Desktop\genai\CourseMateAI\documentloaders/GRU.pdf")
docs = data.load()

print(len(docs))