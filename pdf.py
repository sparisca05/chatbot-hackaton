import fitz  # PyMuPDF

def pdf():
    # Abre el PDF
    pdf_path = './Files/respuesta.pdf'
    pdf_document = fitz.open(pdf_path)
    text=""

    # Extrae el texto
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    
    return text