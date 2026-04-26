from langchain.tools import tool


@tool # decorator for creating a tool
def get_greeting(name: str) -> str:
  """Generate a greeting message for the given name."""

  return f"Hello {name}, Welcome to the world of AI agents!"



result=get_greeting.invoke({"name": "Sushit"})
print(result)

print(get_greeting.name)
print(get_greeting.description)
print(get_greeting.args_schema)

