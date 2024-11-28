# from dotenv import load_dotenv
# load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import pdfplumber
import streamlit as st

chat_model = ChatOpenAI()
output_parser = StrOutputParser()

st.title("Summarizer")

selector = st.radio(
    "Select the type of content you want to summarize.",
    ["Text", "URL", "PDF"],
    captions = ["Input text directly.", "Input link to a website.", "Upload PDF files."]
)

option = st.text_input("**Prompt (Optional)**")
st.caption("**Examples :** 'Summarize within 100 words.', 'Summarize by list', 'Translate to Korean', ...")
if selector == "Text":
    content = st.text_area("**Text**")
    if st.button('Summarize'):
        with st.spinner("Summarizing..."):
            chain = chat_model | output_parser
            result = chain.invoke(f"Summarize the text delimited by triple backticks, and refer to the text delimited by angled brackets when summarizing it. <{option}> ```{content}```")
            if content == "":
                 result = ""
            st.write(result)
elif selector == "URL":
    content = st.text_input("**URL**")
    if st.button('Summarize'):
        with st.spinner("Summarizing..."):
            chain = chat_model | output_parser
            result = chain.invoke(f"Summarize the link delimited by triple backticks, and refer to the text delimited by angled brackets when summarizing it. <{option}> ```{content}```")
            if content == "":
                 result = ""
            st.write(result)
elif selector == "PDF":
    uploaded_files = st.file_uploader("**PDF**", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        st.write(len(uploaded_files), "files uploaded")
        content = ""
        for uploaded_file in uploaded_files:
            st.write("File name:", uploaded_file.name, " (", uploaded_file.size, "bytes)")
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    content += text
    if st.button('Summarize'):
        with st.spinner("Summarizing..."):
            chain = chat_model | output_parser
            result = chain.invoke(f"Summarize the text delimited by triple backticks, and refer to the text delimited by angled brackets when summarizing it. <{option}>  ```{content}```")
            st.write(result)
