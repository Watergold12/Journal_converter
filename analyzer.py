import re
from docx import Document

doc = Document("data/Raw Copy/2602320 Full Paper.docx")

pattern = r'^\d+\.\d+'

# sections that should never be treated as subheadings
excluded_sections = {"REFERENCES", "ACKNOWLEDGEMENTS"}

for para in doc.paragraphs:

    text = para.text.strip()

    if not text:
        continue

    # ---------------- TITLE DETECTION ----------------
    is_title = False
    for run in para.runs:
        if run.font.size and run.font.size.pt > 12:
            print("TITLE:", text)
            is_title = True
            break

    if is_title:
        continue

    # ---------------- SECTION DETECTION ----------------
    if text.isupper():
        print("SECTION:", text)
        continue

    # ---------------- SUBHEADING DETECTION ----------------
    if text.upper() in excluded_sections:
        continue

    numPr = para._element.xpath('./w:pPr/w:numPr')

    if numPr:

        # extract numbering level
        level = numPr[0].xpath('./w:ilvl/@w:val')
        numId = numPr[0].xpath('./w:numId/@w:val')

        if level and int(level[0]) >= 1:

            # try extracting the numbering prefix
            number_match = re.match(pattern, text)

            if number_match:
                number = number_match.group()
                heading_text = text[len(number):].strip()
                print(f"SUBHEADING: {number} {heading_text}")
            else:
                print("SUBHEADING:", text)

        continue

    # ---------------- REGEX FALLBACK ----------------
    if re.match(pattern, text):

        if "reference" in text.lower():
            continue

        print("SUBHEADING:", text)

# import re
# from docx import Document

# doc = Document("data/Raw Copy/2602320 Full Paper.docx")

# section_pattern = r'^\d+\.'        # 1. 2. 3.
# subheading_pattern = r'^\d+\.\d+'  # 1.1 2.3

# excluded_sections = {"REFERENCES", "ACKNOWLEDGEMENTS", "ACKNOWLEDGMENTS"}

# for para in doc.paragraphs:

#     text = para.text.strip()

#     if not text:
#         continue

#     # ---------------- TITLE DETECTION ----------------
#     is_title = False
#     for run in para.runs:
#         if run.font.size and run.font.size.pt > 12:
#             print("TITLE:", text)
#             is_title = True
#             break

#     if is_title:
#         continue

#     # ---------------- SECTION DETECTION ----------------
#     section_match = re.match(section_pattern, text)

#     if section_match:

#         number = section_match.group()
#         name = text[len(number):].strip()

#         if name.upper() not in excluded_sections:
#             print(f"SECTION: {number} {name}")
#         else:
#             print(f"SECTION: {name}")

#         continue

#     # ---------------- SUBHEADING DETECTION ----------------
#     sub_match = re.match(subheading_pattern, text)

#     if sub_match:

#         number = sub_match.group()
#         name = text[len(number):].strip()

#         if "reference" not in name.lower():
#             print(f"SUBHEADING: {number} {name}")

#         continue