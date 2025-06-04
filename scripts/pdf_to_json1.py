import pdfplumber
import json
import os

def extract_chunks_from_pdf(pdf_path, chunk_size=750):
    chunks = []
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    words = full_text.split()
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i+chunk_size])
        chunks.append(chunk_text)
    return chunks


def save_chunks_as_jsonl(chunks, output_path, source_name="document.pdf"):
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, chunk in enumerate(chunks):
            json.dump({
                "id": f"chunk-{idx}",
                "content": chunk,
                "metadata": {
                    "source": source_name
                }
            }, f)
            f.write("\n")

if __name__ == "__main__":
    input_pdf = "../data/Hacking_the_Art_of_Exploitation.pdf"
    output_jsonl = "../data/hacking_chunks.jsonl"

    if not os.path.exists("../data"):
        os.makedirs("../data")

    chunks = extract_chunks_from_pdf(input_pdf)
    save_chunks_as_jsonl(chunks, output_jsonl)
    print(f"{len(chunks)} chunks written to {output_jsonl}")
