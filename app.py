import streamlit as st
import sys
import os
import tempfile
import time
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# ---------------------------------------------------------
# FIND SRC FOLDER
# ---------------------------------------------------------

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
sys.path.insert(0, SRC_PATH)

from analyzer import analyze


# ---------------------------------------------------------
# TEXT -> PDF HELPER
# ---------------------------------------------------------
# Many job descriptions are copy-pasted as plain text (LinkedIn,
# Naukri, email, etc.) rather than uploaded as a PDF. analyze()
# expects a PDF path, so pasted text is rendered into a simple
# temporary PDF here — analyzer.py itself needs no changes.

def text_to_temp_pdf(text: str) -> str:
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp.close()

    c = canvas.Canvas(temp.name, pagesize=letter)
    width, height = letter
    margin = 50
    line_height = 14
    font_size = 11

    c.setFont("Helvetica", font_size)
    y = height - margin

    for paragraph in text.split("\n"):
        wrapped_lines = simpleSplit(paragraph, "Helvetica", font_size, width - 2 * margin) or [""]
        for line in wrapped_lines:
            if y < margin:
                c.showPage()
                c.setFont("Helvetica", font_size)
                y = height - margin
            c.drawString(margin, y, line)
            y -= line_height

    c.save()
    return temp.name


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="ResumeJobMatchAI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
# NOTE: every HTML block below is written on a single line with no
# leading indentation. Streamlit's markdown renderer treats any
# 4-space-indented (or multi-line, blank-line-separated) HTML as a
# literal code block, which is why the header/footer were showing
# up as raw text in a white box. Single-line strings avoid that.

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.18), transparent 32%),
        radial-gradient(circle at 90% 15%, rgba(168,85,247,0.14), transparent 32%),
        radial-gradient(circle at 50% 100%, rgba(59,130,246,0.10), transparent 40%),
        #05070d;
    color: #f8fafc;
}

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.block-container { max-width: 1200px; padding-top: 2.5rem; padding-bottom: 3rem; }

/* ---------- HERO ---------- */

.badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.35);
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.hero { text-align: center; padding: 20px 20px 40px 20px; }

.logo {
    font-size: 48px;
    font-weight: 900;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #f8fafc 30%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo span { background: linear-gradient(135deg, #a78bfa, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.tagline { color: #94a3b8; font-size: 17px; margin-top: 14px; font-weight: 500; }

/* ---------- UPLOAD CARDS ---------- */

/* Streamlit's real bordered container is used for the upload cards
   instead of a hand-opened/closed <div>, because content placed
   between two separate st.markdown() calls does NOT nest inside
   the div — each call is its own block. st.container(border=True)
   renders as [data-testid="stVerticalBlockBorderWrapper"], which we
   restyle here so the real widgets end up visually inside the card. */

div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) {
    background: linear-gradient(160deg, rgba(30,41,59,0.55), rgba(15,23,42,0.75));
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 22px !important;
    padding: 18px 10px 10px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.30);
    transition: border-color 0.2s ease, transform 0.2s ease;
    text-align: center;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]):hover {
    border-color: rgba(139,92,246,0.35) !important;
    transform: translateY(-2px);
}

/* force every element inside the card to actually center — target
   the widest possible set of Streamlit's inner wrapper testids since
   flex-on-parent alone was not reaching the caption/title/uploader */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) [data-testid="stVerticalBlock"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) [data-testid="stElementContainer"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) [data-testid="stCaptionContainer"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) [data-testid="stMarkdownContainer"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) [data-testid="stFileUploader"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) [data-testid="stFileUploaderDropzone"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) p,
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stFileUploader"]) small {
    text-align: center !important;
    width: 100%;
}

.upload-card-icon-wrap {
    width: 96px;
    height: 96px;
    border-radius: 24px;
    background: linear-gradient(160deg, rgba(139,92,246,0.28), rgba(139,92,246,0.08));
    border: 1px solid rgba(139,92,246,0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
    margin: 6px auto 14px;
}

.upload-card-title { font-size: 18px; font-weight: 700; margin-bottom: 2px; text-align: center; width: 100%; }
[data-testid="stFileUploaderDropzoneInstructions"] { justify-content: center !important; }
[data-testid="stFileUploader"] { max-width: 340px; margin: 0 auto; }

/* ---------- FILE UPLOADER (Streamlit widget) ---------- */

[data-testid="stFileUploaderDropzone"] {
    background: rgba(8,11,20,0.65) !important;
    border: 1.5px dashed rgba(139,92,246,0.4) !important;
    border-radius: 16px !important;
    transition: all 0.2s ease;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(167,139,250,0.85) !important;
    background: rgba(30,41,59,0.7) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] span { color: #cbd5e1 !important; }

[data-testid="stFileUploaderDropzoneInstructions"] small { color: #64748b !important; }

[data-testid="stFileUploaderDropzoneInstructions"] svg { fill: #a78bfa !important; }

[data-testid="stFileUploaderDropzone"] button {
    background: rgba(139,92,246,0.15) !important;
    color: #c4b5fd !important;
    border: 1px solid rgba(139,92,246,0.45) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    border-color: #a78bfa !important;
    color: #ffffff !important;
}

[data-testid="stFileUploaderFile"] {
    background: rgba(30,41,59,0.9) !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
}

[data-testid="stFileUploaderFileName"] { color: #f8fafc !important; }
[data-testid="stFileUploaderFileErrorMessage"] { color: #f87171 !important; }

/* ---------- PASTE-TEXT AREA (job description) ---------- */

.stTextArea textarea {
    background: rgba(8,11,20,0.85) !important;
    color: #f1f5f9 !important;
    border: 1.5px solid rgba(139,92,246,0.35) !important;
    border-radius: 14px !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}

.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.8) !important;
    box-shadow: 0 0 0 1px rgba(167,139,250,0.4) !important;
}

.stTextArea textarea::placeholder { color: #64748b !important; }

/* Streamlit tabs — restyle to match the dark/purple theme */

.stTabs [data-baseweb="tab-list"] { gap: 4px; }

.stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
    font-weight: 600;
    font-size: 13px;
}

.stTabs [aria-selected="true"] {
    color: #c4b5fd !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #8b5cf6 !important;
}

.stTabs [data-baseweb="tab-border"] { background-color: rgba(148,163,184,0.15) !important; }

/* ---------- ANALYZE BUTTON ---------- */

.stButton > button {
    background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 0 !important;
    font-weight: 800 !important;
    letter-spacing: 0.03em;
    font-size: 15px !important;
    box-shadow: 0 15px 35px rgba(139,92,246,0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 20px 45px rgba(139,92,246,0.5) !important;
}

/* ---------- DASHBOARD STAT ROW ---------- */
/* replaces the old centered score-card + separate metric row with a
   single 4-up stat strip, like a sales-analytics dashboard: icon
   chip top-left, big number, label, all in matching flat panels */

.stat-card {
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 16px;
    padding: 20px 22px;
    text-align: left;
}

.stat-card.stat-primary {
    border-color: rgba(139,92,246,0.4);
    background: linear-gradient(160deg, rgba(76,29,149,0.22), rgba(15,23,42,0.9));
}

.stat-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    margin-bottom: 14px;
    background: rgba(139,92,246,0.15);
    border: 1px solid rgba(139,92,246,0.35);
}

.stat-number { font-size: 28px; font-weight: 800; color: #f8fafc; line-height: 1.1; }
.stat-primary .stat-number { font-size: 34px; background: linear-gradient(135deg, #c4b5fd, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stat-label { color: #94a3b8; font-size: 11px; margin-top: 6px; letter-spacing: 0.05em; text-transform: uppercase; }

/* ---------- SECTION TITLE ---------- */

.section-title { font-size: 24px; font-weight: 800; margin-top: 42px; margin-bottom: 20px; }

/* ---------- SKILL PILLS ---------- */

.skill { display: inline-block; padding: 9px 15px; margin: 5px; border-radius: 20px; font-size: 13px; font-weight: 600; }
.skill-match { background: rgba(34,197,94,0.12); color: #4ade80; border: 1px solid rgba(34,197,94,0.22); }
.skill-missing { background: rgba(239,68,68,0.12); color: #f87171; border: 1px solid rgba(239,68,68,0.22); }

/* ---------- AI CARD ---------- */
/* dashboard-style: flat dark surface, thin border, small icon chip in
   the header instead of a heavy purple gradient wash */

.ai-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(148,163,184,0.12);
}

.ai-card-icon, .panel-icon {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: rgba(139,92,246,0.15);
    border: 1px solid rgba(139,92,246,0.35);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}

.ai-card-header-text, .panel-header-text { font-size: 15px; font-weight: 700; }

div[data-testid="stVerticalBlockBorderWrapper"]:has(.ai-card-marker),
div[data-testid="stVerticalBlockBorderWrapper"]:has(.panel-marker) {
    background: rgba(15,23,42,0.85) !important;
    border: 1px solid rgba(148,163,184,0.14) !important;
    border-radius: 18px !important;
    padding: 22px !important;
    margin-top: 20px;
}

.ai-card-marker, .panel-marker { display: none; }

.panel-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(148,163,184,0.12);
}

.panel-icon.icon-green { background: rgba(34,197,94,0.15); border-color: rgba(34,197,94,0.35); }
.panel-icon.icon-red { background: rgba(239,68,68,0.15); border-color: rgba(239,68,68,0.35); }

/* ---------- FOOTER ---------- */

.footer-wrap { margin-top: 70px; padding-top: 30px; border-top: 1px solid rgba(148,163,184,0.12); text-align: center; }
.footer-title { color: #cbd5e1; font-size: 14px; font-weight: 600; }
.footer-stack { color: #64748b; font-size: 13px; margin-top: 6px; }
.footer-tag { color: #a78bfa; font-size: 13px; font-weight: 600; margin-top: 14px; }

/* ---------- HOME / MODE SELECTOR ---------- */

div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-card-marker) {
    background: linear-gradient(160deg, rgba(30,41,59,0.55), rgba(15,23,42,0.75));
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 22px !important;
    padding: 30px 20px 20px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.30);
    transition: border-color 0.2s ease, transform 0.2s ease;
    text-align: center;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-card-marker):hover {
    border-color: rgba(139,92,246,0.35) !important;
    transform: translateY(-2px);
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-card-marker) [data-testid="stVerticalBlock"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-card-marker) [data-testid="stElementContainer"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-card-marker) [data-testid="stCaptionContainer"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-card-marker) [data-testid="stMarkdownContainer"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
}

div[data-testid="stVerticalBlockBorderWrapper"]:has(.home-card-marker) p { text-align: center !important; width: 100%; }

.home-card-desc { color: #94a3b8; font-size: 13px; margin: 6px 0 18px; line-height: 1.5; }

.mode-pill {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 999px;
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.35);
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 4px;
}

/* ---------- CANDIDATE RANKING TABLE ---------- */

.rank-row {
    display: grid;
    grid-template-columns: 44px 1fr 140px 120px;
    align-items: center;
    gap: 14px;
    padding: 12px 6px;
    border-bottom: 1px solid rgba(148,163,184,0.08);
}

.rank-row:last-child { border-bottom: none; }

.rank-row-header {
    color: #64748b;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0 6px 10px;
    border-bottom: 1px solid rgba(148,163,184,0.14);
}

.rank-badge {
    width: 30px;
    height: 30px;
    border-radius: 9px;
    background: rgba(139,92,246,0.15);
    border: 1px solid rgba(139,92,246,0.35);
    color: #c4b5fd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
}

.rank-badge.rank-1 { background: rgba(250,204,21,0.15); border-color: rgba(250,204,21,0.4); color: #fde047; }

.candidate-name { font-size: 13px; font-weight: 700; color: #f8fafc; }

.rank-bar-track { width: 100%; height: 8px; border-radius: 999px; background: rgba(148,163,184,0.12); overflow: hidden; }
.rank-bar-fill { height: 100%; border-radius: 999px; }

.status-pill { display: inline-block; padding: 5px 11px; border-radius: 14px; font-size: 11px; font-weight: 700; white-space: nowrap; }
.status-strong { background: rgba(34,197,94,0.14); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.status-good { background: rgba(74,222,128,0.10); color: #86efac; border: 1px solid rgba(74,222,128,0.25); }
.status-moderate { background: rgba(250,204,21,0.12); color: #facc15; border: 1px solid rgba(250,204,21,0.3); }
.status-low { background: rgba(239,68,68,0.12); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown('<div class="hero"><div class="badge">✨ AI-Powered Career Intelligence</div><div class="logo">🤖 Resume<span>JobMatchAI</span></div><div class="tagline">Know your match. Close your skill gaps. Get hired.</div></div>', unsafe_allow_html=True)


def render_home_page():
    st.markdown('<div class="section-title">👋 Get Started</div>', unsafe_allow_html=True)
    hc1, hc2 = st.columns(2)

    with hc1:
        with st.container(border=True):
            st.markdown('<div class="home-card-marker"></div><div class="upload-card-icon-wrap">🏢</div><div class="upload-card-title">For a Company / Recruiter</div><div class="home-card-desc">Upload a job description and multiple candidate resumes to get an instant ranked shortlist.</div>', unsafe_allow_html=True)
            if st.button("Continue as Recruiter", key="pick_company", use_container_width=True):
                st.session_state.app_mode = "company"
                st.rerun()

    with hc2:
        with st.container(border=True):
            st.markdown('<div class="home-card-marker"></div><div class="upload-card-icon-wrap">👤</div><div class="upload-card-title">For an Employee / Job Seeker</div><div class="home-card-desc">Upload your resume and a job description to see your match score, skill gaps, and personalized tips.</div>', unsafe_allow_html=True)
            if st.button("Continue as Job Seeker", key="pick_employee", use_container_width=True):
                st.session_state.app_mode = "employee"
                st.rerun()


def render_company_page():
    if st.button("← Back to Home", key="back_from_company"):
        st.session_state.app_mode = None
        st.rerun()

    st.markdown('<div class="mode-pill">🏢 Recruiter Mode</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Job Description</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="upload-card-icon-wrap">💼</div><div class="upload-card-title">Target Role</div>', unsafe_allow_html=True)
        st.caption("Upload a PDF, or paste the job posting as text.")

        jd_tab_upload, jd_tab_paste = st.tabs(["📎 Upload PDF", "📝 Paste text"])

        with jd_tab_upload:
            company_job_file = st.file_uploader("Job Description", type=["pdf"], key="company_job", label_visibility="collapsed")

        with jd_tab_paste:
            company_job_text = st.text_area(
                "Job description text",
                key="company_job_text",
                height=140,
                placeholder="Paste the job description here — e.g. copied from LinkedIn, Naukri, or a company careers page.",
                label_visibility="collapsed",
            )

    st.markdown('<div class="section-title">👥 Candidate Resumes</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="upload-card-icon-wrap">👥</div><div class="upload-card-title">Upload Resumes</div>', unsafe_allow_html=True)
        st.caption("Upload multiple candidate resumes (PDF) to rank against the job description above.")
        candidate_files = st.file_uploader("Candidate resumes", type=["pdf"], accept_multiple_files=True, key="candidates", label_visibility="collapsed")

    st.write("")
    rank_button = st.button("🔍  RANK CANDIDATES", use_container_width=True, key="rank_button")

    if rank_button:

        company_job_text_stripped = company_job_text.strip() if company_job_text else ""

        if company_job_file is None and not company_job_text_stripped:
            st.error("Please upload a job description PDF or paste the job description text.")
            st.stop()

        if not candidate_files:
            st.error("Please upload at least one candidate resume.")
            st.stop()

        if company_job_text_stripped:
            company_job_temp_path = text_to_temp_pdf(company_job_text_stripped)
        else:
            jtemp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            jtemp.write(company_job_file.getvalue())
            jtemp.close()
            company_job_temp_path = jtemp.name

        candidates = []

        with st.spinner(f"🤖 Analyzing {len(candidate_files)} candidate(s)..."):
            for cfile in candidate_files:
                ctemp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                ctemp.write(cfile.getvalue())
                ctemp.close()

                try:
                    cresult = analyze(ctemp.name, company_job_temp_path)
                    score = cresult["final_score"]
                except Exception:
                    score = None
                finally:
                    try:
                        os.remove(ctemp.name)
                    except Exception:
                        pass

                if score is not None:
                    candidate_name = os.path.splitext(cfile.name)[0]
                    candidates.append({"name": candidate_name, "score": score})

        try:
            os.remove(company_job_temp_path)
        except Exception:
            pass

        if not candidates:
            st.error("Could not analyze any of the uploaded resumes.")
            st.stop()

        candidates.sort(key=lambda c: c["score"], reverse=True)

        def status_for(score):
            if score >= 90:
                return "Strong", "status-strong", "🟢"
            if score >= 75:
                return "Good", "status-good", "🟢"
            if score >= 50:
                return "Moderate", "status-moderate", "🟡"
            return "Low", "status-low", "🔴"

        st.success(f"Ranked {len(candidates)} candidate(s)! 🎉")

        total = len(candidates)
        top_score = candidates[0]["score"]
        avg_score = round(sum(c["score"] for c in candidates) / total, 1)
        strong_count = sum(1 for c in candidates if c["score"] >= 90)

        st.write("")
        rs1, rs2, rs3, rs4 = st.columns(4)

        with rs1:
            st.markdown(f'<div class="stat-card stat-primary"><div class="stat-icon">👥</div><div class="stat-number">{total}</div><div class="stat-label">Candidates</div></div>', unsafe_allow_html=True)

        with rs2:
            st.markdown(f'<div class="stat-card"><div class="stat-icon">🏆</div><div class="stat-number">{top_score}%</div><div class="stat-label">Top match</div></div>', unsafe_allow_html=True)

        with rs3:
            st.markdown(f'<div class="stat-card"><div class="stat-icon">📊</div><div class="stat-number">{avg_score}%</div><div class="stat-label">Average match</div></div>', unsafe_allow_html=True)

        with rs4:
            st.markdown(f'<div class="stat-card"><div class="stat-icon">🟢</div><div class="stat-number">{strong_count}</div><div class="stat-label">Strong matches</div></div>', unsafe_allow_html=True)

        # CHART: all candidates ranked by match score
        st.markdown('<div class="section-title">📊 Match Score Comparison</div>', unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="panel-marker"></div><div class="panel-header"><div class="panel-icon">📈</div><div class="panel-header-text">All candidates, ranked</div></div>', unsafe_allow_html=True)

            bar_colors = {"status-strong": "#4ade80", "status-good": "#86efac", "status-moderate": "#facc15", "status-low": "#f87171"}
            chart_candidates = candidates[::-1]  # reverse so #1 renders at the top of the horizontal chart
            names = [c["name"] for c in chart_candidates]
            scores = [c["score"] for c in chart_candidates]
            colors = [bar_colors[status_for(c["score"])[1]] for c in chart_candidates]

            candidate_bar = go.Figure(go.Bar(
                y=names, x=scores, orientation="h",
                marker_color=colors,
                text=[f"{s}%" for s in scores], textposition="outside", textfont={"color": "#f8fafc"},
            ))
            candidate_bar.update_layout(
                height=max(160, 50 * len(chart_candidates)),
                margin=dict(t=10, b=10, l=10, r=40),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#f8fafc", "size": 12},
                xaxis={"range": [0, 105], "gridcolor": "rgba(148,163,184,0.12)", "zerolinecolor": "rgba(148,163,184,0.12)"},
                yaxis={"gridcolor": "rgba(148,163,184,0.0)"},
                showlegend=False,
            )
            st.plotly_chart(candidate_bar, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-title">🏆 Candidate Ranking</div>', unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown('<div class="panel-marker"></div>', unsafe_allow_html=True)

            header_html = '<div class="rank-row rank-row-header"><div>RANK</div><div>CANDIDATE</div><div>MATCH</div><div>STATUS</div></div>'
            rows_html = ""

            bar_colors = {"status-strong": "#4ade80", "status-good": "#86efac", "status-moderate": "#facc15", "status-low": "#f87171"}

            for i, c in enumerate(candidates, start=1):
                label, css_class, dot = status_for(c["score"])
                bar_color = bar_colors[css_class]
                rank_class = "rank-badge rank-1" if i == 1 else "rank-badge"
                rows_html += (
                    f'<div class="rank-row">'
                    f'<div class="{rank_class}">#{i}</div>'
                    f'<div class="candidate-name">{c["name"]}</div>'
                    f'<div><div class="rank-bar-track"><div class="rank-bar-fill" style="width:{c["score"]}%;background:{bar_color};"></div></div></div>'
                    f'<div><span class="status-pill {css_class}">{dot} {label}</span></div>'
                    f'</div>'
                )

            st.markdown(header_html + rows_html, unsafe_allow_html=True)


def render_employee_page():
    if st.button("← Back to Home", key="back_from_employee"):
        st.session_state.app_mode = None
        st.rerun()

    st.markdown('<div class="mode-pill">👤 Job Seeker Mode</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # UPLOAD SECTION
    # ---------------------------------------------------------

    st.markdown('<div class="section-title">📄 Start Your Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown('<div class="upload-card-icon-wrap">📄</div><div class="upload-card-title">Your Resume</div>', unsafe_allow_html=True)
            st.caption("Upload your resume as a PDF.")
            resume_file = st.file_uploader("Resume", type=["pdf"], key="resume", label_visibility="collapsed")

    with col2:
        with st.container(border=True):
            st.markdown('<div class="upload-card-icon-wrap">💼</div><div class="upload-card-title">Job Description</div>', unsafe_allow_html=True)
            st.caption("Upload a PDF, or paste the job posting as text.")

            tab_upload, tab_paste = st.tabs(["📎 Upload PDF", "📝 Paste text"])

            with tab_upload:
                job_file = st.file_uploader("Job Description", type=["pdf"], key="job", label_visibility="collapsed")

            with tab_paste:
                job_text = st.text_area(
                    "Job description text",
                    key="job_text",
                    height=160,
                    placeholder="Paste the job description here — e.g. copied from LinkedIn, Naukri, or a company careers page.",
                    label_visibility="collapsed",
                )


    # ---------------------------------------------------------
    # ANALYZE BUTTON
    # ---------------------------------------------------------

    st.write("")
    analyze_button = st.button("✨  ANALYZE MY JOB MATCH", use_container_width=True)


    # ---------------------------------------------------------
    # ANALYSIS
    # ---------------------------------------------------------

    if analyze_button:

        job_text_stripped = job_text.strip() if job_text else ""

        if resume_file is None:
            st.error("Please upload your resume PDF.")
            st.stop()

        if job_file is None and not job_text_stripped:
            st.error("Please upload a job description PDF or paste the job description text.")
            st.stop()

        # Job description may be pasted text (rendered to a temp PDF)
        # or an uploaded PDF; resume is always an uploaded PDF now.
        resume_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        resume_temp.write(resume_file.getvalue())
        resume_temp.close()
        resume_temp_path = resume_temp.name

        if job_text_stripped:
            job_temp_path = text_to_temp_pdf(job_text_stripped)
        else:
            job_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            job_temp.write(job_file.getvalue())
            job_temp.close()
            job_temp_path = job_temp.name

        try:
            with st.spinner("🤖 AI is analyzing your resume..."):
                result = analyze(resume_temp_path, job_temp_path)

            st.success("Analysis completed successfully! 🎉")

            # DASHBOARD STAT ROW
            st.write("")
            s1, s2, s3, s4 = st.columns(4)

            with s1:
                st.markdown(f'<div class="stat-card stat-primary"><div class="stat-icon">🎯</div><div class="stat-number">{result["final_score"]}%</div><div class="stat-label">Overall match</div></div>', unsafe_allow_html=True)

            with s2:
                st.markdown(f'<div class="stat-card"><div class="stat-icon">✅</div><div class="stat-number">{result["required_score"]}%</div><div class="stat-label">Required skills</div></div>', unsafe_allow_html=True)

            with s3:
                st.markdown(f'<div class="stat-card"><div class="stat-icon">⭐</div><div class="stat-number">{result["preferred_score"]}%</div><div class="stat-label">Preferred skills</div></div>', unsafe_allow_html=True)

            with s4:
                missing_count = len(result["required_missing"])
                st.markdown(f'<div class="stat-card"><div class="stat-icon">⚠️</div><div class="stat-number">{missing_count}</div><div class="stat-label">Skill gaps</div></div>', unsafe_allow_html=True)

            # CHARTS: match gauge + required vs preferred bar chart
            st.markdown('<div class="section-title">📊 Skill Match Overview</div>', unsafe_allow_html=True)
            c1, c2 = st.columns([1, 1.3])

            with c1:
                with st.container(border=True):
                    st.markdown('<div class="panel-marker"></div><div class="panel-header"><div class="panel-icon">🎯</div><div class="panel-header-text">Overall match score</div></div>', unsafe_allow_html=True)

                    gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=result["final_score"],
                        number={"suffix": "%", "font": {"size": 40, "color": "#f8fafc"}},
                        gauge={
                            "axis": {"range": [0, 100], "tickcolor": "#475569", "tickfont": {"color": "#94a3b8", "size": 10}},
                            "bar": {"color": "#8b5cf6", "thickness": 0.28},
                            "bgcolor": "rgba(0,0,0,0)",
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0, 50], "color": "rgba(239,68,68,0.18)"},
                                {"range": [50, 75], "color": "rgba(250,204,21,0.15)"},
                                {"range": [75, 100], "color": "rgba(74,222,128,0.15)"},
                            ],
                        },
                    ))
                    gauge.update_layout(
                        height=220,
                        margin=dict(t=10, b=10, l=20, r=20),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={"color": "#f8fafc"},
                    )
                    st.plotly_chart(gauge, use_container_width=True, config={"displayModeBar": False})

            with c2:
                with st.container(border=True):
                    st.markdown('<div class="panel-marker"></div><div class="panel-header"><div class="panel-icon">📈</div><div class="panel-header-text">Required vs preferred coverage</div></div>', unsafe_allow_html=True)

                    categories = ["Required", "Preferred"]
                    matched_counts = [len(result["required_matched"]), len(result["preferred_matched"])]
                    missing_counts = [len(result["required_missing"]), len(result["preferred_missing"])]

                    bar = go.Figure()
                    bar.add_trace(go.Bar(
                        y=categories, x=matched_counts, name="Matched",
                        orientation="h", marker_color="#4ade80",
                        text=matched_counts, textposition="inside", textfont={"color": "#052e16"},
                    ))
                    bar.add_trace(go.Bar(
                        y=categories, x=missing_counts, name="Missing",
                        orientation="h", marker_color="#f87171",
                        text=missing_counts, textposition="inside", textfont={"color": "#450a0a"},
                    ))
                    bar.update_layout(
                        barmode="stack",
                        height=220,
                        margin=dict(t=10, b=10, l=10, r=10),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={"color": "#f8fafc", "size": 12},
                        legend={"orientation": "h", "y": -0.2, "font": {"color": "#94a3b8", "size": 11}},
                        xaxis={"gridcolor": "rgba(148,163,184,0.12)", "zerolinecolor": "rgba(148,163,184,0.12)"},
                        yaxis={"gridcolor": "rgba(148,163,184,0.0)"},
                    )
                    st.plotly_chart(bar, use_container_width=True, config={"displayModeBar": False})

            # REQUIRED SKILLS
            st.markdown('<div class="section-title">🧠 Required Skill Intelligence</div>', unsafe_allow_html=True)
            left, right = st.columns(2)

            with left:
                with st.container(border=True):
                    st.markdown('<div class="panel-marker"></div><div class="panel-header"><div class="panel-icon icon-green">✅</div><div class="panel-header-text">Matched skills</div></div>', unsafe_allow_html=True)
                    for skill in result["required_matched"]:
                        st.markdown(f'<span class="skill skill-match">✓ {skill}</span>', unsafe_allow_html=True)

            with right:
                with st.container(border=True):
                    st.markdown('<div class="panel-marker"></div><div class="panel-header"><div class="panel-icon icon-red">❌</div><div class="panel-header-text">Missing skills</div></div>', unsafe_allow_html=True)
                    for skill in result["required_missing"]:
                        st.markdown(f'<span class="skill skill-missing">✕ {skill}</span>', unsafe_allow_html=True)

            # PREFERRED SKILLS
            st.markdown('<div class="section-title">⭐ Preferred Skills</div>', unsafe_allow_html=True)
            left, right = st.columns(2)

            with left:
                with st.container(border=True):
                    st.markdown('<div class="panel-marker"></div><div class="panel-header"><div class="panel-icon icon-green">🟢</div><div class="panel-header-text">Matched</div></div>', unsafe_allow_html=True)
                    for skill in result["preferred_matched"]:
                        st.markdown(f'<span class="skill skill-match">✓ {skill}</span>', unsafe_allow_html=True)

            with right:
                with st.container(border=True):
                    st.markdown('<div class="panel-marker"></div><div class="panel-header"><div class="panel-icon icon-red">🟠</div><div class="panel-header-text">Missing</div></div>', unsafe_allow_html=True)
                    for skill in result["preferred_missing"]:
                        st.markdown(f'<span class="skill skill-missing">✕ {skill}</span>', unsafe_allow_html=True)

            # CAREER COACH
            st.markdown('<div class="section-title">🤖 AI Career Coach</div>', unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown('<div class="ai-card-marker"></div><div class="ai-card-header"><div class="ai-card-icon">🤖</div><div class="ai-card-header-text">Personalized recommendations</div></div>', unsafe_allow_html=True)
                st.markdown(result["recommendations"])

            # RESUME SKILLS
            with st.expander("📋 View All Detected Resume Skills"):
                skills = result["resume_skills"]
                cols = st.columns(4)
                for index, skill in enumerate(skills):
                    with cols[index % 4]:
                        st.write(f"✓ {skill}")

        except Exception as e:
            st.error("Something went wrong.")
            st.exception(e)

        finally:
            try:
                os.remove(resume_temp_path)
                os.remove(job_temp_path)
            except Exception:
                pass


# ---------------------------------------------------------
# MODE DISPATCH
# ---------------------------------------------------------

if "app_mode" not in st.session_state:
    st.session_state.app_mode = None

if st.session_state.app_mode is None:
    render_home_page()
elif st.session_state.app_mode == "company":
    render_company_page()
else:
    render_employee_page()


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown('<div class="footer-wrap"><div class="footer-title">ResumeJobMatchAI</div><div class="footer-stack">Built with Python • LangChain • Ollama • ChromaDB • Streamlit</div><div class="footer-tag">Know your match. Close your skill gaps. Get hired. 🚀</div></div>', unsafe_allow_html=True)