
import sqlite3

# connect to database (creates file if not exists)
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

# create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL
)
''')

# function to add task
def add_task(task):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()

# function to view tasks
def view_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    for r in rows:
        print(r)

# simple input
task_name = input("Enter task: ")
add_task(task_name)

print("\nSaved Tasks:")
view_tasks()

conn.close()
