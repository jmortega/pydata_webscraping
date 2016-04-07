from robobrowser import RoboBrowser

browser = RoboBrowser(history=True)

url = "http://docs.python.org.ar/tutorial/pdfs/TutorialPython3.pdf"
pdf_file_path = "local.pdf"

# do the login (e.g. via a login form)
request = browser.session.get(url, stream=True)

with open(pdf_file_path, "wb") as pdf_file:
    pdf_file.write(request.content)