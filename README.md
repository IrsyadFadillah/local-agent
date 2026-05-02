# 🧠 Local AI Agent (Ollama + Qwen)

A lightweight local AI agent built using **Ollama + Qwen models**.

This project runs **fully locally** (no API, no internet required after setup).

---

## 🚀 Features

* 🧠 Memory system
* 🔍 Simple RAG (context retrieval)
* 🔁 Self-refine loop
* ⚡ Fast local inference
* 🛠 Command system (`reset memory`)

---

## ⚙️ Requirements

Before running this project, make sure you have:

### 1. Install Ollama

Download and install:

👉 https://ollama.com

---

### 2. Download Models

Run in terminal:

```bash
ollama pull qwen3:4b-instruct
ollama pull qwen2.5-coder:3b-instruct
```

These models are used for:

* Planning (understanding intent)
* Coding / answering

---

### 3. Install Python Dependencies

```bash
pip install langchain-ollama
```

---

## ▶️ How to Run

```bash
python main.py
```

---

## 💬 Example Usage

```text
>> deskripsikan project ini
>> jadi ini portfolio ya?
>> reset memory
```

---

## 🧠 How It Works

1. User input
2. Memory check
3. File scanning
4. Context retrieval (RAG)
5. LLM generates answer
6. Self-refine improves answer

---

## 📁 Project Structure

```
project/
main.py
memory.json
```

---

## ⚠️ Important Notes

* This project requires **local models (Ollama)**
* First run may be slower due to model loading
* GPU recommended but not required

---

## 🚀 Future Improvements

* Vector database (FAISS / Chroma)
* Multi-agent system
* GUI (web interface)
* Code execution tools

---

## 👨‍💻 Author

Irsyad Fadillah
