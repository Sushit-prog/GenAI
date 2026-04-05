import streamlit as st
from dotenv import load_dotenv
from langchain_cohere.chat_models import ChatCohere
from langchain_core.prompts import ChatPromptTemplate

# Load env
load_dotenv()

# Model
model = ChatCohere(model="command-xlarge-nightly")

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a professional Movie Information Extraction Assistant.

Your job is to extract useful structured information from a movie-related paragraph.

STRICT RULES:
- Do NOT add explanations
- Do NOT add extra comments
- Follow the exact format below
- If information is missing, write "NULL"
- Do NOT guess or infer missing facts
- Keep the summary within 2–3 lines only

OUTPUT FORMAT:

Title:
Release Year:
Genre:
Director:
Main Cast:
Main Characters:
Setting/Location:
Key Plot Points:
Scientific/Technical Concepts:
Themes:
Notable Elements:
Summary:
"""),
    ("human", """
Extract information from this paragraph:

{paragraph}
""")
])

# UI
st.title("Movie Info Extractor")

paragraph = st.text_area("Enter your paragraph:")

if st.button("Extract"):
    if paragraph.strip() == "":
        st.warning("Enter a paragraph first.")
    else:
        final_prompt = prompt.invoke({"paragraph": paragraph})
        response = model.invoke(final_prompt)
        
        st.subheader("Extracted Information")
        st.text(response.content)