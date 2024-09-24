import streamlit as st
import PyPDF2
from openai import OpenAI
import os

# Inicjalizacja klienta OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_content(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "Jesteś asystentem specjalizującym się w analizie treści czasopism. Twoim zadaniem jest przeczytać treść czasopisma i stworzyć krótkie podsumowanie najważniejszych tematów i informacji."},
            {"role": "user", "content": f"Przeanalizuj poniższą treść czasopisma i stwórz krótkie podsumowanie najważniejszych tematów i informacji:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content

def generate_content(prompt, summary):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś doświadczonym copywriterem specjalizującym się w tworzeniu treści na podstawie czasopism."},
            {"role": "user", "content": f"{prompt}\n\nPodsumowanie treści czasopisma:\n{summary}"}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("Wirtualny Copywriter z Analizą OpenAI")

    uploaded_file = st.file_uploader("Wgraj plik PDF z czasopismem", type="pdf")

    if uploaded_file is not None:
        text_content = extract_text_from_pdf(uploaded_file)
        
        with st.spinner('Analizuję treść czasopisma...'):
            content_summary = analyze_content(text_content)
        
        st.subheader("Podsumowanie treści czasopisma")
        st.write(content_summary)

        st.subheader("Generowanie treści")

        if st.button("Generuj 'Z tego wydania dowiesz się'"):
            prompt = "Na podstawie podsumowania treści czasopisma, napisz krótkie podsumowanie 'Z tego wydania dowiesz się'. Wymień 3-5 najważniejszych punktów."
            result = generate_content(prompt, content_summary)
            st.write(result)

        if st.button("Generuj krótki opis wydania"):
            prompt = "Na podstawie podsumowania treści czasopisma, napisz krótki, zachęcający opis tego wydania w 2-3 zdaniach."
            result = generate_content(prompt, content_summary)
            st.write(result)

if __name__ == "__main__":
    main()
