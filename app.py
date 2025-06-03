import streamlit as st
import datetime
from transformers import pipeline
import uuid

# Generate a unique session ID
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

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
        caret-color: #000000;
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
        color: #1a2e5b;
        font-weight: 600;
    }
    
    .footer a {
        color: #1a2e5b;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .footer a:hover {
        text-decoration: underline;
        color: #000000;
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
    return pipeline("summarization", model="facebook/bart-base")

summarizer = load_summarizer()

# Initialize entries for this session
@st.cache_data(ttl=3600, show_spinner=False)
def get_entries(session_id):
    return []

entries = get_entries(st.session_state.session_id)

# App UI
st.markdown('<h1 class="main-title">ChronoMind 📝 - Daily Journal Summarizer</h1>', unsafe_allow_html=True)

# Journal entry input
st.markdown('<div style="font-size: 18px; font-weight: 600; color: #000000; margin-bottom: 8px;">Enter your journal entry for today:</div>', unsafe_allow_html=True)
user_input = st.text_area("", height=80, label_visibility="collapsed")

if st.button("Submit Entry") and user_input.strip():
    today = datetime.date.today().isoformat()
    entries.append({"date": today, "text": user_input.strip()})
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
                    st.rerun()
else:
    st.info("No entries yet.")

# Generate weekly summaries
st.markdown('<h2 style="font-size: 16px; font-weight: 600; margin-bottom: 1rem;">🧠 Weekly Summaries</h2>', unsafe_allow_html=True)
if entries:
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
            # Calculate appropriate max_length based on input length
            input_length = len(combined_text.split())
            max_length = min(50, input_length // 2)  # Use half the input length, but cap at 50
            min_length = min(20, max_length // 2)    # Use half of max_length, but cap at 20
            
            summary = summarizer(
                combined_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True,
                no_repeat_ngram_size=3,
                length_penalty=1.0,
                num_beams=2
            )[0]['summary_text']
            if summary.lower().startswith('summary:'):
                summary = summary[len('summary:'):].strip()
            summaries[week] = summary

    for week, summary in summaries.items():
        st.markdown(f'<div class="summary-box"><strong>{week}</strong><br>{summary}</div>', unsafe_allow_html=True)

    if st.button("📤 Export Summaries to Text File"):
        with open("weekly_summaries.txt", "w") as f:
            for week, summary in summaries.items():
                f.write(f"{week}\n{summary}\n\n")
        st.success("Summaries exported to weekly_summaries.txt")
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
