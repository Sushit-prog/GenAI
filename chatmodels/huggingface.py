
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="C:/Users/pakra/Desktop/genai/.env")

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
  repo_id="deepseek-ai/DeepSeek-R1"
  
)

model = ChatHuggingFace(llm=llm)
response=model.invoke("What is the capital of France?")
print(response.content)



