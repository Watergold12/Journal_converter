import pdfplumber
from docx import Document

doc = Document()

def extract_text_from_pdf(pdf_path):
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            print(f"--- Page {i} ---")
            text = page.extract_text()
            if text:
                print(text)
                all_text += f"\n--- Page {i} ---\n" + text
                doc.add_paragraph(all_text)
                doc.save("extracted_text.docx")
            else:
                print("[No extractable text on this page, it might be a scanned image]")
    return all_text

file_path = "ZEPHYR_VISHAL_AA_24AD124_REPORT.pdf" 

extract_text_from_pdf(file_path)
