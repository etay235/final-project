import threading
import socket
import sqlite3
import random
import string

codes = {}


class handle_client:
    def does_cell_in_column(self, table_name, column, cell):
        conn = sqlite3.connect('projdb.db')  # connection to database
        sql = "SELECT {} FROM {} WHERE {} = ?".format(column, table_name, column)
        cur = conn.execute(sql, (cell, ))
        check = cur.fetchall()
        if len(check) > 0:
            conn.close()
            return True
        conn.close()
        return False

    def generatecode(self):
        code = "{}".format(random.randint(1000000, 9999999))
        if self.does_cell_in_column("users", "code", code):
            return self.generatecode()
        return code

    def get_user_code(self, username):
        # create connection
        code_conn = sqlite3.connect('projdb.db')
        code_cursor = code_conn.cursor()
        # get user's code
        code_cursor.execute('SELECT code FROM users WHERE username = ?', (username,))
        code = code_cursor.fetchall()[0][0]
        return code

    def sign_up(self, username, password, email):
        # crate connection to database
        signup_conn = sqlite3.connect('projdb.db')
        signup_conn.row_factory = sqlite3.Row
        # check of username or email already exist
        user = False
        eml = False
        if self.does_cell_in_column("users", "username", username):
            user = True
        if self.does_cell_in_column("users", "email", email):
            eml = True
        if user or eml:
            return "{} {}".format(user, eml)
        # create code for user
        code = self.generatecode()
        print(username, password, email, code)
        # insert user information to database
        signup_conn.execute('INSERT INTO users (username, password, email, code) VALUES (?, ?, ?, ?)',
                            (username, password, email, code))
        signup_conn.commit()
        signup_conn.close()
        return "succeed"

    def login(self, username, password):
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

    def handle_signup(self, data):
        _, username, password, email = data.split(" ")
        answer = self.sign_up(username, password, email)
        self.send(answer)

    def handle_login(self, data):
        _, username, password = data.split(" ")
        if self.login(username, password):
            self.send(self.get_user_code(username))
        else:
            self.send("failed")

    def handle_code(self, data):
        _, code = data.split(" ")
        ip = None
        while ip is None:
            try:
                ip = codes[code]
            except:
                pass
        delete_code(code)
        print(ip)
        self.send(ip)

    @staticmethod
    def handle_ip(data):
        _, code, ip = data.split(" ")
        add_code(code, ip)

    def recv(self):
        # the function receives messages from the client and send it to the appropriate function to handle it
        print("start recv")
        while True:
            response = self.client_socket.recv(1024).decode()
            print(response)
            if response.startswith("signup"):
                self.handle_signup(response)
            if response.startswith("login"):
                self.handle_login(response)
            if response.startswith("code"):
                self.handle_code(response)
            if response.startswith("ip"):
                self.handle_ip(response)

    def send(self, message):
        self.client_socket.send(message.encode())

    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address
        print("connection has started")
        recv_thread = threading.Thread(target=self.recv, args=())
        recv_thread.start()


def add_code(code, ip):
    codes[code] = ip
    print(codes)


def delete_code(code):
    del codes[code]


def main():
    port = 9000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(100)
    while True:
        print("waiting for client")
        new_client_socket, new_client_address = server_socket.accept()
        client_conn = threading.Thread(target=handle_client, args=(new_client_socket, new_client_address))
        client_conn.start()


if __name__ == "__main__":
    main()
