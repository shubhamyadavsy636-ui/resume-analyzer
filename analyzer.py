import re

def normalize_text(text):
    """
    Convert text to lowercase and
    remove unnecessary spaces.
    """

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def keyword_exists(text, keyword):
    """
    Check whether a keyword exists
    in the resume text.
    """

    keyword = keyword.lower()

    # For multi-word keywords
    if " " in keyword:
        return keyword in text

    # For single-word keywords
    pattern = r"\b" + re.escape(keyword) + r"\b"

    return re.search(
        pattern,
        text
    ) is not None


def analyze_resume(text, required_keywords):


    # Normalize resume text

    normalized_text = normalize_text(text)

    # Find matched and missing keywords

    matched = []
    missing = []

    for keyword in required_keywords:

        if keyword_exists(
            normalized_text,
            keyword
        ):
            matched.append(keyword)

        else:
            missing.append(keyword)

    # Keyword Score

    total_keywords = len(
        required_keywords
    )

    matched_count = len(
        matched
    )

    if total_keywords > 0:

        keyword_score = (
            matched_count / total_keywords
        ) * 70

    else:

        keyword_score = 0


    # Resume Word Count

    words = re.findall(
        r"\b\w+\b",
        text
    )

    word_count = len(words)


    # Check Resume Sections

    section_patterns = {

        "experience": [
            "experience",
            "work experience",
            "employment"
        ],

        "education": [
            "education",
            "academic"
        ],

        "projects": [
            "projects",
            "project experience"
        ],

        "skills": [
            "skills",
            "technical skills",
            "technologies"
        ],

        "contact": [
            "linkedin",
            "github",
            "@",
            "phone",
            "email",
            "X"
        ]
    }


    quality_score = 0


    # Each section = 5 points
    for section, patterns in section_patterns.items():

        for pattern in patterns:

            if pattern in normalized_text:

                quality_score += 5

                break

    # Final Score

    score = round(
        keyword_score + quality_score
    )

    score = min(
        score,
        100
    )

    # Recommendations


    recommendations = []


    # Missing skills
    if missing:

        recommendations.append(
            "Consider adding relevant missing skills "
            "if you genuinely have experience with them: "
            + ", ".join(missing[:6])
            + "."
        )


    # Resume length
    if word_count < 250:

        recommendations.append(
            "Your resume is quite short. "
            "Consider adding relevant project, "
            "internship, or experience details."
        )

    elif word_count > 900:

        recommendations.append(
            "Your resume is quite long. "
            "Consider removing repetitive or "
            "less relevant information."
        )


    # Projects
    if "projects" not in normalized_text:

        recommendations.append(
            "Add a Projects section with "
            "technologies used and measurable outcomes."
        )


    # Experience
    if "experience" not in normalized_text:

        recommendations.append(
            "Add relevant internship, work, "
            "freelance, or practical experience if available."
        )


    # Skills
    if "skills" not in normalized_text:

        recommendations.append(
            "Add a clear Technical Skills section."
        )


    # Certifications
    if (
        "certification" not in normalized_text
        and
        "certificate" not in normalized_text
    ):

        recommendations.append(
            "Consider adding relevant certifications "
            "or achievements."
        )


    # If everything looks good
    if not recommendations:

        recommendations.append(
            "Your resume has good basic structure "
            "and keyword alignment. Focus on "
            "measurable achievements and concise "
            "bullet points."
        )

    return {

        "score": score,

        "matched": matched,

        "missing": missing,

        "matched_count": matched_count,

        "total_keywords": total_keywords,

        "word_count": word_count,

        "recommendations": recommendations,

        "text_preview": text[:10000]
    }