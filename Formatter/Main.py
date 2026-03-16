from engine.parser import DocumentParser
from engine.structure_detector import StructureDetector
from engine.document_model import DocumentModel, Section, SubSection
import re

file_path = r"C:\Users\SRI VIGNESH\Downloads\Eclearnix\Raw Copy\2602325 Full Paper.docx"

parser = DocumentParser(file_path)

detector = StructureDetector()

document = DocumentModel()

current_section = None

current_subsection = None


for para in parser.get_paragraphs():

    text = para.text.strip()

    block_type = detector.classify(para)

    if block_type=="IGNORE":

        continue


    # SECTION
    if block_type=="HEADING":

        match = re.match(r'^(\d+)\s+(.*)',text)

        if match:

            number = match.group(1)

            title = match.group(2)

        else:

            number = ""

            title = text


        current_section = Section(title,number)

        document.add_section(current_section)

        current_subsection = None

        continue


    # SUBSECTION
    elif block_type=="SUBHEADING":

        if current_section is None:

            continue

        match = re.match(r'^(\d+(\.\d+)+)\.?\s+(.*)',text)

        if match:

            number = match.group(1)

            title = match.group(3)

        else:

            number=""

            title=text


        current_subsection = SubSection(title,number)

        current_section.subsections.append(current_subsection)

        continue


    # BULLET
    elif block_type=="BULLET":

        if current_subsection:

            current_subsection.bullets.append(text)

        elif current_section:

            current_section.bullets.append(text)

        continue


    # PARAGRAPH
    else:

        if current_subsection:

            current_subsection.content.append(text)

        elif current_section:

            current_section.content.append(text)



print("\nDOCUMENT STRUCTURE")

print("------------------")


for section in document.sections:

    if section.number=="":

        print(f"\nSECTION: {section.title}")

    else:

        print(f"\nSECTION {section.number}: {section.title}")


    for para in section.content:

        print("   ",para)


    for bullet in section.bullets:

        print("   •",bullet)


    for sub in section.subsections:

        if sub.number=="":

            print(f"\n   SUBHEADING: {sub.title}")

        else:

            print(f"\n   SUBHEADING {sub.number}: {sub.title}")


        for para in sub.content:

            print("      ",para)


        for bullet in sub.bullets:

            print("      •",bullet)