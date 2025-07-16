# app.py
import streamlit as st
from agent import extract_text_from_pdf, split_into_chunks, summarize_chunks

st.title("🧠 Smart Note Summarizer")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    text = extract_text_from_pdf("temp.pdf")
    chunks = split_into_chunks(text)
    summary = summarize_chunks(chunks)

    st.subheader("📚 Summary")
    st.write(summary)
