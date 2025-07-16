import streamlit as st
from agent import extract_text_from_pdf, split_into_chunks, summarize_chunks_batch
import tempfile
import time

st.set_page_config(page_title=" Smart Note Summarizer", layout="centered")
st.title(" Smart Note Summarizer")
st.write("Upload your PDF and get fast, batched AI-generated summaries using open-source LLMs.")
st.markdown("### 📄 Upload your PDF file of 5MB")
st.caption("⚠️ Max file size: **5MB** • Only PDF allowed")
uploaded_file = st.file_uploader("", type=["pdf"])



if uploaded_file is not None:
    if uploaded_file.size > 5_000_000:
        st.error("❌ File too large. Please upload below 5MB.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    st.write("✅ File uploaded. Extracting text...")

    try:
        text = extract_text_from_pdf(temp_path)
        if not text.strip():
            st.error("⚠️ No text found. Is this a scanned PDF?")
            st.stop()

        st.success(f"Extracted {len(text)} characters.")
        st.write("📖 Preview:")
        st.text(text[:1000])

        st.info("🪓 Splitting into chunks...")
        chunks = split_into_chunks(text, max_tokens=300)
        st.success(f"✅ Split into {len(chunks)} chunks.")

        st.info("🧠 Summarizing in batch...")
        start_time = time.time()

        summaries = summarize_chunks_batch(chunks, batch_size=4)
        total_time = round(time.time() - start_time, 2)

        st.success(f"✅ Summarization done in {total_time} seconds.")
        st.subheader("📌 Final Summary")
        st.write("\n\n".join(summaries))

    except Exception as e:
        st.error(f"❌ Error: {e}")
