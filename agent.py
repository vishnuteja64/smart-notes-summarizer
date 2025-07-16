from transformers import pipeline

# ✅ Fast, open-source LLM
summarizer = pipeline(
    "summarization",
    model="Falconsai/text_summarization",
    tokenizer="Falconsai/text_summarization"
)

def extract_text_from_pdf(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_into_chunks(text, max_tokens=300):
    words = text.split()
    chunks = [' '.join(words[i:i + max_tokens]) for i in range(0, len(words), max_tokens)]
    return chunks

def summarize_chunks_batch(chunks, batch_size=4):
    summaries = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        try:
            results = summarizer(batch, max_length=60, min_length=15, do_sample=False)
            summaries.extend([result['summary_text'] for result in results])
        except Exception as e:
            summaries.append(f"❌ Error summarizing batch {i // batch_size + 1}: {e}")
    return summaries
