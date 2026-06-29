from groq import Groq
import time
from config import GROQ_API_KEY, MODEL_NAME, CHUNK_PROMPT, MERGE_PROMPT
from utils import clean_text, split_into_chunks

client = Groq(api_key=GROQ_API_KEY)

def summarize_chunk(chunk: str, retries: int = 3) -> str:
    prompt = CHUNK_PROMPT + chunk

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e)
            if "429" in err and attempt < retries - 1:
                time.sleep(60 * (attempt + 1))
                continue
            raise RuntimeError(f"Groq API error on chunk: {err}")


def merge_summaries(partial_summaries: list[str]) -> str:
    combined = "\n\n".join(
        [f"Summary {i+1}:\n{s}" for i, s in enumerate(partial_summaries)]
    )
    prompt = MERGE_PROMPT + "\n\n" + combined

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq API error on merge: {str(e)}")


def summarize_document(raw_text: str, progress_callback=None) -> dict:
    cleaned = clean_text(raw_text)
    chunks = split_into_chunks(cleaned)
    total_chunks = len(chunks)

    partial_summaries = []
    for i, chunk in enumerate(chunks):
        summary = summarize_chunk(chunk)
        partial_summaries.append(summary)
        if progress_callback:
            progress_callback(i + 1, total_chunks)

    if len(partial_summaries) == 1:
        final_summary = partial_summaries[0]
    else:
        final_summary = merge_summaries(partial_summaries)

    return {
        "final_summary": final_summary,
        "partial_summaries": partial_summaries,
        "chunk_count": total_chunks,
        "word_count": len(cleaned.split())
    }