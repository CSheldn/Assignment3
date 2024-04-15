from Q2_business import Player
import Q2_database as db


def menu():
    print("COMMAND MENU")
    print("view - View players")
    print("add - Add a player")
    print("del - Delete a player")
    print("exit - Exit program\n")


def add_player(connection):
    name = input("Name: ").title()
    wins = int(input("Wins: "))
    losses = int(input("Losses: "))
    ties = int(input("Ties: "))

    # Checks to make sure integer is valid
    if wins < 0 or losses < 0 or ties < 0:
        print("Invalid input, must be positive integer values")
    else:
        player = Player(name, wins, losses, ties)
        db.add_player(connection, player)
        print(f"{name} was added to the database")


def delete_player(connection):
    name = input("Name: ").title()
    db.delete_player(connection, name)
    print(f"{name} was deleted from the database")


def main():
    conn = db.connect()
    print("Player Manager\n")
    menu()
    while True:
        command = input("Command: ").lower()
        if command == "view":
            print("Name\t\t Wins\tLosses\t\tTies\t Games")
            print("-"*50)
            db.view_players(conn)
            print()
        elif command == "add":
            add_player(conn)
            print()
        elif command == "del":
            delete_player(conn)
            print()
        elif command == "exit":
            print("Bye!")
            db.close(conn)
            break


if __name__ == "__main__":
    main()
