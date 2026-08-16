# 🤖 ResumeJobMatchAI

### AI-Powered Resume ↔ Job Matching & Candidate Ranking System

ResumeJobMatchAI is an AI-powered application that analyzes resumes against job descriptions, detects relevant skills, identifies skill gaps, calculates job-match scores, ranks candidates, and generates personalized recommendations.

The application is built with **Python, Streamlit, LangChain, Gemini, ChromaDB, FAISS, and Sentence Transformers** and is designed to demonstrate a practical AI/ML recruitment use case.

## 🚀 Live Demo

👉 **[Try ResumeJobMatchAI](https://resumejobmatchai-4lgfsqpxxac9opcky78ppm.streamlit.app/)**

## 💻 GitHub Repository

👉 **[View Source Code](https://github.com/Sheminsharafudheen/ResumeJobMatchAI)**

---

## 🎯 Problem Statement

Recruiters may need to review many resumes for a single job opening.

Manually comparing every resume with a job description can be:

* Time-consuming
* Repetitive
* Difficult to scale
* Inconsistent when comparing candidates

ResumeJobMatchAI helps automate this process by comparing candidate skills with the skills required by a job description and producing an understandable matching report.

---

## ✨ Key Features

### 📄 Resume Analysis

* Upload resume PDF files
* Extract resume text
* Detect technical skills
* Identify relevant candidate skills

### 💼 Job Description Analysis

* Upload a job description
* Extract required skills
* Extract preferred skills
* Use an LLM to structure job requirements

### 🎯 Skill Matching

The system compares:

* Required skills
* Preferred skills
* Candidate skills

It identifies both matched and missing skills.

### 📊 Match Score

The application calculates:

* Overall match score
* Required skill coverage
* Preferred skill coverage

Required skills receive higher importance in the final score.

### 🏆 Candidate Ranking

Multiple resumes can be analyzed against the same job description and candidates can be ranked based on their calculated match scores.

### 🤖 AI Recommendations

The application generates recommendations covering:

1. Priority skills to learn
2. Resume improvement suggestions
3. Project suggestions
4. Interview preparation

Recommendations focus mainly on missing required skills.

---

## 🔄 Application Workflow

```text
                 ┌──────────────────┐
                 │   Resume PDF(s)  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Resume Text      │
                 │ Extraction       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Skill Detection  │
                 └────────┬─────────┘
                          │
                          │
                          ▼
┌──────────────────────────────────────────────┐
│              Job Description                 │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Gemini / LLM     │
              │ Skill Extraction │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Required Skills  │
              │ Preferred Skills │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Skill Matching   │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Match Score      │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Candidate        │
              │ Ranking          │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ AI Recommendations│
              └──────────────────┘
```

---

## 🧠 Matching Logic

The application calculates separate coverage scores for required and preferred skills.

### Required Skill Score

```text
Required Score =
Matched Required Skills / Total Required Skills × 100
```

### Preferred Skill Score

```text
Preferred Score =
Matched Preferred Skills / Total Preferred Skills × 100
```

### Final Match Score

The current implementation gives greater importance to required skills:

```text
Final Score =
Required Score × 0.70
+
Preferred Score × 0.20
```

This makes the system prioritize the skills that are more important for the job.

---

## 🛠️ Technology Stack

| Technology            | Purpose                                             |
| --------------------- | --------------------------------------------------- |
| Python                | Core application development                        |
| Streamlit             | Web application interface                           |
| LangChain             | LLM application framework                           |
| Gemini                | AI-powered job skill extraction and recommendations |
| ChromaDB              | Vector database                                     |
| FAISS                 | Similarity search                                   |
| Sentence Transformers | Text embeddings                                     |
| PyPDF                 | PDF text extraction                                 |
| Plotly                | Data visualization                                  |
| Pandas                | Data processing                                     |
| NumPy                 | Numerical operations                                |
| Git & GitHub          | Version control and project hosting                 |

---

## 📁 Project Structure

```text
ResumeJobMatchAI/
│
├── app.py
├── analyzer.py
├── document_loader.py
├── job_loader.py
├── job_matcher.py
├── llm.py
├── match_score.py
├── rag_chain.py
├── recommendations.py
├── resume_skill_detector.py
├── resume_skill_extractor.py
├── retriever.py
├── skill_database.py
├── skill_extractor.py
├── skill_matcher.py
├── text_splitter.py
├── vector_store.py
│
├── src/
│   ├── analyzer.py
│   ├── job_matcher.py
│   ├── llm.py
│   ├── match_score.py
│   ├── rag_chain.py
│   ├── skill_database.py
│   └── skill_matcher.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sheminsharafudheen/ResumeJobMatchAI.git
```

### 2. Move into the project directory

```bash
cd ResumeJobMatchAI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Gemini API Configuration

The application uses a Gemini API key for AI-powered analysis.

Create an API key through Google AI Studio and configure it as an environment variable.

### Windows

```bash
set GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

For Streamlit deployment, use **Streamlit Secrets** instead of putting the API key directly into your source code.

Example:

```toml
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
```

> ⚠️ Never commit your real API key to GitHub.

---

## ▶️ Run the Application Locally

Start Streamlit with:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📊 Example Workflow

### Step 1 — Upload Resume

Upload one or more candidate resumes in PDF format.

### Step 2 — Add Job Description

Upload or provide the target job description.

### Step 3 — Analyze

The system:

```text
Resume
   ↓
Text Extraction
   ↓
Skill Detection
   ↓
Job Description
   ↓
AI Skill Extraction
   ↓
Skill Matching
   ↓
Match Score
   ↓
Candidate Ranking
   ↓
AI Recommendations
```

### Step 4 — Review Results

The recruiter can review:

* Candidate match score
* Required skills matched
* Required skills missing
* Preferred skills matched
* Preferred skills missing
* AI recommendations
* Candidate ranking

---

## 🔐 Privacy & Security

Resume files may contain sensitive personal information.

When using this application:

* Do not upload resumes containing information you do not have permission to process.
* Never expose API keys in source code.
* Keep API credentials in environment variables or Streamlit Secrets.
* Avoid committing uploaded resumes or personal candidate data to GitHub.
* Use temporary files for uploaded documents where possible.
* For production use, add stronger data-retention and deletion controls.

---

## 🚧 Future Improvements

Potential future improvements include:

* 🔹 Advanced semantic resume-job similarity
* 🔹 Better skill normalization
* 🔹 Experience-level matching
* 🔹 Education matching
* 🔹 Job-title similarity
* 🔹 Recruiter dashboard
* 🔹 Candidate comparison charts
* 🔹 Explainable ranking
* 🔹 Automated resume feedback
* 🔹 Improved privacy and automatic file deletion
* 🔹 Authentication and role-based access
* 🔹 Database-backed candidate management

---

## 💡 Why I Built This Project

I built ResumeJobMatchAI to apply my knowledge of **Python, AI/ML, NLP, LLM applications, LangChain, embeddings, vector databases, and Streamlit** to a practical recruitment problem.

The project helped me understand how an AI application can combine traditional skill matching with LLM-based analysis to produce useful, explainable results.

---

## 🎓 Skills Demonstrated

This project demonstrates practical experience with:

```text
Python
│
├── PDF Processing
├── Data Processing
├── NLP
├── Skill Extraction
├── Skill Matching
│
AI / GenAI
│
├── LLM Integration
├── Prompt Engineering
├── Gemini
├── LangChain
├── Embeddings
├── Vector Databases
│
Application Development
│
├── Streamlit
├── Git
├── GitHub
└── Deployment
```

---

## 👨‍💻 Author

**Shemin T.S**

BCA – Artificial Intelligence & Machine Learning

### Project Links

🚀 **Live Demo:**
https://resumejobmatchai-4lgfsqpxxac9opcky78ppm.streamlit.app/

💻 **GitHub:**
https://github.com/Sheminsharafudheen/ResumeJobMatchAI

---

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub.

---

### ResumeJobMatchAI

**Know your match. Close your skill gaps. Get hired. 🚀**
