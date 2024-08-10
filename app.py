import streamlit as st
from qa_pipeline import QAPipeline
from database import Database
from utils import save_history_as_pdf
import os

# Initialize the app
st.set_page_config(page_title="Document Query Chatbot", layout="centered", page_icon="🤖")

# Set up a cleaner layout
st.title("📄 Document Query Chatbot by Aryan Singh")

# Initialize database and QA pipeline
db = Database('queries.db')
qa_pipeline = QAPipeline()

# File upload section
st.header("Upload Document")
uploaded_file = st.file_uploader("Upload a PDF, Word, or .txt file", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Extract text from the file
    file_text = qa_pipeline.extract_text(uploaded_file)
    
    if file_text:
        st.success("File uploaded and text extracted successfully!")
        
        # Query input section
        st.header("Ask a Question")
        query = st.text_input("Type your question based on the document")
        
        if query:
            # Get the answer from the QA pipeline
            answer = qa_pipeline.answer_query(file_text, query)
            
            # Save query and answer to the database
            db.save_query(uploaded_file.name, query, answer)
            
            # Display the answer
            st.write("**Answer:**", answer)
            st.success("Question answered successfully!")
            
        # Query history section
        st.header("Query History")
        
        # Show complete history in a single tabs
        if st.button("Show Query History"):
            history = db.get_history(uploaded_file.name)
            if history:
                st.subheader("Complete Query History")
                for idx, (query, answer) in enumerate(history, 1):
                    st.write(f"**Query {idx}:** {query}")
                    st.write(f"**Answer {idx}:** {answer}")
                    st.write("---")
                
                # Download chat history as PDF
                if st.button("Download Chat History as PDF"):
                    save_history_as_pdf(uploaded_file.name, db)
                    st.success("History saved as PDF.")
            else:
                st.info("No history available for this document.")
    else:
        st.error("Failed to extract text from the uploaded file.")
