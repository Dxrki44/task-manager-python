import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def format_task(task, index):
    status = "✅" if task["done"] else "⬜"
    created = task.get("created_at", "N/A")
    return f"{index}. {status} {task['title']}  (créée: {created})"

def list_tasks(tasks):
    if not tasks:
        print("\nAucune tâche pour l’instant.\n")
        return

    print("\n--- Tes tâches ---")
    for i, task in enumerate(tasks, start=1):
        print(format_task(task, i))
    print()

def add_task(tasks):
    title = input("Titre de la tâche: ").strip()
    if not title:
        print("❌ Le titre ne peut pas être vide.")
        return

    new_task = {
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("✅ Tâche ajoutée !")

def ask_index(tasks, action_name):
    if not tasks:
        print("❌ Il n’y a aucune tâche.")
        return None

    raw = input(f"Numéro de la tâche à {action_name}: ").strip()
    if not raw.isdigit():
        print("❌ Entre un nombre valide.")
        return None

    idx = int(raw)
    if idx < 1 or idx > len(tasks):
        print("❌ Numéro hors limite.")
        return None

    return idx - 1  # index Python

def mark_done(tasks):
    idx = ask_index(tasks, "marquer comme terminée")
    if idx is None:
        return

    tasks[idx]["done"] = True
    save_tasks(tasks)
    print("✅ Tâche marquée comme terminée !")

def delete_task(tasks):
    idx = ask_index(tasks, "supprimer")
    if idx is None:
        return

    removed = tasks.pop(idx)
    save_tasks(tasks)
    print(f"🗑️ Tâche supprimée : {removed['title']}")

def menu():
    print("===== Task Manager =====")
    print("1) Afficher les tâches")
    print("2) Ajouter une tâche")
    print("3) Marquer une tâche terminée")
    print("4) Supprimer une tâche")
    print("5) Quitter")

def main():
    tasks = load_tasks()

    while True:
        menu()
        choice = input("Choix: ").strip()

        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Bye 👋")
            break
        else:
            print("❌ Choix invalide. Essaie encore.")

if __name__ == "__main__":
    main()
    