import streamlit as st
import spacy
from spacy import displacy

# Title
st.title("Named Entity Recognition Web App")
st.markdown("🔍 Highlight entities like PERSON, DATE, ORG, etc.")

# Option to choose model
model_choice = st.radio("Choose NER Model:", ("Custom Model", "Pretrained Model"))

# Load the model
if model_choice == "Pretrained Model":
    nlp = spacy.load("en_core_web_sm")
else:
    try:
        nlp = spacy.load("model")
    except:
        st.error("❌ Custom model not found. Train the model and save it in the 'model/' directory.")
        st.stop()

# Text input
text_input = st.text_area("Enter text for NER:")

# Process button
if st.button("Analyze"):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        doc = nlp(text_input)
        html = displacy.render(doc, style="ent", jupyter=False)
        st.markdown(html, unsafe_allow_html=True)
