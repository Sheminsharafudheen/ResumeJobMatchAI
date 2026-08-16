import streamlit as st
import sys
import os
import tempfile

# Add src folder to Python path
SRC_PATH = os.path.join(
    os.path.dirname(__file__),
    "src"
)

sys.path.insert(0, SRC_PATH)

from analyzer import analyze


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="ResumeJobMatchAI",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🤖 ResumeJobMatchAI")

st.subheader(
    "AI-Powered Resume ↔ Job Matching Assistant"
)

st.write(
    "Upload your resume and job description "
    "to analyze your job compatibility."
)

st.divider()


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 📄 Resume")

    resume_file = st.file_uploader(
        "Upload your Resume PDF",
        type=["pdf"],
        key="resume_upload"
    )


with col2:

    st.markdown("### 💼 Job Description")

    job_file = st.file_uploader(
        "Upload Job Description PDF",
        type=["pdf"],
        key="job_upload"
    )


st.divider()


# --------------------------------------------------
# ANALYZE
# --------------------------------------------------

if st.button(
    "🚀 Analyze Resume",
    use_container_width=True
):

    if resume_file is None:

        st.error(
            "Please upload your Resume PDF."
        )

        st.stop()


    if job_file is None:

        st.error(
            "Please upload the Job Description PDF."
        )

        st.stop()


    # --------------------------------------------------
    # SAVE UPLOADED FILES
    # --------------------------------------------------

    resume_temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    resume_temp.write(
        resume_file.getvalue()
    )

    resume_temp.close()


    job_temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    job_temp.write(
        job_file.getvalue()
    )

    job_temp.close()


    # --------------------------------------------------
    # RUN ANALYSIS
    # --------------------------------------------------

    try:

        with st.spinner(
            "🤖 AI is analyzing your resume..."
        ):

            result = analyze(
                resume_temp.name,
                job_temp.name
            )


        st.success(
            "Analysis completed successfully! 🎉"
        )


        # --------------------------------------------------
        # SCORE
        # --------------------------------------------------

        st.markdown(
            "## 🎯 Resume Match Score"
        )

        score1, score2, score3 = st.columns(3)


        with score1:

            st.metric(
                "Overall Match",
                f"{result['final_score']}%"
            )


        with score2:

            st.metric(
                "Required Skills",
                f"{result['required_score']}%"
            )


        with score3:

            st.metric(
                "Preferred Skills",
                f"{result['preferred_score']}%"
            )


        st.divider()


        # --------------------------------------------------
        # REQUIRED SKILLS
        # --------------------------------------------------

        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                "### ✅ Matched Required Skills"
            )

            if result["required_matched"]:

                for skill in result[
                    "required_matched"
                ]:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "No required skills matched."
                )


        with col2:

            st.markdown(
                "### ❌ Missing Required Skills"
            )

            if result["required_missing"]:

                for skill in result[
                    "required_missing"
                ]:

                    st.error(
                        f"✗ {skill}"
                    )

            else:

                st.success(
                    "No missing required skills!"
                )


        st.divider()


        # --------------------------------------------------
        # PREFERRED SKILLS
        # --------------------------------------------------

        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                "### ⭐ Matched Preferred Skills"
            )

            if result["preferred_matched"]:

                for skill in result[
                    "preferred_matched"
                ]:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "No preferred skills matched."
                )


        with col2:

            st.markdown(
                "### ⚠️ Missing Preferred Skills"
            )

            if result["preferred_missing"]:

                for skill in result[
                    "preferred_missing"
                ]:

                    st.warning(
                        f"✗ {skill}"
                    )

            else:

                st.success(
                    "No missing preferred skills!"
                )


        st.divider()


        # --------------------------------------------------
        # AI RECOMMENDATIONS
        # --------------------------------------------------

        st.markdown(
            "## 🤖 AI Improvement Recommendations"
        )

        st.markdown(
            result["recommendations"]
        )


        st.divider()


        # --------------------------------------------------
        # RESUME SKILLS
        # --------------------------------------------------

        with st.expander(
            "📋 View Detected Resume Skills"
        ):

            skills = result[
                "resume_skills"
            ]

            for skill in skills:

                st.write(
                    f"✓ {skill}"
                )


    except Exception as e:

        st.error(
            "An error occurred during analysis."
        )

        st.exception(e)


    finally:

        # Delete temporary files
        try:

            os.remove(
                resume_temp.name
            )

            os.remove(
                job_temp.name
            )

        except Exception:
            pass


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "ResumeJobMatchAI | "
    "Python • LangChain • Ollama • ChromaDB • Streamlit"
)