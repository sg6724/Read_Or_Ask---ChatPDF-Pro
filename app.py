import streamlit as st
from pdf_service import get_pdf_text, split_text
from vector_embeddings import save_vector_store, load_vector_store
from chatbot import handle_user_input
from database import save_pdf_to_db, get_all_pdfs, init_db, delete_pdf_from_db
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config("PDF Reader Project", layout="wide")

init_db()

st.title("📘 Your PDF READER is here!")
st.subheader("Read or Ask! As you wish !🙂")

#Tabbed Interface
tab1, tab2, tab3 = st.tabs(["📤 Upload PDFs", "📖 Read PDFs", "🤖 Ask PDFbot"])

#Upload PDFs Tab
with tab1:
    st.header("Upload PDFs to Database")
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if st.button("Upload and Process"):
        if not uploaded_files:
            st.warning("Please select at least one PDF file to upload.")
        else:
            with st.spinner("Uploading PDFs to database..."):
                for file in uploaded_files:
                    save_pdf_to_db(file)  # Save to database
                st.success("PDFs uploaded to database successfully!")

            with st.spinner("Processing and indexing all PDFs..."):
                # Process all PDFs in the database for vector store
                pdfs = get_all_pdfs()
                all_text = ""
                
                # Combine all PDF text
                for pdf in pdfs:
                    all_text += pdf["extracted_text"] + "\n\n"
                
                # Split text into chunks
                text_chunks = split_text(all_text)
                
                # Save to vector store
                success = save_vector_store(text_chunks, "combined_pdfs")
                
                if success:
                    st.success("All PDFs processed and indexed for searching!")
                else:
                    st.error("Failed to index PDFs. Please check the logs.")

            for file in uploaded_files:
                with st.expander(f"Preview of {file.name}"):
                    file.seek(0)  # Reset file pointer
                    text = get_pdf_text([file])
                    st.text(text[:1000] + "..." if len(text) > 1000 else text)

# Read PDFs Tab
with tab2:
    st.header("Available PDFs")
    pdfs = get_all_pdfs()

    if not pdfs:
        st.info("No PDFs found in the database.")
    else:
        for pdf in pdfs:
            st.markdown(f"📄 **{pdf['name']}**")
            
            # Create tabs for viewing options
            pdf_tabs = st.tabs(["PDF Viewer", "Raw Text"])
            
            # Tab 1: PDF Viewer (displays original PDF)
            with pdf_tabs[0]:
                # Display the PDF using HTML embed
                pdf_display = f'<embed src="data:application/pdf;base64,{pdf["content_base64"]}" width="100%" height="600" type="application/pdf">'
                st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Tab 2: Raw Text (shows extracted text for search and copy-paste)
            with pdf_tabs[1]:
                st.text_area("Extracted Text", value=pdf["extracted_text"][:5000] + "..." if len(pdf["extracted_text"]) > 5000 else pdf["extracted_text"], 
                            height=400, key=f"text_area_{pdf['id']}")

            # Add delete button for each PDF
            if st.button(f"Delete {pdf['name']}", key=f"delete_{pdf['id']}"):
                delete_pdf_from_db(pdf['id'])
                
                # Reprocess remaining PDFs for vector store
                updated_pdfs = get_all_pdfs()
                if updated_pdfs:
                    all_text = ""
                    for pdf in updated_pdfs:
                        all_text += pdf["extracted_text"] + "\n\n"
                    
                    text_chunks = split_text(all_text)
                    save_vector_store(text_chunks, "combined_pdfs")
                
                st.success(f"Deleted {pdf['name']} successfully!")
                st.experimental_rerun()
                
                
#Ask PDFbot Tab
with tab3:
    st.header("Ask PDFbot 🤖")
    
    pdfs = get_all_pdfs()
    if not pdfs:
        st.warning("No PDFs found to ask about. Please upload PDFs first.")
    else:
        question = st.text_input("Ask a question about the uploaded PDFs")

    # Process the question
    if st.button("Go!", key="ask_pdfbot_go") and question:
        handle_user_input(question)