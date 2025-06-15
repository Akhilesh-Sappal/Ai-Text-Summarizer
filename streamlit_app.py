import streamlit as st
import streamlit.components.v1 as components
import requests
import time
from PIL import Image
import io

# --- Page Setup ---
st.set_page_config(page_title="AI Summarizer", page_icon="✨", layout="centered", initial_sidebar_state="collapsed")

# --- Custom CSS Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0f172a; color: white; }
.stApp { background-color: transparent; }

h1.title {
    font-size: 2.5rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.5rem;
    background: linear-gradient(to right, #ec4899, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.tab-button {
    display: inline-block;
    padding: 0.6rem 1.2rem;
    margin: 1rem 0.5rem;
    border-radius: 10px;
    border: 2px solid #a855f7;
    background: transparent;
    color: #d8b4fe;
    font-weight: 500;
    transition: all 0.3s ease;
    cursor: pointer;
}
.tab-button:hover {
    background: #a855f7;
    color: white;
}
textarea {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #475569 !important;
}
.stButton>button {
    background: linear-gradient(to right, #ec4899, #8b5cf6);
    border: none;
    border-radius: 8px;
    padding: 0.7rem 2rem;
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.03);
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
}
.result-box {
    background-color: #1e293b;
    padding: 1rem;
    border-radius: 12px;
    border-left: 4px solid #a855f7;
    margin-top: 1.5rem;
}
.metric-box {
    background: rgba(255,255,255,0.05);
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="title">✨ AI Text Summarizer</h1>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; font-size: 1.1rem; color:#cbd5e1;">Summarize Text or Image Instantly Using AI</div>', unsafe_allow_html=True)

# --- Toggle Option ---
option = st.radio("Choose Summarization Type:", ["📝 Text Summarization", "🖼️ Image Summarization"], horizontal=True, label_visibility="collapsed")

# --- Text Summarization ---
if option == "📝 Text Summarization":
    input_text = st.text_area("", placeholder="Paste text to summarize...", height=250)

    if st.button("🚀 Generate Summary"):
        if input_text.strip():
            with st.spinner("Summarizing..."):
                try:
                    response = requests.post("http://localhost:8000/summarize", data={"text": input_text})
                    result = response.json()
                    summary = result.get("Summary", "No summary returned.")
                    original_words = len(input_text.split())
                    summary_words = len(summary.split())
                    ratio = round((1 - summary_words / original_words) * 100, 1) if original_words > 0 else 0

                    st.success("✅ Summary generated!")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Original Words", original_words)
                    col2.metric("Summary Words", summary_words)
                    col3.metric("Compression", f"{ratio}%")

                    st.markdown(f"<div class='result-box'><b>📄 Summary:</b><br><br>{summary}</div>", unsafe_allow_html=True)

                    # WORKING Copy Button
                    components.html(f"""
                        <button onclick="navigator.clipboard.writeText(`{summary}`)"
                            style="margin-top:10px; padding:8px 16px; background-color:#8b5cf6; color:white; border:none; border-radius:6px; cursor:pointer;">
                            📋 Copy Summary
                        </button>
                    """, height=50)

                    st.download_button(
                        label="📥 Download as TXT",
                        data=summary,
                        file_name="summary.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter some text!")

# --- Image Summarization ---
else:
    uploaded_file = st.file_uploader("Upload an image containing text", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("🧠 Summarize Image"):
            with st.spinner("Extracting and summarizing text from image..."):
                try:
                    files = {"image": uploaded_file.getvalue()}
                    response = requests.post("http://localhost:8000/image-summarize", files=files)
                    result = response.json()
                    summary = result.get("Summary", "No summary returned.")
                    st.success("✅ Summary from image:")
                    st.markdown(f"<div class='result-box'>{summary}</div>", unsafe_allow_html=True)

                    # WORKING Copy Button
                    components.html(f"""
                        <button onclick="navigator.clipboard.writeText(`{summary}`)"
                            style="margin-top:10px; padding:8px 16px; background-color:#8b5cf6; color:white; border:none; border-radius:6px; cursor:pointer;">
                            📋 Copy Summary
                        </button>
                    """, height=50)

                    st.download_button(
                        label="📥 Download as TXT",
                        data=summary,
                        file_name="image_summary.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# --- Footer ---
st.markdown("---")
st.markdown(
    '<div style="text-align:center; font-size: 0.9rem; color:#64748b;">Powered by AI • Built by Akhilesh</div>',
    unsafe_allow_html=True
)
