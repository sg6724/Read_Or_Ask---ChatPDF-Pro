
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text



def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 10000 , chunk_overlap = 1000)
    return splitter.split_text(text)



