import sqlite3

playerDBFiles = 'player_db.sqlite'


def connect():
    conn = sqlite3.connect(playerDBFiles)
    conn.row_factory = sqlite3.Row
    return conn


def close(conn):
    conn.close()


def add_player(conn, player_obj):
    cur = conn.cursor()
    # Null value for the id to properly pull the correct columns
    query = """INSERT INTO Player VALUES (NULL, ?, ?, ?, ?)"""
    cur.execute(query, (player_obj.Name, player_obj.Wins, player_obj.Losses, player_obj.Ties))
    conn.commit()


def delete_player(conn, player_name):
    cur = conn.cursor()
    query = """DELETE FROM Player WHERE Name = ?"""
    cur.execute(query, (player_name,))
    conn.commit()


def view_players(conn):
    cur = conn.cursor()
    query = """SELECT * FROM Player ORDER BY Wins DESC"""
    cur.execute(query)
    players = cur.fetchall()
    for player in players:
        # Selecting the columns and adding the totals to get the amount of games
        print(f"{player[1]}\t\t\t{player[2]}\t\t {player[3]}\t\t   {player[4]}\t\t{player[2]+player[3]+player[4]}")
