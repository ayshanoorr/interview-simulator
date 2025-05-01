from PyPDF2 import PdfReader

def extract_text(file):
    reader = PdfReader(file.file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
