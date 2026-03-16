from docx import Document

doc = Document("D:/volume_e_files/Projects/ECLearnix/journal_converter/data/Raw Copy/demo_title.docx")

for para in doc.paragraphs:
    print(para.text)