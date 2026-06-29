import re
from config import CHUNK_SIZE


def clean_text(text: str) -> str:
    """
    Remove noise from extracted PDF text.
    Fixes: extra whitespace, weird line breaks, repeated newlines.
    """
    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)
    
    # Collapse multiple spaces into one
    text = re.sub(r' +', ' ', text)
    
    # Collapse 3+ newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.splitlines()]
    text = '\n'.join(lines)
    
    return text.strip()


def split_into_chunks(text: str, chunk_size: int = CHUNK_SIZE) -> list[str]:
    """
    Split text into word-based chunks.
    chunk_size: max words per chunk
    Returns: list of text chunks
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk = words[i : i + chunk_size]
        chunks.append(' '.join(chunk))
    
    return chunks


def estimate_read_time(text: str) -> int:
    """
    Estimate reading time in minutes.
    Avg reading speed: 200 words/min
    """
    word_count = len(text.split())
    return max(1, round(word_count / 200))


def get_word_count(text: str) -> int:
    """Return word count of text."""
    return len(text.split())