import streamlit as st
from agent import extract_text_from_pdf, split_into_chunks, summarize_chunks
import tempfile

st.set_page_config(page_title="🧠 Smart Note Summarizer", layout="centered")

st.title("🧠 Smart Note Summarizer")
st.write("Upload a large PDF and get a clean summary using Hugging Face Transformers.")

# 📂 File Upload
uploaded_file = st.file_uploader("📄 Upload your PDF file (Max: 10 MB)", type=["pdf"])

if uploaded_file is not None:
    if uploaded_file.size > 10_000_000:
        st.error("❌ File too large. Please upload a file smaller than 10 MB.")
        st.stop()

    # Save file to temp path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    with st.spinner("🔍 Extracting text from PDF..."):
        text = extract_text_from_pdf(temp_path)
        st.success(f"✅ Extracted {len(text)} characters from PDF.")

    st.write("📖 Preview of extracted text (first 1000 characters):")
    st.text(text[:1000])

    with st.spinner("🪓 Splitting text into chunks..."):
        chunks = split_into_chunks(text, max_tokens=300)
        st.success(f"✅ Split into {len(chunks)} chunks.")

    with st.spinner("🧠 Summarizing chunks (please wait)..."):
        summaries = []
        for i, chunk in enumerate(chunks):
            st.write(f"🧠 Summarizing chunk {i + 1} of {len(chunks)}...")
            try:
                summary = summarize_chunks([chunk])
                summaries.append(summary)
            except Exception as e:
                st.error(f"❌ Error summarizing chunk {i + 1}: {e}")
        final_summary = "\n\n".join(summaries)

    st.success("✅ Summary generation complete!")
    st.subheader("📌 Final Summary")
    st.write(final_summary)
