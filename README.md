# 🧴 Cosmetic Answer Engine

An AI-powered, local, private answer engine for querying cosmetic formulations and ingredients — powered by **LangChain**, **Ollama (LLaMA3)**, **ChromaDB**, and **Streamlit**.

<div align="center">
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?style=flat&logo=fastapi" />
  <img src="https://img.shields.io/badge/Frontend-Streamlit-fc4c02?style=flat&logo=streamlit" />
  <img src="https://img.shields.io/badge/LLM-Ollama%20LLaMA3-blueviolet" />
  <img src="https://img.shields.io/badge/VectorDB-Chroma-ffaa00" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</div>

---

## 🚀 Features

- 🧠 Ask natural-language questions about cosmetic formulations or ingredients
- 🔍 Retrieves answers with real product context
- 📚 Cites sources with `product_name` and file reference
- 🌊 Streams answers in real time like ChatGPT/Perplexity
- 🧾 Simple UI built with Streamlit
- 🛡️ Fully local and private (no external API calls)

---

## 📸 Demo

![streamlit-ui](https://github.com/samiesaheb/cosmetic-answer-engine/assets/preview-screenshot-placeholder.png)

---

## 📂 Project Structure

cosmetic-answer-engine/
├── app.py # FastAPI backend
├── answer.py # LangChain pipeline
├── streamlit_app.py # Streamlit frontend
├── ingest.py # Document loader / vectorizer
├── csv_to_txt.py # Converts your .csv into ingestible text
├── formulations_cleaned.csv
├── documents/
│ └── formulations.txt # Cleaned text file with product data
├── vectorstore/ # Chroma vector index
├── requirements.txt
└── README.md


---

## ⚙️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/samiesaheb/cosmetic-answer-engine.git
cd cosmetic-answer-engine

pip install -r requirements.txt

ollama run llama3

python csv_to_txt.py

python ingest.py

uvicorn app:app --reload

streamlit run streamlit_app.py```

💬 Example Question
What is panthenol used for?

Returns a streamed answer with citations like:

Panthenol is used as a moisturizer, humectant, and soothing agent... [[1]] [[2]]

Sources:
[[1]] (Sephora) Cosmo Lip Scrub - Cherry (formulations.txt)
[[2]] Baby Head to Toe 200 ml (formulations.txt)

📦 Dependencies

fastapi
uvicorn
streamlit
requests
langchain>=0.2
langchain-community
chromadb
sentence-transformers

Samie Saheb
Director at Sky High International Co., Ltd.
