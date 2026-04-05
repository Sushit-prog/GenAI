from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_cohere.chat_models import ChatCohere

load_dotenv()

# Schema
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    main_cast: Optional[List[str]]
    main_characters: Optional[List[str]]
    setting_location: Optional[str]
    key_plot_points: Optional[List[str]]
    scientific_technical_concepts: Optional[List[str]]
    themes: Optional[List[str]]
    notable_elements: Optional[List[str]]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie)

# Model
model = ChatCohere(model="command-xlarge-nightly")

# Prompt (FIXED)
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a strict movie information extraction system.

Follow these rules:
- Do NOT add explanations
- Do NOT hallucinate
- If data is missing, return null
- Follow the schema exactly

{format_instructions}
"""),
    ("human", "{paragraph}")
])

# Input
para = input("Give your paragraph: ")

# Invoke
final_prompt = prompt.invoke({
    "paragraph": para,
    "format_instructions": parser.get_format_instructions()
})

response = model.invoke(final_prompt)

# 🔥 THIS IS WHAT YOU MISSED
parsed_output = parser.parse(response.content)

print(parsed_output)