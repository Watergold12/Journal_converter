from engine.parser import DocumentParser
from engine.structure_detector import StructureDetector
from engine.document_model import DocumentModel, Section, SubSection

file_path = r"C:\Users\SRI VIGNESH\Downloads\Eclearnix\Raw Copy\2602325 Full Paper.docx"

parser = DocumentParser(file_path)
detector = StructureDetector()
document = DocumentModel()

section_count = 0
sub_count = 0

current_section = None
current_subsection = None

NON_NUMBERED = ["abstract","conclusion"]

for para in parser.get_paragraphs():

    text = para.text.strip()

    if text == "":
        continue

    block_type = detector.classify(para)

    # ======================
    # SECTION DETECTION
    # ======================

    if block_type == "HEADING":

        text_lower = text.lower()

        # Sections without numbering
        if text_lower in NON_NUMBERED:

            current_section = Section(text,"")

        else:

            section_count += 1

            current_section = Section(text,section_count)

        sub_count = 0

        document.add_section(current_section)

        current_subsection = None

        continue


    # ======================
    # SUBSECTION DETECTION
    # ======================

    elif block_type == "SUBHEADING":

        if current_section is None:
            continue

        sub_count += 1

        number = str(section_count)+"."+str(sub_count)

        current_subsection = SubSection(text,number)

        current_section.subsections.append(current_subsection)

        continue


    # ======================
    # PARAGRAPH CONTENT
    # ======================

    else:

        if current_subsection:

            current_subsection.content.append(text)

        elif current_section:

            current_section.content.append(text)


# ======================
# PRINT STRUCTURE
# ======================

print("\nDOCUMENT STRUCTURE")
print("------------------")

for section in document.sections:

    if section.number == "":

        print(f"\nSECTION: {section.title}")

    else:

        print(f"\nSECTION {section.number}: {section.title}")


    # Section paragraphs
    for para in section.content:

        print("   ",para)


    # Subsections
    for sub in section.subsections:

        print(f"\n   SUBHEADING {sub.number}: {sub.title}")

        for para in sub.content:

            print("      ",para)