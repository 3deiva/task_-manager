

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

# take input
task_name = input("Enter task: ")

# store task
add_task(task_name)

# show tasks
cursor.execute("SELECT * FROM tasks")
rows = cursor.fetchall()

for r in rows:
    print(r)

conn.close()
