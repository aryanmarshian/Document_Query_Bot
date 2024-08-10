# Document_Query_Bot

## Overview

The Document Query Chatbot is a Streamlit application that allows users to upload PDF, Word, or text files and ask questions based on the content of those documents. The application utilizes a pre-trained TinyBERT model for question answering and maintains a query history for user reference.

## Features

- Upload documents in PDF, Word, or text format.
- Ask questions based on the uploaded document.
- View the query history for each document.
- Download the query history as a PDF.
- User-friendly interface with a minimalist design.

## Requirements

To run this application, you will need the following:

- Python 3.6 or higher
- Streamlit
- Transformers
- PyPDF2
- python-docx
- SQLite
- FPDF
- Cryptography
- Datasets (optional for fine-tuning)

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/document-query-chatbot.git
   cd document-query-chatbot
2. Install the required packages:
   ```bash
   pip install streamlit transformers PyPDF2 python-docx fpdf cryptography datasets torch
   
3. Start the Streamlit application:
   ```bash
   streamlit run app.py


   
