import streamlit as st
from textblob import TextBlob
import language_tool_python
from langdetect import detect, DetectorFactory
import pycountry

# --- Make language detection consistent
DetectorFactory.seed = 0

# Page configuration
st.set_page_config(page_title="NLP Text Analyzer", layout="wide")

# App title
st.title("🧠 NLP Text Analyzer")
st.write("Analyze text sentiment, detect language, and correct grammar — built with Python, TextBlob, LanguageTool, and LangDetect.")

# Text input
text = st.text_area("Enter your text here:", height=200)

# Analyze button
if st.button("Analyze"):
    if text.strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        # --- Sentiment Analysis ---
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity

        if sentiment > 0:
            mood = "Positive 😊"
        elif sentiment < 0:
            mood = "Negative 😞"
        else:
            mood = "Neutral 😐"

        # --- Language Detection (LangDetect + PyCountry) ---
        try:
            lang_code = detect(text)
            lang_name = pycountry.languages.get(alpha_2=lang_code)
            if lang_name:
                lang_result = f"{lang_name.name} ({lang_code.upper()})"
            else:
                lang_result = f"{lang_code.upper()} (unknown)"
        except Exception:
            lang_result = "Could not detect language"

        # --- Grammar Correction (LanguageTool first, fallback to TextBlob) ---
        try:
            tool = language_tool_python.LanguageToolPublicAPI('en-US')
            matches = tool.check(text)
            corrected = language_tool_python.utils.correct(text, matches)
            correction_info = "✅ LanguageTool correction applied."
        except Exception:
            corrected = str(blob.correct())
            correction_info = "⚠️ LanguageTool failed — used TextBlob correction as fallback."

        # --- Display results ---
        st.subheader("🔍 Analysis Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Sentiment Score", round(sentiment, 3))
        col2.metric("Mood", mood)
        col3.metric("Detected Language", lang_result)

        st.subheader("📝 Corrected Text")
        st.write(corrected)

        st.caption(correction_info)
