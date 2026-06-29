# 📄 Smart Summarizer

An AI-powered document summarization platform that extracts key insights from multi-page PDFs using **Groq LLM** and **Streamlit**.

---

## 🚀 Features

- Upload any PDF and get an instant AI-generated summary
- Chunk-based text processing to handle large documents
- Per-chunk summaries + merged final summary
- Word count, page count, and reading time stats
- Download summary as `.txt` file

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Groq API (LLaMA 3.3 70B) |
| PDF Parsing | PyPDF2 |
| Config | python-dotenv |

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/smart-summarizer.git
cd smart-summarizer
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add API key
```bash
cp .env.example .env
```
Edit `.env` and paste your Groq API key: