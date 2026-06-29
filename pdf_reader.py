import PyPDF2
import io

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract all text from uploaded PDF file.
    uploaded_file: Streamlit UploadedFile object
    Returns: full text as single string
    """
    text = ""
    
    try:
        # Read bytes from Streamlit file object
        pdf_bytes = uploaded_file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        
        total_pages = len(pdf_reader.pages)
        
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            
            if page_text:  # Some pages may return None
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page_text
        
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {str(e)}")
    
    if not text.strip():
        raise ValueError("No extractable text found. PDF may be scanned/image-based.")
    
    return text


def get_page_count(uploaded_file) -> int:
    """Return total page count of PDF."""
    pdf_bytes = uploaded_file.read()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    uploaded_file.seek(0)  # Reset pointer after read
    return len(pdf_reader.pages)