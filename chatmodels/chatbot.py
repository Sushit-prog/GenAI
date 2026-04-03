from dotenv import load_dotenv
load_dotenv(dotenv_path="C:/Users/pakra/Desktop/genai/.env")

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-small-2603",temperature=0.9)

messages = [

]

print("----------------- welcom type 0 to exit the application-----------------")
while True:
    
    prompt = input("You : ")
    messages.append(prompt)
    # messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(messages)
    messages.append(response.content)
    # messages.append(AIMessage(content=response.content))
    print("Bot :",response.content)

print(messages)
