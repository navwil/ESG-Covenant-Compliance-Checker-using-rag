import re

# Centralized sensitive word mapping
SENSITIVE_TERMS = {

    # ---------------- MEDICAL ----------------
    "treatment": "recommendation",
    "therapy": "intervention",
    "diagnosis": "assessment",
    "diagnostic": "evaluation",
    "prescription": "guideline",
    "medicine": "wellness support",
    "medical": "health-related",
    "clinical": "operational",
    "patient": "individual",
    "patients": "individuals",
    "doctor": "specialist",
    "physician": "expert",
    "hospital": "facility",
    "hospitals": "facilities",
    "healthcare": "support services",

    # ---------------- HEALTH CONDITIONS ----------------
    "disease": "condition",
    "diseases": "conditions",
    "illness": "issue",
    "illnesses": "issues",
    "disorder": "condition",
    "syndrome": "condition",
    "injury": "incident",
    "injuries": "incidents",
    "disability": "accessibility consideration",
    "disabled": "accessible",
    "depression": "wellbeing concern",
    "anxiety": "wellbeing concern",
    "stress": "workload factor",
    "mental health": "employee wellbeing",
    "medical condition": "wellbeing condition",
    "health condition": "wellbeing status",

    # ---------------- GENDER / WOMEN ----------------
    "women": "employees",
    "woman": "employee",
    "female": "staff",
    "male": "staff",
    "gender": "workforce",
    "girl": "employee",
    "girls": "employees",

    # ---------------- MATERNITY ----------------
    "pregnancy": "employee welfare",
    "pregnant": "employee welfare",
    "maternal": "employee support",
    "maternity": "employee support",

    # ---------------- ESG SAFE REPLACEMENTS ----------------
    "employee health": "employee wellbeing",
    "health program": "wellbeing initiative",
    "medical support": "employee support",
    "health issue": "wellbeing issue",
    "health risk": "operational risk",

    # ---------------- ADDITIONAL SAFETY ----------------
    "prescribe": "suggest",
    "prescribed": "recommended",
    "therapy session": "support session",
    "medical treatment": "management action",
    "clinical treatment": "operational action",
}


def streamline_text(text: str) -> str:
    """
    Sanitizes sensitive content before sending to LLM
    """

    if not text:
        return ""

    cleaned = str(text)

    # Replace terms
    for old_word, new_word in SENSITIVE_TERMS.items():

        pattern = rf"\b{re.escape(old_word)}\b"

        cleaned = re.sub(
            pattern,
            new_word,
            cleaned,
            flags=re.IGNORECASE
        )

    # Remove extra spaces
    cleaned = re.sub(
        r"\s+",
        " ",
        cleaned
    )

    return cleaned.strip()


def sanitize_documents(docs):
    """
    Sanitize LangChain documents
    """

    sanitized_docs = []

    for doc in docs:

        if hasattr(doc, "page_content"):

            doc.page_content = streamline_text(
                doc.page_content
            )

        sanitized_docs.append(doc)

    return sanitized_docs