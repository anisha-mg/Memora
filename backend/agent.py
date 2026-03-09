from tools import search_email, search_pdf, search_notes


def handle_query(question):

    question_lower = question.lower()

    if "logistics" in question_lower or "email" in question_lower:
        result = search_email(question)

    elif "document" in question_lower or "pdf" in question_lower:
        result = search_pdf(question)

    else:
        result = search_notes(question)

    if result:
        return result

    return {
        "answer": "No relevant information found.",
        "source": "Unknown"
    }