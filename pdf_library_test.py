"""
2020_07_06 by Cheon Young Jo
A module to convert PDF Files to Text in Python.
1. PyPDF2 ( PDF to Text ) : Happen the Encoding Text
2. pdftotext ( PDF to Text ) : Happen the Install Error
3. pdftotree ( PDF to HTML ) : Not Test
4. pdfminer ( PDF to HTML ) : Difficult Code
5. tika-python (PDF to XML ) : Required JDK.
"""

# Using the PyPDF2
import PyPDF2


PDF_FILE_NAME = "TV 매뉴얼.pdf"
file = open('Elastic Logging.pdf', 'rb')
opend_pdf = PyPDF2.PdfFileReader(file)
print(opend_pdf, opend_pdf.numPages)
for i in range(0, opend_pdf.numPages):
    p = opend_pdf.getPage(i)
    p_text = p.extractText()
    p_lines = p_text.splitlines()
    print(p_text, type(p_text), p_lines, type(p_lines))
file.close()


# Using the pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_pdf_to_text():
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open('Elastic Logging.pdf', 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


v = convert_pdf_to_text()
print(v)


# Using the tika
from bs4 import BeautifulSoup
import tika, re
# tika.initVM()
from tika import parser, language
parsed = parser.from_file(PDF_FILE_NAME, xmlContent=True)

# fileOut = open('tika_output.txt', 'w', encoding='utf-8')
# print(">>>", parsed['content'], file=fileOut)
# fileOut.close()

print(parsed['content'], dir(parsed), parsed["metadata"], parsed["metadata"]["xmpTPg:NPages"])
print(">>>", tika.language.from_file(PDF_FILE_NAME))

html = BeautifulSoup(parsed['content'], 'html.parser')
# html = html.prettify()
print(html)
KEYWORD = "음소거"
print(">>", html.find_all(text=KEYWORD), len(html.find_all(text=KEYWORD)))
print(">>>>", html.find_all(text=re.compile(KEYWORD)), len(html.find_all(text=re.compile(KEYWORD))))

for i in html.find_all(text=re.compile(KEYWORD)):
    print(">", i)
