# pdf to text extractor
# conversion: pdf -> one long string

import fitz
import os

def extract_text_from_pdf(pdf_path: str) -> tuple[str | None, str | None]:
    if not os.path.exists(pdf_path):
        print(f"[pdf_to_text] Error: File not found at '{pdf_path}'")
        return None, None

    if not pdf_path.lower().endswith(".pdf"):
        print(f"[pdf_to_text] Error: File '{pdf_path}' is not a PDF.")
        return None, None
    
    try:
        doc = fitz.open(pdf_path)

        raw_page_texts = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            raw_page_texts.append(page.get_text("text"))
        
        doc.close()

        if not raw_page_texts:
            return "", ""
        
        text_for_regex = "\n\n".join(raw_page_texts).strip()

        text_for_pattern_matching = " ".join(text_for_regex.split()).strip()

        return text_for_regex, text_for_pattern_matching
    
    except fitz.errors.FitzAuthError: # For password-protected PDFs
        print(f"[pdf_to_text] Error: PDF file '{pdf_path}' is password-protected and cannot be opened.")
        return None, None
    except Exception as e:
        print(f"[pdf_to_text] Error processing PDF file '{pdf_path}': {e}")
        return None, None