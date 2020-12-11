"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
2020_07_08 Tika Library Programming by Cheon Young Jo v.1.24
    - Install : pip install tika
    - Tika-python is java library, so required the recently version JDK.
    - 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from bs4 import BeautifulSoup
from tika import parser, language
import re, time

print("Tika Server Start...")
time.sleep(3)
PDF_FILE_NAME = "RS500N_users_guide.pdf"  #"LG-F700_UG_281.0_29_20161025.pdf"
KEY_WORD = "회전판"

parsed = parser.from_file(PDF_FILE_NAME, xmlContent=True)  # Exist ['metadata', 'content', 'status']
if parsed['status'] is not 200:
    raise Exception
print(parsed)
print("\nTotal Page : ", parsed['metadata']['xmpTPg:NPages'])
html = BeautifulSoup(parsed['content'], 'html.parser')
print("\n >>>", html)

print("\n=>", len(html.find_all(text=re.compile(KEY_WORD))))
for row in html.find_all(text=re.compile(KEY_WORD)):
    print(">", row, row.__dict__)

print(html.find_all(text=re.compile(KEY_WORD)))
