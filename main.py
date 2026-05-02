import os
import json
from langchain_ollama import ChatOllama

MEMORY_FILE = "memory.json"
chat_history = []

# =========================
# MEMORY
# =========================
def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return None
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

# =========================
# FILE TOOLS
# =========================
def scan_folder(folder):
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith((".py", ".js", ".html", ".json")):
                files.append(os.path.join(root, f))
    return files

def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

# =========================
# SIMPLE RAG
# =========================
def retrieve_context(files, prompt):
    result = []
    for f in files:
        if any(word in f.lower() for word in prompt.lower().split()):
            result.append(f)
    return result[:3] if result else files[:2]

# =========================
# SELF REFINE
# =========================
def self_refine(llm, prompt, answer):
    critique = llm.invoke(f"""
User: {prompt}
Answer: {answer}

Is this answer clear and correct? Improve if needed.
""").content

    refined = llm.invoke(f"""
Original: {answer}
Improve this answer based on critique:
{critique}

Make it concise and confident.
""").content

    return refined

# =========================
# AGENT
# =========================
def agent(prompt, folder="./project"):
    global chat_history

    cmd = prompt.lower().strip()

    # =========================
    # 🚨 HARD COMMAND LAYER
    # =========================
    if cmd == "reset memory":
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        chat_history.clear()
        return "🗑️ Memory berhasil di-reset"

    # =========================
    # MODELS
    # =========================
    planner = ChatOllama(model="qwen3:4b-instruct")
    llm = ChatOllama(model="qwen2.5-coder:3b-instruct")

    history_text = "\n".join(chat_history[-6:])

    # =========================
    # MEMORY
    # =========================
    memory = load_memory()

    if memory:
        files = memory["files"]
        summary = memory["summary"]
    else:
        files = scan_folder(folder)

        summary = planner.invoke(f"""
Explain briefly what this project is:
{files}
""").content

        save_memory({
            "files": files,
            "summary": summary
        })

    # =========================
    # RAG
    # =========================
    selected_files = retrieve_context(files, prompt)

    context = ""
    for f in selected_files:
        context += f"\nFILE: {f}\n{read_file(f)[:300]}\n"

    # =========================
    # GENERATE
    # =========================
    answer = llm.invoke(f"""
Conversation:
{history_text}

User:
{prompt}

Project:
{summary}

Context:
{context}

Rules:
- Answer clearly
- Be confident
- Use Indonesian if user uses Indonesian
""").content

    # =========================
    # SELF REFINE
    # =========================
    final_answer = self_refine(llm, prompt, answer)

    chat_history.append(f"User: {prompt}")
    chat_history.append(f"AI: {final_answer}")

    return final_answer


# =========================
# RUN
# =========================
if __name__ == "__main__":
    while True:
        user_input = input("\n>> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        print(agent(user_input))