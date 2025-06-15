import fitz  # PyMuPDF
import os
import re
import unicodedata # For advanced text cleaning

def _clean_and_normalize_text(text: str) -> str:
    if not text:
        return ""
    # Normalize Unicode characters to their simplest form (NFKC).
    text = unicodedata.normalize('NFKC', text)
    # Replace common non-standard bullets or symbols with a standard one or remove them.
    text = re.sub(r'[•·●]', r'*', text)
    # Remove any remaining non-ASCII characters. This is an aggressive but effective
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Standardize whitespace. Replaces multiple spaces/newlines/tabs with a single space.
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_text_from_pdf(pdf_path: str) -> tuple[str | None, str | None]:
    if not os.path.exists(pdf_path):
        print(f"[pdf_to_text] Error: File not found at '{pdf_path}'")
        return None, None

    try:
        doc = fitz.open(pdf_path)
        
        raw_page_texts = []
        for page in doc:
            raw_page_texts.append(page.get_text("text"))
        doc.close()

        if not raw_page_texts:
            return "", ""

        # Join pages and perform basic normalization. This preserves paragraph structure.
        full_text_raw = "\n\n".join(raw_page_texts)
        text_for_regex = unicodedata.normalize('NFKC', full_text_raw).strip()
        
        text_for_pattern_matching = _clean_and_normalize_text(full_text_raw)
        
        return text_for_regex, text_for_pattern_matching
    
    except Exception as e:
        print(f"[pdf_to_text] Error processing PDF file '{pdf_path}': {e}")
        return None, None

