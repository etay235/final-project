import threading
import socket
import sqlite3
import random
import string


def handle_client(client_socket, client_address):
    print("connection has started")
    while True:
        response = client_socket.recv(1024).decode()
        print(response)
        data = response.split(" ")
        if len(data) == 3:
            answer = sign_up(data[0], data[1], data[2])
            client_socket.send(answer.encode())
        if len(data) == 2:
            print(data[0], data[1])
            if login(data[0], data[1]):
                client_socket.send("login succeed".encode())
                client_socket.send(get_user_code(data[0]).encode())
            else:
                client_socket.send("login failed".encode())


def does_cell_in_column(table_name, column, cell):
    conn = sqlite3.connect('projdb.db')
    sql = "SELECT {} FROM {} WHERE {} = ?".format(column, table_name, column)
    cur = conn.execute(sql, (cell, ))
    check = cur.fetchall()
    if len(check) > 0:
        conn.close()
        return True
    conn.close()
    return False


def generatecode():
    l1 = random.choice(string.ascii_letters)
    l2 = random.choice(string.ascii_letters)
    n1 = random.randint(10, 99)
    n2 = random.randint(10, 99)
    n3 = random.randint(10, 99)
    code = "{}{}{}{}{}".format(n3, l1, n2, l2, n1)
    if does_cell_in_column("users", "code", code):
        return generatecode()
    return code


def sign_up(username, password, email):
    # crate connection to database
    signup_conn = sqlite3.connect('projdb.db')
    signup_conn.row_factory = sqlite3.Row
    # check of username or email already exist
    user = False
    eml = False
    if does_cell_in_column("users", "username", username):
        user = True
    if does_cell_in_column("users", "email", email):
        eml = True
    if user or eml:
        signup_conn.close()
        return "{} {}".format(user, eml)
    # create code for user
    code = generatecode()
    print(username, password, email, code)
    # insert user information to database
    signup_conn.execute('INSERT INTO users (username, password, email, code) VALUES (?, ?, ?, ?)',
                        (username, password, email, code))
    signup_conn.commit()
    signup_conn.close()
    return "succeed"


def login(username, password):
    print(username, password)
    # create connection to database
    login_conn = sqlite3.connect('projdb.db')
    login_cursur = login_conn.cursor()
    # check if user exist
    login_cursur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    if login_cursur.fetchall():
        login_conn.close()
        return True
    login_conn.close()
    return False


def get_user_code(username):
    # create connection
    code_conn = sqlite3.connect('projdb.db')
    code_cursor = code_conn.cursor()
    # get user's code
    code_cursor.execute('SELECT code FROM users WHERE username = ?', (username,))
    code = code_cursor.fetchall()[0][0]
    return code


def main():
    port = 9000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(100)
    while True:
        print("waiting for client")
        new_client_socket, new_client_address = server_socket.accept()
        client_conn = threading.Thread(target=handle_client, args=(new_client_socket, new_client_address))
        client_conn.start()


if __name__ == "__main__":
    main()
