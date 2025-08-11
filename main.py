import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создание таблицы, если её нет
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    done BOOLEAN DEFAULT 0
)
""")
conn.commit()

# Команды
def add_task(task_text):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task_text,))
    conn.commit()
    print("✅ Задача добавлена.")

def list_tasks():
    cursor.execute("SELECT id, task, done FROM tasks")
    tasks = cursor.fetchall()
    if not tasks:
        print("📭 Нет задач.")
    else:
        for tid, text, done in tasks:
            status = "✅" if done else "❌"
            print(f"[{tid}] {status} {text}")

def mark_done(task_id):
    cursor.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    print(f"☑️ Задача {task_id} отмечена как выполненная.")

def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    print(f"🗑️ Задача {task_id} удалена.")

# 🔁 Интерактивный режим
def interactive_mode():
    print("📋 Менеджер задач. Введите команду:")
    print("add \"текст\" | list | done <id> | delete <id> | exit")

    while True:
        command = input(">>> ").strip()

        if command.startswith("add "):
            task_text = command[4:].strip().strip('"')
            add_task(task_text)
        elif command == "list":
            list_tasks()
        elif command.startswith("done "):
            try:
                task_id = int(command[5:].strip())
                mark_done(task_id)
            except ValueError:
                print("❗ Неверный ID.")
        elif command.startswith("delete "):
            try:
                task_id = int(command[7:].strip())
                delete_task(task_id)
            except ValueError:
                print("❗ Неверный ID.")
        elif command == "exit":
            print("👋 Выход.")
            break
        else:
            print("❗ Неизвестная команда.")

# Запуск
interactive_mode()