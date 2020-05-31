import threading
import socket
import sqlite3
import random

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
        # generates code for user
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

    @staticmethod
    def get_list(table_name, header, user_id):
        # this function returns list of friends or last connections
        conn = sqlite3.connect('projdb.db')  # connection to database
        cursor = conn.cursor()
        sql = "SELECT {} FROM {} WHERE user_id = ?".format(header, table_name)
        cursor.execute(sql, (user_id,))
        name_list = [num[0] for num in cursor.fetchall()]
        return name_list

    @staticmethod
    def update_number_cell(user_id, number):
        # create connection to database
        conn = sqlite3.connect('projdb.db')
        sql = 'UPDATE last_con SET number = ? WHERE user_id  = ? AND number = ?'
        conn.execute(sql, (number + 1, user_id, number))
        conn.commit()
        conn.close()

    def add_one(self, user_id):
        # this function add one to the number of each last connection
        last_list = self.get_list("last_con", "number", user_id)
        # add one to each last connection number
        # last_list.reverse()  # reverse the list so it will start updating from the higher number to lower
        for number in last_list:
            self.update_number_cell(user_id, int(number))
        # delete connection number 6 if exists
        try:
            last_conn = sqlite3.connect('projdb.db')
            last_conn.execute('DELETE FROM last_con WHERE number = ? and user_id = ?', (6, user_id))
            last_conn.commit()
            last_conn.close()
        except:
            pass

    @staticmethod
    def get_friend_list(user_id):
        # this function returns string of friends list
        conn = sqlite3.connect('projdb.db')  # connection to database
        sql = "SELECT name FROM friends WHERE user_id = ?"
        cur = conn.execute(sql, (user_id, ))
        friends = cur.fetchall()
        friends_text = ""
        for friend in friends:
            friends_text += friend[0] + ","
        friends_text = friends_text[:-1]
        print(friends_text)
        return friends_text

    @staticmethod
    def get_conn_list(user_id):
        # this function returns string of last connection list
        conn = sqlite3.connect('projdb.db')  # connection to database
        sql = "SELECT name FROM last_con WHERE user_id = ?"
        cur = conn.execute(sql, (user_id,))
        conns = cur.fetchall()
        conns_text = ""
        for con in conns:
            conns_text += con[0] + ","
        conns_text = conns_text[:-1]
        print(conns_text)
        return conns_text

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
        row = login_cursur.fetchall()
        if row:
            row = row[0]
            self.details["id"] = row[0]
            self.details["username"] = row[1]
            self.details["email"] = row[3]
            print(self.details)
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
        print(username, password)
        if self.login(username, password):
            self.stop_code = False
            friends = self.get_friend_list(self.details["id"])
            conns = self.get_conn_list(self.details["id"])
            self.send("{} {} {}".format(self.get_user_code(username), friends, conns))
        else:
            self.send("failed")

    def handle_code(self, data):
        _, code = data.split(" ")
        ip = None
        while ip is None:
            if self.stop_code:
                self.send("close_connection")
                self.stop_code = True
                return
            try:
                ip = codes[code]
            except:
                pass
        self.delete_code(code)
        self.send(ip)

    def handle_ip(self, data):
        _, code, ip = data.split(" ")
        self.add_code(code, ip)

    def recv(self):
        # the function receives messages from the client and send it to the appropriate function to handle it
        running = True
        while running:
            response = self.client_socket.recv(1024).decode()
            print(response)
            if response == "closing":
                self.client_socket.close()
                running = False
            if response.startswith("signup"):
                self.handle_signup(response)
            if response.startswith("login"):
                self.handle_login(response)
            if response.startswith("code"):
                code_thread = threading.Thread(target=self.handle_code, args=(response, ))
                code_thread.start()
            if response.startswith("ip"):
                self.handle_ip(response)
            if response.startswith("friend"):
                self.add_friend(response)
            if response.startswith("getcode"):
                self.send(self.get_user_code(response.split(" ")[1]))
            if response.startswith("addconn"):
                self.add_conn(response)
            if response.startswith("stopcode"):
                self.stop_code = True
            if response.startswith("delete"):
                self.delete_code(response.split(" ")[1])
                print(codes)

    def conn_exist(self, user_id, name):
        conn = sqlite3.connect('projdb.db')  # connection to database
        sql = "SELECT name FROM last_con WHERE user_id = ?"
        cur = conn.execute(sql, (user_id,))
        conns = cur.fetchall()
        for con in conns:
            if con[0] == name:
                conn.close()
                return True
        conn.close()
        return False

    def friend_exist(self, user_id, friend_name):
        conn = sqlite3.connect('projdb.db')  # connection to database
        sql = "SELECT name FROM friends WHERE user_id = ?"
        cur = conn.execute(sql, (user_id, ))
        friends = cur.fetchall()
        for name in friends:
            if name[0] == friend_name:
                conn.close()
                return True
        conn.close()
        return False

    def add_conn(self, name):
        _, name = name.split(" ")
        try:
            print("adding conn")
            # create connection to database
            if not self.conn_exist(self.details['id'], name):
                last_conn = sqlite3.connect('projdb.db')
                self.add_one(self.details['id'])
                last_conn.execute('INSERT INTO last_con (user_id, name, number) VALUES (?, ?, ?)',
                                  (self.details['id'], name, 1))
                print("connection added")
                self.send("connection added")
                last_conn.commit()
                last_conn.close()
            else:
                self.send("connection already exists")
        except:
            self.send("couldn't add connection")

    def add_friend(self, username):
        _, username = username.split(" ")
        try:
            print("trying to add friend")
            if username == self.details['username']:
                self.send("can't add yourself")
            elif self.does_cell_in_column("users", "username", username):
                print("name exist")
                # create connection to database
                friend_cone = sqlite3.connect('projdb.db')
                friend_cone.row_factory = sqlite3.Row
                # check user already have this friend
                if not self.friend_exist(self.details["id"], username):
                    # insert friend information to database
                    friend_cone.execute('INSERT INTO friends (user_id, name) VALUES (?, ?)',
                                        (self.details["id"], username))
                    friend_cone.commit()
                    self.send("friend added")
                else:
                    self.send("friend already exist")
                friend_cone.close()
            else:
                self.send("name does not exist")
        except:
            self.send("couldn't add friend")

    @staticmethod
    def add_code(code, ip):
        codes[code] = ip
        print(codes)

    @staticmethod
    def delete_code(code):
        del codes[code]

    def send(self, message):
        self.client_socket.send(message.encode())

    def __init__(self, client_socket, client_address):
        self.details = {}
        self.client_socket = client_socket
        self.client_address = client_address
        self.stop_code = False
        print("connection has started")
        recv_thread = threading.Thread(target=self.recv, args=())
        recv_thread.start()


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
