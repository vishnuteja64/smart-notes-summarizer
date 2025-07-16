# agent.py
import fitz  #  module from PyMuPDF
from transformers import pipeline

summarizer = pipeline("summarization")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_into_chunks(text, max_tokens=500):
    words = text.split()
    chunks = [' '.join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]
    return chunks

def summarize_chunks(chunks):
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return "\n\n".join(summaries)

if __name__ == "__main__":
    text = extract_text_from_pdf("AI-whitepaper.pdf")
    print("✅ Extracted PDF Text:")
    print(text[:1000])

    chunks = split_into_chunks(text)
    print(f"\n✅ Total chunks: {len(chunks)}")

    summary = summarize_chunks(chunks)
    print("\n✅ Summary:\n")
    print(summary)
