# 🍽️ AI Restaurent-dish-suggestor
> A Smart Meal Combo Suggester built as project for the **5-Day AI Value Added Course**  
> organized by the **Department of ECO FROM MIT ADT UNIVERSITY**

🌐 **Live Demo:** (https://menusuggeter.streamlit.app)
---

## 👥 Team Members
1. Sohail Bagwan 
2. Vivek Adile 
3. Yash Gujare

---

## 📌 About the Project
This project was developed on **Day 5** of the AI Value Added Course as the final hands-on project. It is an AI-powered restaurant ordering system that suggests personalized meal combos based on the user's food preference, spice level, and budget — and generates a downloadable PDF invoice on order placement.

---

## ✨ Features

- 🥗 Supports **Veg & Non-Veg** menus
- 🌶️ Filter by **Spice Level** (Low / Medium / High)
- 💰 Smart combo suggestions within your **Budget**
- 🧾 Auto-generated **PDF Invoice** with order details
- 🎈 Interactive UI built with **Streamlit**
- 🤖 AI-powered retrieval using **FAISS + Sentence Transformers**
- 💬 LLM meal suggestions via **Ollama (LLaMA 3)**

---

## 🛠️ Tech Stack
| Technology | Purpose 
| Python     | Core language 
| Streamlit  | Web UI 
| Pandas     | Data handling 
| FAISS      | Vector similarity search 
| Transformer| Text embeddings 
| Ollama     | AI meal suggestions 
| fpdf       | PDF invoice generation 

---

## 📁 Project Structure

```
├── app.py                  # Streamlit web application
├── implementation.py       # CLI-based implementation with RAG pipeline
├── veg_menu.csv            # Vegetarian menu data
├── nonveg_menu.csv         # Non-vegetarian menu data
├── extras_menu.csv         # Rotis, Rice, and extras data
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

---

## 🚀 How to Run Locally
**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the Streamlit app**
```bash
streamlit run app.py

## 📦 Requirements

streamlit
pandas
numpy
faiss-cpu
sentence-transformers
fpdf
ollama

---
This project was created for educational purposes as part of an academic course.
