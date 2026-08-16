# 🤖 ResumeJobMatchAI

### AI-Powered Resume ↔ Job Matching & Candidate Ranking System

ResumeJobMatchAI is an AI-powered application that analyzes resumes against job descriptions and provides an intelligent **job-match score, skill-gap analysis, personalized recommendations, and candidate ranking**.

The application supports two modes:

* 👤 **Job Seeker Mode** — Analyze how well your resume matches a specific job.
* 🏢 **Recruiter Mode** — Compare and rank multiple candidates against a job description.

---

## ✨ Features

### 👤 Job Seeker Mode

* Upload your resume as a PDF
* Upload a job description PDF
* Paste a job description directly from LinkedIn, Naukri, or a careers page
* Calculate an overall job-match score
* Analyze required skills
* Analyze preferred skills
* Identify matched skills
* Identify missing skills
* Display visual match charts
* Generate AI-powered career recommendations
* View detected resume skills

### 🏢 Recruiter Mode

* Upload a job description
* Paste a job description as text
* Upload multiple candidate resumes
* Analyze candidates against the target role
* Calculate candidate match scores
* Rank candidates automatically
* Display candidate comparison charts
* Identify strong, good, moderate, and low matches

---

## 🧠 How It Works

```text
                 Resume PDF
                     │
                     ▼
              PDF Text Extraction
                     │
                     ▼
               Text Processing
                     │
                     ▼
                Skill Analysis
                     │
                     ▼
Job Description ──► Matching Engine
                     │
                     ▼
              Match Score
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
    Skill Gap Analysis     AI Recommendations
          │                     │
          └──────────┬──────────┘
                     ▼
              Streamlit Dashboard
```

For recruiter mode:

```text
Job Description
      │
      ▼
Multiple Candidate Resumes
      │
      ▼
Resume ↔ Job Matching
      │
      ▼
Candidate Scores
      │
      ▼
Automatic Ranking
      │
      ▼
Recruiter Dashboard
```

---

## 🛠️ Technologies Used

| Technology     | Purpose                               |
| -------------- | ------------------------------------- |
| Python         | Core programming language             |
| Streamlit      | Web application interface             |
| LangChain      | LLM application framework             |
| Ollama         | Local LLM execution                   |
| ChromaDB       | Vector database                       |
| PyTorch        | Machine learning / AI dependencies    |
| ReportLab      | PDF generation                        |
| Plotly         | Interactive charts                    |
| PDF Processing | Resume and job-description extraction |
| Git & GitHub   | Version control                       |

---

## 📊 Dashboard

The application provides a modern dashboard containing:

* Overall Match Score
* Required Skill Score
* Preferred Skill Score
* Skill Gap Count
* Match Score Charts
* Matched Skills
* Missing Skills
* AI Career Coach
* Candidate Ranking

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sheminsharafudheen/ResumeJobMatchAI.git
cd ResumeJobMatchAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama:

https://ollama.com/

Then pull the required model:

```bash
ollama pull llama3
```

Make sure Ollama is running before using the application.

---

## ▶️ Run the Application

Start Streamlit with:

```bash
python -m streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 📁 Project Structure

```text
ResumeJobMatchAI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── analyzer.py
│   └── ...
│
├── data/
│   └── ...
│
└── ...
```

---

## 🎯 Example Use Case

A job seeker can:

1. Upload their resume.
2. Paste an AI/ML Engineer job description.
3. Run the analysis.
4. Receive an overall match score.
5. See which required skills are already present.
6. Identify missing skills.
7. Get personalized recommendations for improving their resume and skills.

A recruiter can:

1. Upload a job description.
2. Upload multiple candidate resumes.
3. Run candidate analysis.
4. Compare candidate scores.
5. Automatically identify the strongest candidates.

---

## 🔮 Future Improvements

* [ ] Resume improvement suggestions
* [ ] ATS compatibility analysis
* [ ] Resume keyword optimization
* [ ] Downloadable PDF analysis reports
* [ ] Candidate history and analytics
* [ ] Job recommendation system
* [ ] Resume-to-multiple-job comparison
* [ ] Cloud deployment
* [ ] Authentication and user accounts
* [ ] Advanced semantic similarity scoring

---

## ⚠️ Disclaimer

ResumeJobMatchAI is an AI-assisted career tool. Match scores and recommendations should be used as guidance and should not be treated as the sole basis for hiring decisions.

---

## 👨‍💻 Author

**Shemin T.S**

BCA — Artificial Intelligence & Machine Learning

GitHub:
https://github.com/Sheminsharafudheen

---

## ⭐ If You Find This Project Useful

Give the repository a ⭐ on GitHub!

**ResumeJobMatchAI — Know your match. Close your skill gaps. Get hired. 🚀**
