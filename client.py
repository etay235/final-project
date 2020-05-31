import threading
import socket
import pickle
import pygame
import ctypes
import time
import os
import re
import loginpage
import signuppage
import mainpage
import waitingpage
import addfriendpage
import alertmessage
import techalertmessage
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
from zlib import compress
from zlib import decompress
from mss import mss
import win32console
import win32gui


#Hide the Console
window = win32console.GetConsoleWindow()
win32gui.ShowWindow(window, 0)

secondary_port = 8023
scroll_amount = 75
max_bytes = 65000

file = open("server_ip.txt", "r")
server_ip = file.read()
file.close()
server_port = 9000


def main():
    global main_client
    global opened
    opened = False
    main_client = MainClient()


class MainClient:
    def stop_connection(self, tech_or_client):
        self.close = None
        if tech_or_client == "client":
            alertmessage.vp_start_gui(self)
        else:
            techalertmessage.vp_start_gui(self)
        while self.close is None:
            pass
        if self.close == 'yes':
            return True
        else:
            return False

    @staticmethod
    def close_signup_page():
        signuppage.signuppage_support.destroy_window()

    @staticmethod
    def close_login_page():
        loginpage.loginpage_support.destroy_window()

    @staticmethod
    def close_main_page():
        mainpage.mainpage_support.destroy_window()

    @staticmethod
    def close_addfriend_page():
        addfriendpage.addfriendpage_support.destroy_window()

    def open_addfriend_page(self):
        addfriendpage.vp_start_gui(self)

    def open_signup_page(self):
        signuppage.vp_start_gui(self)

    def open_login_page(self):
        loginpage.vp_start_gui(self)

    def open_mainpage(self, data):
        mainpage.vp_start_gui(self, data)

    def open_waiting_page(self):
        waitingpage.vp_start_gui(self)

    def on_closing(self):
        self.send("closing")
        self.server_socket.close()
        print("close socket")
        os._exit(1)

    def sign_up(self, username, password, email):
        self.send("signup {} {} {}".format(username, password, email))
        response = self.server_socket.recv(1024).decode()
        if response == "succeed":
            self.close_signup_page()
            self.open_login_page()
        else:
            user, eml = response.split(" ")
            signuppage.failed_signup(user, eml)

    def login(self, username, password):
        print(username, password)
        self.send("login {} {}".format(username, password))
        answer = self.server_socket.recv(1024).decode()
        print(answer)
        if answer == "failed":
            loginpage.loginpage_support.failed_login()
        else:
            self.close_login_page()
            print(answer)
            self.name = username
            self.open_mainpage(answer)

    def wait_close(self):
        if self.tech_or_user == "u":
            self.send("delete {}".format(self.code))
            temp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            temp_socket.sendto("close_connection".encode(), ("127.0.0.1", secondary_port))
            temp_socket.close()
        else:
            self.send("stopcode")
        mainpage.mainpage_support.change_state()

    def add_friend(self, name):
        self.send("friend {}".format(name))
        answer = self.server_socket.recv(1024).decode()
        print(answer)
        if answer == "friend added":
            mainpage.mainpage_support.w.friendslist.insert("end", name)
            self.close_addfriend_page()
        else:
            addfriendpage.addfriendpage_support.change_message(answer)

    def add_conn(self, name):
        print(name)
        self.send("addconn {}".format(name))
        answer = self.server_socket.recv(1024).decode()
        print(answer)

    def get_friend_code(self, name):
        print(name)
        self.send("getcode {}".format(name))
        code = self.server_socket.recv(1024).decode()
        print(code)
        mainpage.mainpage_support.change_code(code)

    @staticmethod
    def get_ip():
        addresses = os.popen('IPCONFIG | FINDSTR /R "Ethernet adapter Local Area Connection .* Address.*[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*"')
        my_ip = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', addresses.read()).group()
        return my_ip

    def send(self, message):
        print(message)
        self.server_socket.send(message.encode())

    @staticmethod
    def stop_waitingpage():
        waitingpage.waitingpage_support.stop = True

    def start_connection(self):
        self.waitingpage_thread = threading.Thread(target=self.open_waiting_page, args=())
        self.waitingpage_thread.start()
        if self.tech_or_user == "u":
            self.send("ip {} {}".format(self.code, self.get_ip()))
            server = Server()
        else:
            self.send("code {}".format(self.code))
            user_ip = self.server_socket.recv(1024).decode()
            if user_ip != "close_connection":
                user = User(user_ip)
            else:
                print("connection closed")

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((server_ip, server_port))
        self.waitingpage_thread = threading.Thread(target=self.open_waiting_page, args=())
        self.tech_or_user = "u"
        self.code = ""
        self.name = ""
        self.data = ""
        self.close = None
        login_page_thread = threading.Thread(target=self.open_login_page, args=())
        login_page_thread.start()


class User:
    def close(self, check="none"):
        global main_client
        main_client.on_closing()
        self.watching = False
        if check == "first":
            connection_address_port = (self.client_ip, self.port)
            self.client_socket.sendto("close".encode(), connection_address_port)
        os._exit(1)

    @staticmethod
    def push_window_on_top():
        from ctypes import POINTER, WINFUNCTYPE, windll
        from ctypes.wintypes import BOOL, HWND, RECT
        # get our window ID:
        hwnd = pygame.display.get_wm_info()["window"]
        # Jump through all the ctypes hoops:
        prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
        paramflags = (1, "hwnd"), (2, "lprect")
        GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
        # finally get our data!
        rect = GetWindowRect(hwnd)
        x = rect.left
        y = rect.top
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

    def socket_send(self, conn_socket, message, port):
        connection_address_port = (self.client_ip, port)
        conn_socket.sendto(message.encode(), connection_address_port)

    def socket_recv(self, conn_socket, msgsize):
        full_message, address = conn_socket.recvfrom(msgsize)
        try:
            if full_message.decode() == "close":
                self.close()
        except:
            pass
        return full_message

    def recvall(self, length):
        # recv all the pixels of a picture
        buf = b''
        while len(buf) < length:
            data = self.client_socket.recvfrom(self.max_bytes)
            # add if decode later *****************************************************************************************************
            data = data[0]
            try:
                if data.decode() == "close":
                    self.close()
            except:
                pass
            if not data:
                return data
            buf += data
        return buf

    def send_listeners(self):
        def change_xy(x, y):
            # adjust x and y size to the other computer size
            x = int(x * prop_x)
            y = int(y * prop_y)
            return x, y
        while self.width == -1:  # wait for open window and then start the listeners
            pass
        prop_x = self.width / self.WIDTH
        prop_y = self.height / self.HEIGHT

        # keyboard listener functions
        def on_release(key):
            if self.control and pygame.mouse.get_focused():
                if self.dont_send and key == (Key.tab or Key.alt_l or Key.alt_r):
                    self.dont_send = False
                else:
                    if key != Key.esc:  # if key is esc don't send
                        data = [key, "release"]
                        keysend = pickle.dumps(data)
                        connection_address_port = (self.client_ip, self.port)
                        self.client_socket.sendto(keysend, connection_address_port)

        def on_press(key):
            if self.control and pygame.mouse.get_focused():
                if key == Key.tab or key == Key.alt_l or key == Key.alt_r or key == Key.cmd:
                    self.dont_send = True
                    self.keyboard.release(key)
                if key != Key.esc:  # if key is esc don't send
                    data = [key, "press"]
                    keysend = pickle.dumps(data)
                    connection_address_port = (self.client_ip, self.port)
                    self.client_socket.sendto(keysend, connection_address_port)

        # mouse listener functions
        def on_move(x, y):
            if self.control and pygame.mouse.get_focused():
                x, y = change_xy(x, y)
                data = "{} {}".format(x, y)
                self.socket_send(self.client_socket, data, self.port)

        def on_click(x, y, button, pressed):
            if self.control and pygame.mouse.get_focused():
                x, y = change_xy(x, y)
                n1, n2 = button.value
                data = "{} {} {} {} {}".format(x, y, n1, n2, 'pressed' if pressed else 'released')
                self.socket_send(self.client_socket, data, self.port)

        def on_scroll(x, y, dx, dy):
            if self.control and pygame.mouse.get_focused():
                x, y = change_xy(x, y)
                data = "{} {} {} {}".format(x, y, dx, dy)
                self.socket_send(self.client_socket, data, self.port)

        # create listeners
        with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener, KeyboardListener(
                on_press=on_press, on_release=on_release) as keyboard_listener:
            # start listeners
            self.mouse_listener = mouse_listener
            self.keyboard_listener = keyboard_listener
            self.mouse_listener.join()
            self.keyboard_listener.join()

    def change_screen_size(self, self_width, self_height, other_width, other_height):
        scale_x = other_width / self_width
        scale_y = other_height / self_height
        if scale_x > scale_y:
            self_height = other_height / scale_x
        else:
            self_width = other_width / scale_y
        return int(self_width), int(self_height)

    def open_window(self):
        global main_client
        time.sleep(0.5)
        main_client.stop_waitingpage()
        close_main_page_thread = threading.Thread(target=main_client.close_main_page)
        close_main_page_thread.start()
        # connect and send name to server
        self.client_socket.sendto(main_client.name.encode(), (self.client_ip, self.port))
        name = self.client_socket.recv(1024).decode()
        main_client.add_conn(name)
        # get other computer width and height
        data = self.socket_recv(self.client_socket, 1024).decode()
        self.width, self.height = data.split(",")
        self.width = int(self.width)
        self.height = int(self.height)
        # adjust screen size to other computer
        self.WIDTH, self.HEIGHT = self.change_screen_size(self.WIDTH, self.HEIGHT, self.width, self.height)
        # open the window
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        # print other computer screen
        try:
            while self.watching:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if pygame.mouse.get_focused():
                                self.control = False
                                print("to stop or not to stop")
                                answer = self.main_client.stop_connection("tech")
                                if answer == "back":
                                    print("go back")
                                elif answer:
                                    self.close("first")
                                else:
                                    self.control = True
                        break
                size = int.from_bytes(self.socket_recv(self.client_socket, self.max_bytes), byteorder='big')
                while size > 10000000:  # checks if it size and not part of the pixels
                    size = int.from_bytes(self.socket_recv(self.client_socket, self.max_bytes), byteorder='big')
                temp_pixels = self.recvall(size)
                try:
                    pixels = decompress(temp_pixels)
                    # Create the Surface from raw pixels
                    img = pygame.image.fromstring(pixels, (self.width, self.height), 'RGB')
                    picture = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
                    # Display the picture
                    screen.blit(picture, (0, 0))
                    pygame.display.flip()
                    clock.tick(60)
                except:
                    pass
        finally:
            self.client_socket.close()

    def __init__(self, client_ip):
        global main_client
        print("connecting to server")
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.width = -1
        self.height = -1
        self.SetCursorPos = ctypes.windll.user32.SetCursorPos
        self.mouse_event = ctypes.windll.user32.mouse_event
        self.WIDTH = user32.GetSystemMetrics(0)
        self.HEIGHT = user32.GetSystemMetrics(1)
        self.max_bytes = max_bytes
        self.client_ip = client_ip
        self.port = secondary_port
        self.control = True
        self.stop_all = False
        self.watching = True
        self.main_client = main_client
        self.mouse_listener = ""
        self.keyboard_listener = ""
        self.keyboard = KeyboardController()
        self.dont_send = False
        self.w_dont_send = False
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.window_thread = threading.Thread(target=self.open_window)
        self.listeners_thread = threading.Thread(target=self.send_listeners)
        self.window_thread.start()
        self.listeners_thread.start()


class Server:
    def close(self, check="none"):
        global main_client
        main_client.on_closing()
        if check == "first":
            self.client_socket.sendto("close".encode(), self.address)
        os._exit(1)

    def stop(self):
        # keyboard listener functions
        def on_release(key):
            print(key)
            if key == Key.esc:  # if key esc is pressed stop
                global main_client
                self.control = False
                if main_client.stop_connection("client"):
                    self.close("first")
                else:
                    self.control = True
        # create listener
        with KeyboardListener(on_release=on_release) as keyboard_listener:
            # start listener
            keyboard_listener.join()

    def send_screen(self):
        with mss() as sct:
            rect = {'top': 0, 'left': 0, 'width': self.WIDTH, 'height': self.HEIGHT}
            screen_size = "{},{}".format(self.WIDTH, self.HEIGHT)
            self.client_socket.sendto(screen_size.encode(), self.address)
            while True:
                img = sct.grab(rect)
                pixels = compress(img.rgb, 6)
                size = len(pixels)
                size_len = (size.bit_length() + 7) // 8
                size_bytes = size.to_bytes(size_len, 'big')
                self.client_socket.sendto(size_bytes, self.address)
                sleep = False
                if size > 200000:
                    sleep = True
                while self.max_bytes < len(pixels):
                    part_pixels = pixels[:self.max_bytes]
                    self.client_socket.sendto(part_pixels, self.address)
                    if sleep:
                        time.sleep(0.001)
                    pixels = pixels[self.max_bytes:]
                self.client_socket.sendto(pixels, self.address)
                if self.stop_running:
                    break

    def main_control(self):
        while True:
            data = self.client_socket.recv(self.max_bytes)
            if self.control:
                try:
                    if data.decode() == "close":
                        self.close()
                    else:
                        pass
                    data = data.decode()
                    data = data.split(" ")
                    self.control_mouse(data)
                except:
                    key = pickle.loads(data)
                    self.control_keyboard(key)

    def control_keyboard(self, key):
        new_key = key[0]
        rop = key[1]
        if rop == "press":
            self.keyboard.press(new_key)
        else:
            self.keyboard.release(new_key)

    def control_mouse(self, data):
        if len(data) == 2:
            x, y = data
            self.mouse.position = (int(x), int(y))
        elif len(data) == 4:
            x, y, dx, dy = data
            self.mouse.position = (int(x), int(y))
            self.mouse.scroll(100 * int(dx), 100 * int(dy))
        else:
            x, y, n1, n2, pressed = data
            button = Button((int(n1), int(n2)))
            self.mouse.position = (int(x), int(y))
            if pressed == "pressed":
                self.mouse.press(button)
            else:
                self.mouse.release(button)

    def __init__(self):
        global main_client
        print("server has started")
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.WIDTH = user32.GetSystemMetrics(0)
        self.HEIGHT = user32.GetSystemMetrics(1)
        self.max_bytes = max_bytes
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.client_ip = "0.0.0.0"
        self.port = secondary_port
        self.control = True
        self.stop_running = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((self.client_ip, self.port))
        data, self.address = self.client_socket.recvfrom(self.max_bytes)
        if data.decode() == "close_connection":
            self.client_socket.close()
            print("server closed")
            return
        main_client.stop_waitingpage()
        main_client.close_main_page()
        main_client.add_conn(data.decode())
        self.client_socket.sendto(main_client.name.encode(), self.address)
        thread = threading.Thread(target=self.send_screen)
        control_thread = threading.Thread(target=self.main_control)
        stop_thread = threading.Thread(target=self.stop)
        thread.start()
        control_thread.start()
        stop_thread.start()


if __name__ == '__main__':
    main()
