import requests
import docx2txt
from io import BytesIO

url = "https://downloads.regulations.gov/IRS-2007-0114-0041/attachment_1.doc"
url = "https://downloads.regulations.gov/IRS-2011-0001-0063/attachment_1.docx"
docx = BytesIO(requests.get(url).content)

# extract text
text = docx2txt.process(docx)
text = textract.process(docx)
response = requests.get("https://downloads.regulations.gov/IRS-2007-0114-0041/attachment_1.doc").content
print(response.text)



from urllib.request import urlopen
from bs4 import BeautifulSoup
from io import BytesIO
from zipfile import ZipFile
import zipfile

file = urlopen(url).read()
file = BytesIO(file)
document = zipfile.ZipFile(file)
content = document.read('word/document.xml')
word_obj = BeautifulSoup(content.decode('utf-8'))
text_document = word_obj.findAll('w:t')
for t in text_document:
    print(t.text)