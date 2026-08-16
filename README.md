\# 🤖 ResumeJobMatchAI



An AI-powered Resume ↔ Job Matching application that analyzes a candidate's resume against a job description and provides an intelligent match score, skill analysis, and career recommendations.



\## 🚀 Features



\* 📄 Upload and analyze resumes

\* 💼 Upload job descriptions

\* 🎯 Calculate Resume–Job Match Score

\* ✅ Identify matched skills

\* ❌ Identify missing skills

\* 📊 Analyze candidate strengths and skill gaps

\* 🤖 AI-powered career recommendations

\* 🧠 RAG-based document processing

\* 🔎 Semantic search using embeddings

\* 💾 Vector storage using ChromaDB / FAISS

\* 🏆 Candidate/job matching analysis

\* 🌐 Interactive Streamlit interface



\## 🧠 How It Works



```text

Resume PDF

&#x20;    ↓

Document Loading

&#x20;    ↓

Text Extraction

&#x20;    ↓

Text Chunking

&#x20;    ↓

Embeddings

&#x20;    ↓

Vector Database

&#x20;    ↓

Job Description

&#x20;    ↓

Semantic Retrieval

&#x20;    ↓

Skill Matching

&#x20;    ↓

Match Score + AI Recommendations

```



\## 🛠️ Technologies Used



\* Python

\* Streamlit

\* LangChain

\* Ollama

\* ChromaDB

\* FAISS

\* Sentence Transformers

\* Hugging Face

\* Pandas

\* NumPy

\* Plotly

\* PyPDF



\## 📁 Project Structure



```text

ResumeJobMatchAI/

│

├── app.py

├── app\_old.py

├── requirements.txt

├── README.md

├── .gitignore

│

└── src/

&#x20;   ├── analyzer.py

&#x20;   ├── document\_loader.py

&#x20;   ├── embeddings.py

&#x20;   ├── job\_loader.py

&#x20;   ├── job\_matcher.py

&#x20;   ├── llm.py

&#x20;   ├── match\_score.py

&#x20;   ├── rag\_chain.py

&#x20;   ├── recommendations.py

&#x20;   ├── resume\_skill\_detector.py

&#x20;   ├── resume\_skill\_extractor.py

&#x20;   ├── retriever.py

&#x20;   ├── skill\_database.py

&#x20;   ├── skill\_extractor.py

&#x20;   ├── skill\_matcher.py

&#x20;   ├── text\_splitter.py

&#x20;   └── vector\_store.py

```



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Sheminsharafudheen/ResumeJobMatchAI.git

cd ResumeJobMatchAI

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



Activate it on Windows:



```bash

venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\## 🤖 Ollama Setup



This project uses Ollama for local LLM inference.



Install Ollama and make sure it is running on your computer.



Then pull the model required by your application. For example:



```bash

ollama pull llama3

```



The exact model should match the model configured in `src/llm.py`.



\## ▶️ Run the Application



From the project directory:



```bash

streamlit run app.py

```



The application will open in your browser.



\## 🎯 Use Case



\### 👤 Job Seekers



\* Understand how well their resume matches a job

\* Find missing skills

\* Identify skill gaps

\* Get AI-powered recommendations

\* Improve their resume according to job requirements



\### 🏢 Recruiters



\* Compare candidates with job requirements

\* Identify relevant skills

\* Analyze candidate-job compatibility

\* Rank candidates based on matching criteria



\## 🔮 Future Improvements



\* Resume improvement suggestions

\* Multiple resume comparison

\* Multiple candidate ranking

\* ATS compatibility analysis

\* Cloud deployment

\* Authentication

\* Job recommendation system

\* Advanced LLM evaluation

\* Support for multiple LLM providers



\## 👨‍💻 Author



\*\*Shemin T.S\*\*



BCA – Artificial Intelligence \& Machine Learning



GitHub: https://github.com/Sheminsharafudheen



