import streamlit as st
from parser import extract_text
from analyzer import analyze_resume


st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide"
)


st.title("Resume Analyzer")

st.write(
    "Upload your resume, select a target domain, "
    "and get an ATS-style score with improvement suggestions."
)


DOMAIN_REQUIREMENTS = {

    "Data Science": [
        "python",
        "machine learning",
        "statistics",
        "pandas",
        "numpy",
        "scikit-learn",
        "sql",
        "data visualization",
        "matplotlib",
        "seaborn"
    ],

    "Machine Learning": [
        "python",
        "machine learning",
        "scikit-learn",
        "pandas",
        "numpy",
        "statistics",
        "feature engineering",
        "model",
        "tensorflow",
        "pytorch"
    ],

    "Generative AI / RAG": [
        "python",
        "llm",
        "generative ai",
        "rag",
        "retrieval augmented generation",
        "embeddings",
        "vector database",
        "transformers",
        "langchain",
        "prompt"
    ],

    "Software Engineering": [
        "python",
        "java",
        "c++",
        "data structures",
        "algorithms",
        "sql",
        "git",
        "api",
        "rest",
        "docker",
        "testing"
    ],

    "Data Analyst": [
        "sql",
        "excel",
        "python",
        "pandas",
        "power bi",
        "tableau",
        "statistics",
        "data visualization",
        "dashboard"
    ],
    
    "Full Stack Development": [
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
        "node.js",
        "express",
        "frontend",
        "backend",
        "rest api",
        "sql",
        "mongodb",
        "git",
        "docker"
    ],

    "Cloud Computing": [
        "cloud computing",
        "aws",
        "azure",
        "google cloud",
        "gcp",
        "ec2",
        "s3",
        "lambda",
        "docker",
        "kubernetes",
        "linux",
        "terraform",
        "ci/cd",
        "devops"
    ]
}


uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx", "pptx", "txt"],
    help="Supported formats: PDF, DOCX, PPTX, and TXT"
)


domain = st.selectbox(
    "Select your target domain",
    list(DOMAIN_REQUIREMENTS.keys())
)


if uploaded_file and st.button(
    "Analyze Resume",
    type="primary"
):

    try:

        # Extract text from resume
        text = extract_text(uploaded_file)


        # Check extracted text
        if not text.strip():

            st.error(
                "No readable text was found in the uploaded file."
            )

            st.stop()


        # Analyze resume
        result = analyze_resume(
            text,
            DOMAIN_REQUIREMENTS[domain]
        )


        st.subheader("ATS-style Analysis")

        # Metrics

        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Overall Score",
            f"{result['score']}/100"
        )


        col2.metric(
            "Matched Skills",
            f"{result['matched_count']}/{result['total_keywords']}"
        )


        col3.metric(
            "Resume Length",
            f"{result['word_count']} words"
        )


        # Score Progress

        st.progress(
            result["score"] / 100
        )


        # Score Message

        if result["score"] >= 80:

            st.success(
                "Strong keyword alignment for this domain."
            )

        elif result["score"] >= 60:

            st.warning(
                "Moderate alignment. Some important skills are missing."
            )

        else:

            st.error(
                "Low alignment. Several domain-specific keywords are missing."
            )



        # Matched / Missing Keywords

        col1, col2 = st.columns(2)


        with col1:

            st.subheader("Matched Keywords")

            if result["matched"]:

                st.write(
                    ", ".join(result["matched"])
                )

            else:

                st.write(
                    "No target keywords detected."
                )


        with col2:

            st.subheader("Missing Keywords")

            if result["missing"]:

                st.write(
                    ", ".join(result["missing"])
                )

            else:

                st.write(
                    "No major keyword gaps detected."
                )


        # Recommendations

        st.subheader("Recommendations")


        for recommendation in result["recommendations"]:

            st.write(
                f"• {recommendation}"
            )


        # Extracted Resume Text

        with st.expander(
            "View Extracted Resume Text"
        ):

            st.text(
                result["text_preview"]
            )


    except Exception as e:

        st.error(
            f"Could not analyze the file: {e}"
        )