import fitz  # PyMuPDF

# Abre el PDF
pdf_path = 'Plantilla_respuestas.pdf'
pdf_document = fitz.open(pdf_path)

# Muestra el número de páginas
print(f"Número de páginas: {len(pdf_document)}")

# Extrae el texto
for page_num in range(len(pdf_document)):
    page = pdf_document.load_page(page_num)
    text = page.get_text()
    print(f"--- Página {page_num + 1} ---")
    print(text)

# Cierra el documento
pdf_document.close()
