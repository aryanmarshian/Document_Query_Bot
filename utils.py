from fpdf import FPDF

def save_history_as_pdf(file_name, db):
    history = db.get_history(file_name)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for item in history:
        pdf.multi_cell(0, 10, f"Query: {item['query']}\nAnswer: {item['answer']}\n\n")

    pdf_file_name = file_name.replace(' ', '_') + '_chat_history.pdf'
    pdf.output(pdf_file_name)
    return pdf_file_name
