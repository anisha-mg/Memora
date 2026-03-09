import pandas as pd
from pypdf import PdfReader


def search_email(query):

    df = pd.read_csv("backend/data/emails.csv")

    for row in df["content"]:
        if query.lower() in row.lower():
            return {
                "answer": row,
                "source": "Email Dataset"
            }

    return None


def search_pdf(query):

    reader = PdfReader("backend/data/logistics.pdf")

    for page in reader.pages:
        text = page.extract_text()

        if text and query.lower() in text.lower():
            return {
                "answer": text[:200],
                "source": "PDF Document"
            }

    return None


def search_notes(query):

    with open("backend/data/notes.txt") as f:
        text = f.read()

    if query.lower() in text.lower():
        return {
            "answer": text[:200],
            "source": "Meeting Notes"
        }

    return None