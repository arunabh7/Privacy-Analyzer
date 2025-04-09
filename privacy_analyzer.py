# privacy_analyzer_app.py

import streamlit as st
import spacy
import matplotlib.pyplot as plt
from collections import defaultdict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define privacy keywords
privacy_keywords = {
    "Data Collection": ["collect", "gather", "record", "store", "log"],
    "Tracking": ["track", "monitor", "cookie", "beacon"],
    "Third-Party Sharing": ["third party", "affiliates", "partners", "vendors"],
    "Location": ["location", "gps", "geolocation"],
    "Advertising": ["ads", "advertising", "marketing", "promotion"],
    "Data Sharing": ["share", "sell", "transfer", "disclose"],
    "Personal Info": ["email", "name", "phone", "address", "birthdate"],
}

# Analyze text using keyword matching and spaCy
def analyze_terms(text):
    results = defaultdict(list)
    doc = nlp(text.lower())

    for token in doc:
        for category, keywords in privacy_keywords.items():
            for keyword in keywords:
                if keyword in token.text:
                    results[category].append(keyword)

    return results

# Generate summary report
def generate_summary(results):
    summary = []
    for category, words in results.items():
        summary.append(f"{category}: {', '.join(set(words))}")
    return "\n".join(summary)

# Risk level calculation
def calculate_risk(results):
    score = len(results)
    if score <= 2:
        return "Low Risk", "🟢"
    elif score <= 4:
        return "Moderate Risk", "🟡"
    else:
        return "High Risk", "🔴"

# Plot chart
def plot_results(results):
    categories = list(results.keys())
    counts = [len(set(results[cat])) for cat in categories]

    fig, ax = plt.subplots()
    ax.barh(categories, counts, color="skyblue")
    ax.set_xlabel("Keyword Hits")
    ax.set_title("Privacy Risk Breakdown")
    st.pyplot(fig)

# Streamlit UI
st.set_page_config(page_title="App Privacy Analyzer", layout="centered")
st.title("🔍 App Privacy Analyzer")
st.markdown("Upload Terms & Conditions text and analyze it for privacy concerns.")

uploaded_file = st.file_uploader("Upload a text file (.txt)", type=["txt"])

if uploaded_file is not None:
    raw_text = uploaded_file.read().decode("utf-8")
    st.subheader("T&C Preview")
    st.text_area("Content", raw_text, height=200)

    if st.button("Analyze Privacy Risk"):
        with st.spinner("Analyzing..."):
            results = analyze_terms(raw_text)
            summary = generate_summary(results)
            risk, symbol = calculate_risk(results)

        st.success(f"*Risk Level:* {symbol} {risk}")
        st.markdown("### Analysis Summary")
        st.markdown(summary)
        st.markdown("### Visual Breakdown")
        plot_results(results)          