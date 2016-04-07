from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from robobrowser import RoboBrowser
import requests


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')

    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    parser.set_document(doc)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

browser = RoboBrowser(history=True)
url = "http://pythonscraping.com/pages/warandpeace/chapter1.pdf";
pdf_file_path = "local.pdf"

# do the login (e.g. via a login form)
request = browser.session.get(url, stream=True)

with open(pdf_file_path, "wb") as pdf_file:
    pdf_file.write(request.content)
    
response = requests.get(url, stream=True)
outputString = convert_pdf_to_txt(pdf_file_path)
print(outputString)