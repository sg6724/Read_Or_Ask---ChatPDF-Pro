import json
from pathlib import Path
from datetime import datetime

def save_chat_log(question, answer):
    log_file = Path("chat_history.json")
    history = []

    if log_file.exists():
        with open(log_file, "r") as f:
            history = json.load(f)

    history.append({
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer
    })

    with open(log_file, "w") as f:
        json.dump(history, f, indent=2)