from Q3_business import Task
import Q3_database as db


def menu():
    print("COMMAND MENU")
    print("view     - View pending tasks")
    print("history  - View completed tasks")
    print("add      - Add new task")
    print("complete - Complete a task")
    print("delete   - Delete a task")
    print("exit     - Exit program\n")


def add_task(connection):
    description = input("Description: ").capitalize()
    completed = 0
    task = Task(description, completed)
    db.add_task(connection, task)


def delete_task(connection):
    description = input("Description: ").capitalize()
    db.delete_task(connection, description)


def main():
    conn = db.connect()
    print("Task List\n")
    menu()
    while True:
        command = input("command: ").lower()
        if command == "view":
            db.view_pending_tasks(conn)
            print()
        elif command == "history":
            db.view_completed_tasks(conn)
            print()
        elif command == "add":
            add_task(conn)
            print()
        elif command == "delete":
            delete_task(conn)
            print()
        elif command == "complete":
            db.complete_task(conn)
            print()
        elif command == "exit":
            print("Bye!")
            db.close(conn)
            break


if __name__ == "__main__":
    main()
