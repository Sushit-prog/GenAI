from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
import os

splitter = CharacterTextSplitter(
  separator="",
  chunk_size=1000,
  chunk_overlap=1
)

data = TextLoader(r"C:\Users\pakra\Desktop\genai\CourseMateAI\documentloaders\notes.txt")
docs=data.load()
chunks = splitter.split_documents(docs)
# print(docs[0].page_content)
for i in chunks:
  print(i.page_content)
  print()
  print()
  print()
