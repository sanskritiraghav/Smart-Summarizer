import streamlit as st
import io
from pdf_reader import extract_text_from_pdf, get_page_count
from summarizer import summarize_document
from utils import estimate_read_time, get_word_count

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Summarizer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Smart Summarizer")
st.caption("Upload a PDF → Get AI-powered summary using Google Gemini")

# ── File Upload ───────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"],
    help="Multi-page PDFs supported. Large files auto-chunked."
)

if uploaded_file is not None:

    # ── File Stats ─────────────────────────────────────────────
    page_count = get_page_count(uploaded_file)
    uploaded_file.seek(0)  # Reset after get_page_count reads it

    st.info(f"📑 **{uploaded_file.name}** — {page_count} pages detected")

    # ── Summarize Button ───────────────────────────────────────
    if st.button("✨ Summarize", use_container_width=True, type="primary"):

        with st.spinner("Reading PDF..."):
            try:
                raw_text = extract_text_from_pdf(uploaded_file)
            except ValueError as e:
                st.error(str(e))
                st.stop()

        word_count = get_word_count(raw_text)
        read_time = estimate_read_time(raw_text)

        st.caption(f"📊 {word_count:,} words · ~{read_time} min read")

        # ── Progress Bar ───────────────────────────────────────
        st.markdown("**Summarizing chunks...**")
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(current, total):
            percent = int((current / total) * 100)
            progress_bar.progress(percent)
            status_text.text(f"Processing chunk {current} of {total}...")

        # ── Run Summarizer ─────────────────────────────────────
        try:
            result = summarize_document(raw_text, progress_callback=update_progress)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

        progress_bar.progress(100)
        status_text.text("Done!")

        # ── Display Summary ────────────────────────────────────
        st.success("✅ Summary ready!")

        st.markdown("## 📝 Final Summary")
        st.markdown(result["final_summary"])

        # ── Stats ──────────────────────────────────────────────
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Pages", page_count)
        col2.metric("Words", f"{result['word_count']:,}")
        col3.metric("Chunks Processed", result["chunk_count"])

        # ── Expandable Partial Summaries ───────────────────────
        if result["chunk_count"] > 1:
            with st.expander("🔍 View Per-Chunk Summaries"):
                for i, partial in enumerate(result["partial_summaries"]):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.markdown(partial)
                    st.divider()

        # ── Download Button ────────────────────────────────────
        st.download_button(
            label="⬇️ Download Summary (.txt)",
            data=result["final_summary"],
            file_name=f"{uploaded_file.name.replace('.pdf', '')}_summary.txt",
            mime="text/plain",
            use_container_width=True
        )