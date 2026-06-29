import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

CHUNK_SIZE = 800
MODEL_NAME = "llama-3.3-70b-versatile"  # fast + free on Groq

CHUNK_PROMPT = """Summarize the following section of a document.
Extract key points, important facts, and actionable insights. Be concise.\n\n"""

MERGE_PROMPT = """You are given multiple partial summaries of a document.
Merge them into one coherent, concise final summary with key insights and actionable points."""