import streamlit as st
from ebooklib import epub
from bs4 import BeautifulSoup
from googletrans import Translator

st.title("ePub Translator")

uploaded_file = st.file_uploader("Upload your ePub file", type=["epub"])
target_lang = st.selectbox("Select target language", ["th", "es", "fr", "de", "zh-cn", "ja"])

if uploaded_file:
    book = epub.read_epub(uploaded_file)
    translator = Translator()
    translated_chapters = []

    for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            text = soup.get_text(separator="\n").strip()
            if not text:
                continue

            parts = [text[i:i+4000] for i in range(0, len(text), 4000)]
            chapter_translations = []
            for part in parts:
                translated = translator.translate(part, dest=target_lang).text
                chapter_translations.append(translated)
            full_text = "\n".join(chapter_translations)
            translated_chapters.append(full_text)

    full_book = "\n\n".join(translated_chapters)
    st.download_button("Download Translation", full_book, file_name="translated_book.txt")


