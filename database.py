from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
import base64
import os
from PyPDF2 import PdfReader

url = os.getenv("DATABASE_URL")
engine = create_engine(url, echo=True)

class PDF(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    content: bytes = Field(default=None)  # Binary PDF content
    extracted_text: str  # Keep text for search/query functionality

def init_db():
    # Drop all tables and recreate them (useful for development)
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
def save_pdf_to_db(uploaded_file):
    # Extract text for search/query functionality
    pdf_reader = PdfReader(uploaded_file)
    extracted_text = "".join(page.extract_text() for page in pdf_reader.pages)
    
    # Reset file pointer to beginning to read binary content
    uploaded_file.seek(0)
    content = uploaded_file.read()  # Read binary content
    
    pdf = PDF(name=uploaded_file.name, content=content, extracted_text=extracted_text)
    with Session(engine) as session:
        session.add(pdf)
        session.commit()

def get_all_pdfs():
    with Session(engine) as session:
        pdfs = session.exec(select(PDF)).all()
        result = []
        for pdf in pdfs:
            # Convert binary content to base64 for embedding in HTML
            pdf_base64 = base64.b64encode(pdf.content).decode('utf-8')
            result.append({
                "id": pdf.id,
                "name": pdf.name,
                "content_base64": pdf_base64,
                "extracted_text": pdf.extracted_text
            })
        return result

def delete_pdf_from_db(pdf_id):
    """Delete a PDF from the database by its ID."""
    with Session(engine) as session:
        pdf = session.get(PDF, pdf_id)
        if pdf:
            session.delete(pdf)
            session.commit()
        else:
            print(f"PDF with ID {pdf_id} not found.")