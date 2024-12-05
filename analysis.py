import streamlit as st
from sentence_transformers import SentenceTransformer
import requests
import json
from unstructured.partition.pdf import partition_pdf
from fpdf import FPDF
import os

# Initialize model and memory
embedding_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
memory = []

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        # Save the uploaded file temporarily to disk
        with open("temp_uploaded_file.pdf", "wb") as temp_file:
            temp_file.write(uploaded_file.read())
        
        # Use the saved file path with partition_pdf
        elements = partition_pdf("temp_uploaded_file.pdf")
        text = " ".join([str(element) for element in elements])
        
        # Cleanup the temporary file
        os.remove("temp_uploaded_file.pdf")
        
        return text
    except Exception as e:
        return f"Error extracting text: {e}"

# Function to generate response
def generate_response(context, question):
    global memory
    prompt = f"{context}\n{question}"
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": "llama3.2-vision:latest", "prompt": prompt, "stream": False}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        ans = result['response']
        memory.append(f"Q: {question}\nA: {ans}")
        if len(memory) > 5:
            memory = memory[-5:]
        return ans
    else:
        return "Error in generating response."

# Function to process text further with LLM
def further_process_with_llm(context, follow_up_question):
    response = generate_response(context, follow_up_question)
    return response

# Streamlit App
st.title("Solicitation Document Analyzer")

uploaded_file = st.file_uploader("Upload a Solicitation Document (PDF)", type=["pdf"])

if uploaded_file:
    # Extract text from the uploaded file
    with st.spinner("Extracting text..."):
        document_text = extract_text_from_pdf(uploaded_file)

    if "Error" in document_text:
        st.error(document_text)
    else:
        st.subheader("Extracted Text")
        st.text_area("Document Content", document_text, height=300)

        # Customizable questions
        st.subheader("Analysis")
        default_questions = [
            """1. Give solicitation ID, it would be a word starting with W, containing 12-15 letters with a combination of numbers and letters (e.g., W912DQ24R4002, W923FG23R3021). 
               2. List the required disciplines of engineers, their experience, and previous projects."""
        ]
        user_question = st.text_input("Ask a custom question (optional):")
        all_questions = default_questions
        if user_question:
            all_questions.append(user_question)

        # Analyze document
        if st.button("Analyze Document"):
            st.subheader("Extracted Information")
            results = {}
            for question in all_questions:
                response = generate_response(document_text, question)
                results[question] = response

            # Display initial analysis
            for question, answer in results.items():
                st.write(f"**{question}**: {answer}")

            # Further process specific parts of the analysis
            solicitation_id_question = "Extract just the solicitation ID from the above text."
            engineers_info_question = "Summarize the engineers' disciplines and experience required."

            solicitation_id = further_process_with_llm(results[default_questions[0]], solicitation_id_question)
            engineers_info = further_process_with_llm(results[default_questions[0]], engineers_info_question)

            # Assign variables and display
            st.subheader("Further Processed Information")
            st.write(f"**Solicitation ID:** {solicitation_id}")
            st.write(f"**Engineers Information:** {engineers_info}")

            # Save results to variables for other use cases
            final_solicitation_id = solicitation_id
            final_engineers_info = engineers_info

            # Download results as PDF
            if st.button("Download Results as PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, "Solicitation Analysis Results", ln=True, align='C')
                pdf.ln(10)
                pdf.multi_cell(0, 10, f"Solicitation ID:\n{final_solicitation_id}")
                pdf.ln(5)
                pdf.multi_cell(0, 10, f"Engineers Information:\n{final_engineers_info}")
                pdf_output_path = "solicitation_analysis.pdf"
                pdf.output(pdf_output_path)
                with open(pdf_output_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file,
                        file_name="solicitation_analysis.pdf",
                        mime="application/pdf"
                    )
