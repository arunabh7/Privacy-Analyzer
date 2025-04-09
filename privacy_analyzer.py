import streamlit as st
import spacy
import os
import matplotlib.pyplot as plt
from collections import Counter

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Privacy-related keywords (you can expand this list)
PRIVACY_KEYWORDS = [
    "data collection", "third-party", "personal information", "cookies",
    "tracking", "location data", "data sharing", "opt-out", "analytics",
    "advertising", "consent", "retention", "GDPR", "CCPA", "sale of data",
    "biometric", "camera", "microphone", "contact list", "SMS", "email",
    "IP address", "device ID", "profiling"
]

# Title
st.set_page_config(page_title="App Privacy Analyzer", layout="wide")
st.title("🔒 App Privacy Analyzer")

# Upload T&C text file
uploaded_file = st.file_uploader("Upload the Terms & Conditions file (TXT format)", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    # Display raw text
    with st.expander("📄 View Uploaded Terms & Conditions"):
        st.text_area("Raw Text", text, height=300)

    # NLP Processing
    doc = nlp(text)
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]

    # Keyword Detection
    detected_keywords = [word for word in tokens if any(kw in word for kw in PRIVACY_KEYWORDS)]
    keyword_freq = Counter(detected_keywords)

    # Summary
    st.subheader("🔍 Privacy Risk Summary")
    if keyword_freq:
        total_mentions = sum(keyword_freq.values())
        st.success(f"✅ Found {total_mentions} potential privacy-related mentions.")

        # Plot
        fig, ax = plt.subplots()
        top_k = keyword_freq.most_common(10)
        labels, values = zip(*top_k)
        ax.barh(labels, values, color="crimson")
        ax.set_xlabel("Frequency")
        ax.set_title("Top Privacy-Related Terms")
        st.pyplot(fig)

        # Table View
        with st.expander("📊 View Detailed Keyword Frequency"):
            st.write({k: v for k, v in top_k})
    else:
        st.warning("⚠️ No privacy-related keywords found. This may indicate low risk, or vague T&C language.")

    # Optional: Additional analysis (e.g., named entities, sentiment)
    with st.expander("🧠 Advanced NLP Insights"):
        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        st.write(f"People Mentioned: {set(persons)}")
        st.write(f"Organizations Mentioned: {set(orgs)}")
else:
    st.info("📤 Please upload a T&C file to begin analysis.")
