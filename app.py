import streamlit as st
import datetime
import os
import json
from transformers import pipeline
import speech_recognition as sr

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');
    
    .stApp {
        background-color: #c6e2ff;
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #1a2e5b;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stButton button {
        background-color: #ffdb7d;
        color: #000000;
        font-size: 14px;
        font-weight: normal;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
    }
    
    .stButton button:hover {
        background-color: #f7c948;
    }
    
    .stTextArea textarea {
        background-color: #ffefb8;
        border-radius: 6px;
        font-size: 16px;
        color: #000000;
    }
    
    .timeline-entry {
        background-color: #ffefb8;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        color: #000000;
    }
    
    .summary-box {
        background-color: #ffefb8;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #000000;
    }
    
    .footer {
        display: flex;
        justify-content: space-between;
        margin-top: 2rem;
        color: #f7c948;
        font-weight: 600;
    }
    
    .footer a {
        color: #f7c948;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }

    /* Fix text color in radio buttons */
    .stRadio > div {
        color: #000000;
    }

    /* Fix text color in labels */
    .stMarkdown {
        color: #000000;
    }

    /* Fix text color in info messages */
    .stInfo {
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# Load summarizer
@st.cache_resource
def load_summarizer():
    try:
        return pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception as e:
        st.error(f"Error loading summarizer: {str(e)}")
        return None

summarizer = load_summarizer()

# File to store entries
DATA_FILE = "journal_entries.json"

# Load or initialize entries
def load_entries():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Error loading entries: {str(e)}")
        return []

def save_entries(entries):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(entries, f)
    except Exception as e:
        st.error(f"Error saving entries: {str(e)}")

entries = load_entries()

# Voice input
def get_voice_input():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Please speak now.")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError:
            st.error("Could not request results.")
    except Exception as e:
        st.error("Voice input is not available in this environment.")
    return ""

# App UI
st.markdown('<h1 class="main-title">ChronoMind 📝 - Daily Journal Summarizer</h1>', unsafe_allow_html=True)

# Input mode selection
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div style="font-size: 16px; font-weight: 600; color: #000000;">Input Mode</div>', unsafe_allow_html=True)
with col2:
    input_mode = st.radio("", ["Type", "Voice"], horizontal=True, label_visibility="collapsed")

# Journal entry input
if input_mode == "Type":
    st.markdown('<div style="font-size: 18px; font-weight: 600; color: #000000; margin-bottom: 8px;">Enter your journal entry for today:</div>', unsafe_allow_html=True)
    user_input = st.text_area("", height=150, label_visibility="collapsed")
else:
    if st.button("🎤 Record Voice"):
        user_input = get_voice_input()
    else:
        user_input = ""

if st.button("Submit Entry") and user_input.strip():
    today = datetime.date.today().isoformat()
    entries.append({"date": today, "text": user_input.strip()})
    save_entries(entries)
    st.success("Entry saved.")

# Display timeline
st.markdown('<h2 style="font-size: 16px; font-weight: 600; margin-bottom: 1rem;">📅 Journal Timeline</h2>', unsafe_allow_html=True)
if entries:
    for i, e in enumerate(reversed(entries)):
        with st.container():
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                st.markdown(f'<div class="timeline-entry"><strong>{e["date"]}</strong>: {e["text"]}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    actual_index = len(entries) - 1 - i
                    entries.pop(actual_index)
                    save_entries(entries)
                    st.rerun()
else:
    st.info("No entries yet.")

# Generate weekly summaries
st.markdown('<h2 style="font-size: 16px; font-weight: 600; margin-bottom: 1rem;">🧠 Weekly Summaries</h2>', unsafe_allow_html=True)
if entries and summarizer:
    # Group entries by week
    grouped = {}
    for entry in entries:
        date_obj = datetime.date.fromisoformat(entry["date"])
        week = f"Week {date_obj.isocalendar()[1]} ({date_obj.strftime('%Y')})"
        grouped.setdefault(week, []).append(entry["text"])

    summaries = {}
    for week, texts in grouped.items():
        combined_text = " ".join(texts)
        if len(combined_text.split()) > 5:
            try:
                summary = summarizer(
                    combined_text,
                    max_length=100,
                    min_length=30,
                    do_sample=False,
                    num_beams=4,
                    length_penalty=2.0,
                    early_stopping=True
                )[0]['summary_text']
                if summary.lower().startswith('summary:'):
                    summary = summary[len('summary:'):].strip()
                summaries[week] = summary
            except Exception as e:
                st.error(f"Error generating summary for {week}: {str(e)}")

    for week, summary in summaries.items():
        st.markdown(f'<div class="summary-box"><strong>{week}</strong><br>{summary}</div>', unsafe_allow_html=True)

    if st.button("📤 Export Summaries to Text File"):
        try:
            with open("weekly_summaries.txt", "w") as f:
                for week, summary in summaries.items():
                    f.write(f"{week}\n{summary}\n\n")
            st.success("Summaries exported to weekly_summaries.txt")
        except Exception as e:
            st.error(f"Error exporting summaries: {str(e)}")
else:
    if not summarizer:
        st.error("Summarizer is not available. Please try refreshing the page.")
    else:
        st.info("Add entries to generate summaries.")

# Footer
st.markdown("""
<div class="footer">
    <a href="https://github.com/Nishantr846" target="_blank">
        <i class="fab fa-github"></i>
        <span>Nishantr846</span>
    </a>
    <a href="https://nishantr846.github.io/Portfolio-Website/index.html" target="_blank">
        <img src="https://storage.googleapis.com/a1aa/image/264b7227-b4ae-4bb9-13c8-a2f144802244.jpg" 
             style="width: 20px; height: 20px; border-radius: 50%;">
        <span>Portfolio</span>
    </a>
    <a href="https://linkedin.com/in/Nishantr846" target="_blank">
        <i class="fab fa-linkedin"></i>
        <span>Nishantr846</span>
    </a>
</div>
""", unsafe_allow_html=True)
