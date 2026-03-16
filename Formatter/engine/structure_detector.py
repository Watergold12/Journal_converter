import re

class StructureDetector:

    def is_title(self,para):

        text = para.text.strip()

        if len(text) == 0:
            return False

        if len(text.split()) > 15:
            return False

        for run in para.runs:

            if run.bold:

                if run.font.size:

                    if run.font.size.pt >= 15:

                        return True

        return False


    def is_author(self,para):

        text = para.text.strip()

        if "," not in text:
            return False

        for run in para.runs:

            if run.italic:

                return True

        return False


    def is_heading(self,para):

        text = para.text.strip().lower()

        SECTION_KEYWORDS = [

            "abstract",
            "introduction",
            "review of literature",
            "method",
            "methodology",
            "results",
            "result and discussion",
            "discussion",
            "conclusion",
            "reference",
            "references",
            "acknowledgements"

        ]

        # exact section names
        if text in SECTION_KEYWORDS:
            return True

        # detect numbered sections like:
        # 1 INTRODUCTION
        # 2 METHOD
        if re.match(r'^\d+\s+[A-Za-z]', para.text):
            return True

        return False


    def is_subheading(self,para):

        text = para.text.strip()

        if len(text) == 0:
            return False

        # detect 2.1 style headings
        if re.match(r'^\d+\.\d+', text):
            return True

        # detect bold short lines (likely subsection)
        if len(text.split()) <= 8:

            for run in para.runs:

                if run.bold:

                    return True

        return False


    def classify(self,para):

        if self.is_title(para):
            return "TITLE"

        if self.is_author(para):
            return "AUTHOR"

        if self.is_heading(para):
            return "HEADING"

        if self.is_subheading(para):
            return "SUBHEADING"

        return "PARAGRAPH"