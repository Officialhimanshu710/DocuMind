# 🤖 Document Reader RAG Chat Bot

A lightweight, high-speed **Retrieval-Augmented Generation (RAG)** application built to chat with multiple **PDFs** and **CSV** files simultaneously.

Unlike traditional RAG applications that rely on heavy Vector Databases (like FAISS or ChromaDB), this project uses a custom **"Smart Context"** algorithm and the **Pure Groq API** to deliver instant answers with zero dependency bloat.

## 🚀 Key Features

* **Multi-Format Support:** Upload and analyze multiple **PDF** and **CSV** documents at once.
* **Pure Groq Architecture:** Bypasses complex libraries (LangChain) to communicate directly with the **Llama-3-8b** model via Groq, ensuring compatibility with the newest Python versions (3.12/3.13).
* **Smart Context Search:** A custom logic that scans *every* uploaded file individually to find relevant paragraphs, ensuring no document is ignored during the analysis.
* **Robust Error Handling:** Automatically detects and skips corrupted files without crashing the application.
* **Modern UI:** Features a clean, WhatsApp-style chat interface with history tracking.

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Model:** [Groq](https://groq.com/) (Llama-3.1-8b-instant)
* **File Processing:** `pypdf`
* **Language:** Python 3.10+

## ⚙️ Installation & Setup

Follow these steps to run the app locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/Officialhimanshu710/rag_chat_bot.git](https://github.com/Officialhimanshu710/rag_chat_bot.git)
cd rag_chat_bot

```
2. Create a Virtual Environment
```
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```
3. Install Dependencies
```
pip install -r requirements.txt

```
4. Configure API Key
Create a file named ```.env``` in the root folder.

Add your Groq API key:
```
GROQ_API_KEY=gsk_your_actual_key_here

```
5. Run the App
```
streamlit run app.py

```
☁️ Deployment
 This app is optimized for Streamlit Cloud:

1. Push your code to GitHub.

2. Go to share.streamlit.io.

3. Deploy the repository ```Officialhimanshu710/rag_chat_bot```.

4. Add ```GROQ_API_KEY``` in the "Advanced Settings" -> "Secrets" section.
---
Developed by Himanshu Dulhe
