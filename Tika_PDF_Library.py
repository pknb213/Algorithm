"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
2020_07_08 Tika Library Programming by Cheon Young Jo v.1.24
    - Install : pip install tika
    - Tika-python is java library, so required the recently version JDK.
    - 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from bs4 import BeautifulSoup
from tika import parser, language
import re

PDF_FILE_NAME = "TV 매뉴얼.pdf"  #"LG-F700_UG_281.0_29_20161025.pdf"
KEY_WORD = "음소거"

parsed = parser.from_file(PDF_FILE_NAME, xmlContent=True)  # Exist ['metadata', 'content', 'status']
if parsed['status'] is not 200:
    raise Exception
print(parsed)
print("Total Page : ", parsed['metadata']['xmpTPg:NPages'])
html = BeautifulSoup(parsed['content'], 'html.parser')
print(html)
# print(html)
# print("=>", len(html.find_all(text=re.compile(KEY_WORD))))
# for row in html.find_all(text=re.compile(KEY_WORD)):
#     print(">", row)
#
# print(html.find_all(text=re.compile(KEY_WORD)))
