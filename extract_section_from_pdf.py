import urllib
import io
from urllib.request import Request, urlopen
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def pdf_from_url_to_txt(url):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # Open the url provided as an argument to the function and read the content
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    f = urlopen(req).read()
    # f = urllib.request.urlopen(url).read()
    # Cast to StringIO object
    #fp = io.StringIO(f)
    fp = io.BytesIO(f)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = b""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp,
                                  pagenos,
                                  maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=False):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def extract_text(text):
    #section = text[text.find('Amendments to the \nRegulations'):text.rfind('BILLING  CODE')]
    section = text[text.find('Accordingly, 26 CFR'):text.rfind('BILLING  CODE')]
    return section

def extract_text_bug(text):
    #section = text[text.find('Amendments to the \nRegulations'):text.rfind('BILLING  CODE')]
    section = text[text.find('amended as \nfollows'):text.rfind('BILLING  CODE')]
    return section

