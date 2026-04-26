from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool 
from langchain_core.messages import HumanMessage


from rich import print

#  creating a tool

@tool
def get_text_length(text: str) -> int:
  """Return the number of characters in a given text"""
  return len(text)

llm = ChatMistralAI(model="mistral-small-2506")

# tool binding
llm_with_tool=llm.bind_tools([get_text_length])

# result=llm.invoke("Return the number of characters in a given text: 'Hello how are you?'")
# result = llm_with_tool.invoke("Return the number of characters in a given text: 'Hello how are you?'")
# if result.tool_calls:
#   tool_call=result.tool_calls[0]
# tool_name= tool_call["name"]
# tool_args= tool_call["args"]

# tool_result = get_text_length.invoke(tool_args)

# final_response = llm_with_tool.invoke(f"The length of the text is {tool_result}")


# print(result.tool_calls[0])
# print(get_text_length.invoke({
#     'name': 'get_text_length',
#     'args': {'text': 'Hello how are you?'},
#     'id': '3cJVZ1DOg',
#     'type': 'tool_call'
# }))


message = []

query = HumanMessage("Return the number of characters in the given text 'Hello How are you?'")

message.append(query)
print(message)

result=llm_with_tool.invoke(message)

print(result)

message.append(result)

if result.tool_calls:
  print(result.tool_calls[0])
  tool_name=result.tool_calls[0]["name"]
  # tool_name.invoke()