import streamlit as st
import PyPDF2
import difflib
import re

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def count_full_mistakes(pdf_text, user_text):
    full_mistakes = 0
    pdf_words = pdf_text.split()
    user_words = user_text.split()

    full_mistakes += len(set(pdf_words) - set(user_words))

    full_mistakes += len(set(user_words) - set(pdf_words))

    matcher = difflib.SequenceMatcher(None, pdf_text, user_text)
    full_mistakes += int((1 - matcher.ratio()) * len(pdf_words)) 

    for word in user_words:
        if word != word.lower():
            full_mistakes += 1
    
    return full_mistakes

def count_half_mistakes(pdf_text, user_text):
    half_mistakes = 0

    pdf_words = pdf_text.split()
    user_words = user_text.split()
    
    for pdf_word, user_word in zip(pdf_words, user_words):
        if pdf_word.lower() != user_word.lower():
            half_mistakes += 1
    
    for pdf_word, user_word in zip(pdf_words, user_words):
        if pdf_word.rstrip('s') == user_word.rstrip('s'):
            half_mistakes += 1

    if not user_text.endswith('.'):
        half_mistakes += 1
    if not user_text[0].isupper():
        half_mistakes += 1

    return half_mistakes

st.title('Stenography For Prashant Baby!')

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

user_text = st.text_area("Enter text for comparison", height=300)

if uploaded_file is not None and user_text:
    pdf_text = extract_text_from_pdf(uploaded_file)

    full_mistakes = count_full_mistakes(pdf_text, user_text)
    half_mistakes = count_half_mistakes(pdf_text, user_text)
    
    total_mistakes = full_mistakes + (half_mistakes / 2)

    num_words_pdf = len(pdf_text.split())

    percentage_errors = (total_mistakes / num_words_pdf) * 100

    st.write(f"Full Mistakes: {full_mistakes}")
    st.write(f"Half Mistakes: {half_mistakes}")
    st.write(f"Percentage of Errors: {percentage_errors:.2f}%")

    if percentage_errors > 90:
        st.success("The texts match very closely!")
    else:
        st.warning("The texts do not match closely.")
