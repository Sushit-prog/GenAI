from langchain_community.document_loaders import TextLoader
import os

data = TextLoader(r"C:\Users\pakra\Desktop\genai\CourseMateAI\documentloaders\notes.txt")
docs=data.load()
# print(docs[0].page_content)
print(len(docs))