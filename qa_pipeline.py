import torch
from transformers import BertTokenizer, BertForQuestionAnswering

class QAPipeline:
    def __init__(self):
        # Load the pre-trained TinyBERT model and tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('prajjwal1/bert-tiny')
        self.model = BertForQuestionAnswering.from_pretrained('prajjwal1/bert-tiny')
        
    def extract_text(self, file):
        # Assuming the file is a PDF, DOCX, or TXT
        # Add your file extraction logic here
        # For now, this is just a placeholder
        if file.type == "application/pdf":
            return self.extract_text_from_pdf(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return self.extract_text_from_docx(file)
        elif file.type == "text/plain":
            return self.extract_text_from_txt(file)
        else:
            return None

    def extract_text_from_pdf(self, file):
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def extract_text_from_docx(self, file):
        import docx
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    def extract_text_from_txt(self, file):
        return file.read().decode('utf-8')

    def answer_query(self, context, query):
        inputs = self.tokenizer(query, context, return_tensors='pt', truncation=True)
        input_ids = inputs['input_ids'].tolist()[0]

        outputs = self.model(**inputs)
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits

        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1

        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end])
        )

        return answer


