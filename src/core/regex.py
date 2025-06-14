import re


HEADERS = [
    "experience", "work experience", "professional experience", "relevant experience",
    "education", "education and training",
    "skills", "technical skills", "skill highlights",
    "summary", "professional summary", "summary of skills", "technical summary",
    "highlights", "accomplishments",
    "certifications", "certifications and credentials",
    "languages", "language skills",
    "profile", "professional profile", "activities and honors"
]

def extract_all_cv_details(text: str) -> dict:
    sections = extract_sections(text)
    details = reformat_sections(sections)
    return details

def clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)  
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\r", "", text)
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

def extract_sections(text: str, target_sections=None):
    if target_sections is None:
        target_sections = ["summary", "skills", "education", "experience"]

    headers_pattern = "|".join([re.escape(h) for h in HEADERS])
    pattern = rf"(?im)^\s*({headers_pattern})\s*$"

    matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
    sections = {}

    for i, match in enumerate(matches):
        header = match.group(1).lower()
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        # Normalisasi header ke target section
        for section in target_sections:
            if section in header:
                section_key = section
                break
        else:
            continue
        section_text = text[start:end].strip()
        sections[section_key] = clean_text(section_text)

    for section in target_sections:
        if section not in sections:
            sections[section] = ""

    return sections


def reformat(text: str) -> str:
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = text.replace('\n', ' ')
    text = re.sub(r',+', ',', text)
    return text.strip(' ,')


def reformat_sections(sections: dict) -> dict:
    return {
        "summary": reformat(sections.get("summary", "")),
        "skills": reformat(sections.get("skills", "")),
        "education": reformat(sections.get("education", "")),
        "experience": reformat(sections.get("experience", "")),
    }

def validate_email(text: str):
    email_match = re.search(r"\b[a-z0-9]+(?:[_\-\.][a-z0-9]+)@[a-z0-9]+(?:-[a-z0-9]+)\.[a-z]{2,}\b", text)
    return email_match.group(0) if email_match else None