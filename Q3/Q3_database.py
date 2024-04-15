import sqlite3

TaskListDB = 'task_list_db.sqlite'


def connect():
    conn = sqlite3.connect(TaskListDB)
    conn.row_factory = sqlite3.Row
    return conn


def close(conn):
    conn.close()


def view_pending_tasks(conn):
    cur = conn.cursor()
    query = """SELECT * FROM Task WHERE completed=0"""
    cur.execute(query)
    tasks = cur.fetchall()
    # To number the remaining pending tasks
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task[1]}")
    return tasks


def view_completed_tasks(conn):
    cur = conn.cursor()
    query = """SELECT * FROM Task WHERE completed=1"""
    cur.execute(query)
    tasks = cur.fetchall()
    # To number the completed tasks
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task[1]} (DONE!)")


def add_task(conn, task_obj):
    cur = conn.cursor()
    # Null value to ignore id
    query = """INSERT INTO Task VALUES (NULL, ?, ?)"""
    cur.execute(query, (task_obj.Description, task_obj.Completed))
    conn.commit()


def delete_task(conn, task_description):
    cur = conn.cursor()
    query = """DELETE FROM Task WHERE Description = ?"""
    cur.execute(query, (task_description,))
    conn.commit()


# To verify valid integer selected for complete method
def check_int(task_list) -> int:
    num = 0
    while True:
        try:
            num = int(input('Number: '))
            if num < 0:
                print("Number must be greater than or equal to zero.")
            elif num > len(task_list):
                print(num, "is not a valid number.")
            else:
                break
        except ValueError:
            print("Invalid input")
    return num


def complete_task(conn):
    todo_tasks = view_pending_tasks(conn)
    user_input = check_int(todo_tasks) - 1

    for i, task in enumerate(todo_tasks):
        if i == user_input:
            cur = conn.cursor()
            query = """UPDATE Task SET Completed = 1 WHERE taskID = ?"""
            cur.execute(query, (task["taskID"],))
            conn.commit()
