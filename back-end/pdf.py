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


def train():
    text="Agente: Veo que tu crédito es de $1.200.000 y tienes 15 días de mora. Podemos dividirlo en 3 cuotas mensuales de $400.000 cada una. ¿Te parece conveniente este monto por cuota?;Agente: Tienes un crédito de $800.000 y 20 días de mora. Podemos dividirlo en 2 cuotas mensuales de $400.000 cada una. ¿Te parece conveniente este arreglo?;Agente: Entiendo, ¿te parecería mejor aumentar a 4 cuotas mensuales, de modo que cada cuota sea de $550.000?;Agente: Tienes un crédito de $950.000 y 25 días de mora. Podemos dividirlo en 2 cuotas quincenales de $475.000 cada una. ¿Te parece adecuado el monto por cuota?;Agente: Entiendo tu inquietud. Tienes un crédito de $1.800.000 y 40 días de mora. Podemos dividirlo en 3 cuotas mensuales de $600.000 cada una o, para reducir el valor por cuota, en 6 cuotas mensuales de $300.000 cada una. ¿Qué opción te parece mejor para adaptarse a tu presupuesto?;Agente: Comprendo tu situación. Tienes un crédito de $2.750.000 y 50 días de mora. Podemos dividirlo en 3 cuotas quincenales de $916.667 cada una. ¿Consideras que ese monto te resulta cómodo?;Agente: Tienes un crédito de $1.200.000 y 35 días de mora. Podemos ofrecerte 2 cuotas mensuales de $600.000 cada una o, si prefieres cuotas más bajas, 3 cuotas mensuales de $400.000 cada una. ¿Cuál opción te parece más adecuada?;Agente: Tienes un crédito de $700.000 y 45 días de mora. Podemos dividirlo en 2 cuotas mensuales de $350.000 cada una o en 3 cuotas quincenales de $233.333 cada una. ¿Qué opción consideras mejor para ti?;Agente: Tienes un crédito de $2.900.000 y 60 días de mora. Podemos dividirlo en 4 cuotas quincenales de $725.000 o en 5 cuotas mensuales de $580.000. ¿Cuál opción te parece que se adapta mejor a tus necesidades?;Agente: Entiendo, tienes un crédito de $1.350.000 y 70 días de mora. Podemos dividirlo en 4 cuotas mensuales de $337.500 cada una o, para que cada cuota sea menor, en 6 cuotas quincenales de $225.000 cada una. ¿Cuál opción prefieres?"
    return text