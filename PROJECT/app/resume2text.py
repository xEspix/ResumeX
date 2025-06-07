import fitz 
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import string

exclude=string.punctuation

class Pdf2Text:
    def __init__(self, file):
        self.file=file

    def createText(self):
        doc=fitz.open(self.file)
        pdf_txt=""
        for pg_no in range(doc.page_count):
            pg=doc.load_page(pg_no)
            txt=pg.get_text("text")
            pdf_txt+=txt

        doc.close()

        return pdf_txt
        