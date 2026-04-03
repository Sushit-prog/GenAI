# from dotenv import load_dotenv
# import os
# # print(os.getcwd())

# load_dotenv(dotenv_path="C:/Users/pakra/Desktop/genai/.env")
# # print("KEY:", os.getenv("OPENROUTER_API_KEY"))
# # print("BASE:", os.getenv("OPENROUTER_API_KEY"))





# # from langchain_openai import ChatOpenAI
# from langchain.chat_models import init_chat_model 
# # model = ChatOpenAI(
# #     model="openai/gpt-4.1",  # OpenRouter format
# #     base_url="https://openrouter.ai/api/v1",
  
# #     temperature=0,
# #     max_tokens=500 
# # )

# model = init_chat_model(model="google/gemini-1.5-pro", temperature=0, max_tokens=500)

# response = model.invoke("Who is considered to be the GOAT of soccer?")
# print(response.content)


# From Gemini 1.5 Pro to Gemini 2.5 Flash Lite
# from dotenv import load_dotenv
# load_dotenv(dotenv_path="C:/Users/pakra/Desktop/genai/.env")

# from langchain_google_genai import ChatGoogleGenerativeAI

# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

# response = model.invoke("Who is considered to be the GOAT of soccer?")
# print(response.content)


# for groq
# from dotenv import load_dotenv
# load_dotenv(dotenv_path="C:/Users/pakra/Desktop/genai/.env")

# from langchain_groq import ChatGroq
# model = ChatGroq(model="openai/gpt-oss-120b")

# response = model.invoke("What was the best Power Rangers series?")
# print(response.content)

# Mistral 
from dotenv import load_dotenv
load_dotenv(dotenv_path="C:/Users/pakra/Desktop/genai/.env")

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-small-2603", temperature=0.9,max_tokens=20)

response = model.invoke("Write a poem on AI")
print(response.content)