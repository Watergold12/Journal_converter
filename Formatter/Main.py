from engine.parser import DocumentParser
from engine.structure_detector import StructureDetector
from engine.sop_formatter import SOPFormatter
import os

file_path=r"C:\Users\SRI VIGNESH\Downloads\Eclearnix\Journal_converter\data\Raw_Copy\2602320_Full_Paper.docx"

parser=DocumentParser(file_path)

detector=StructureDetector()

source_doc=parser.get_document()

formatter=SOPFormatter(source_doc)

new_doc=formatter.build(detector)

os.makedirs("output",exist_ok=True)

new_doc.save("output/final_formatted.docx")

print("Conversion Completed Successfully")