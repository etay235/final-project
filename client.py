import threading
import socket
import pygame
import ctypes
import time
import enum
import loginpage
import signuppage
import mainpage
import waitingpage
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener
from zlib import compress
from zlib import decompress
from mss import mss
from ctypes import windll, Structure, c_long, byref


secondary_port = 8023
scroll_amount = 100
max_bytes = 65000

server_ip = '127.0.0.1'
server_port = 9000


def main():
    global main_client
    global opened
    opened = False
    main_client = MainClient()
    # answer = input("client or server")
    # if answer == "c":
    #     c = User(input("insert ip"))
    # elif answer == "s":
    #     s = Server()
    # else:
    #     print("insert again")


class MainClient:
    @staticmethod
    def close_signup_page():
        signuppage.signuppage_support.destroy_window()

    @staticmethod
    def close_login_page():
        loginpage.loginpage_support.destroy_window()

    @staticmethod
    def close_main_page():
        mainpage.mainpage_support.destroy_window()

    def open_signup_page(self):
        signuppage.vp_start_gui(self)

    def open_login_page(self):
        loginpage.vp_start_gui(self)

    def open_mainpage(self, code):
        mainpage.vp_start_gui(self, code)

    @staticmethod
    def open_waiting_page():
        waitingpage.vp_start_gui()

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
        if answer == "failed":
            loginpage.loginpage_support.failed_login()
        else:
            self.close_login_page()
            self.open_mainpage(answer)

    @staticmethod
    def get_ip():
        hostname = socket.gethostname()
        my_ip = socket.gethostbyname(hostname)
        print(hostname, my_ip)
        return my_ip

    def send(self, message):
        print(message)
        self.server_socket.send(message.encode())

    @staticmethod
    def stop_waitingpage():
        waitingpage.waitingpage_support.stop = True

    def start_connection(self):
        self.close_main_page()
        self.waitingpage_thread.start()
        if self.tech_or_user == "u":
            self.send("ip {} {}".format(self.code, self.get_ip()))
            server = Server()
        else:
            self.send("code {}".format(self.code))
            user_ip = self.server_socket.recv(1024).decode()
            user = User(user_ip)

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((server_ip, server_port))
        self.waitingpage_thread = threading.Thread(target=self.open_waiting_page, args=())
        self.tech_or_user = "u"
        self.code = ""
        login_page_thread = threading.Thread(target=self.open_login_page, args=())
        login_page_thread.start()


class User:
    def socket_send(self, conn_socket, message, port):
        connection_address_port = (self.client_ip, port)
        conn_socket.sendto(message.encode(), connection_address_port)

    def socket_recv(self, conn_socket, msgsize):
        full_message, address = conn_socket.recvfrom(msgsize)
        return full_message

    def recvall(self, length):
        # recv all the pixels of a picture
        buf = b''
        while len(buf) < length:
            data = self.client_socket.recvfrom(self.max_bytes)
            data = data[0]
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
            if isinstance(key, enum.Enum):
                data = "{} {} {}".format("space" if str(key.value)[1:-1:1] == ' ' else key.value, "release", "enum")
            else:
                data = "{} {} {}".format(key.char, "release", "char")
            self.socket_send(self.client_socket, data, self.port)
            if key == Key.esc:  # if key esc is pressed stop
                mouse_listener.stop()
                keyboard_listener.stop()
                return False

        def on_press(key):
            if isinstance(key, enum.Enum):
                data = "{} {} {}".format("space" if str(key.value)[1:-1:1] == ' ' else key.value, "press", "enum")
            else:
                data = "{} {} {}".format(key.char, "press", "char")
            self.socket_send(self.client_socket, data, self.port)

        # mouse listener functions
        def on_move(x, y):
            x, y = change_xy(x, y)
            data = "{} {}".format(x, y)
            self.socket_send(self.client_socket, data, self.port)

        def on_click(x, y, button, pressed):
            x, y = change_xy(x, y)
            n1, n2 = button.value
            data = "{} {} {} {} {}".format(x, y, n1, n2, 'pressed' if pressed else 'released')
            self.socket_send(self.client_socket, data, self.port)

        def on_scroll(x, y, dx, dy):
            x, y = change_xy(x, y)
            data = "{} {} {} {}".format(x, y, dx, dy)
            self.socket_send(self.client_socket, data, self.port)

        # create listeners
        with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener, KeyboardListener(
                on_press=on_press, on_release=on_release) as keyboard_listener:
            # start listeners
            mouse_listener.join()
            keyboard_listener.join()

    def change_screen_size(self, self_width, self_height, other_width, other_height):
        scale_x = other_width / self_width
        scale_y = other_height / self_height
        if scale_x > scale_y:
            self_height = other_height / scale_x
        else:
            self_width = other_width / scale_y
        return int(self_width), int(self_height)

    def open_window(self):
        self.client_socket.sendto("connected".encode(), (self.client_ip, self.port))  # connect to computer
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
        watching = True
        # print other computer screen
        try:
            while watching:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            watching = False
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
        print("connecting to server")
        MainClient.stop_waitingpage()
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
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.window_thread = threading.Thread(target=self.open_window)
        self.listeners_thread = threading.Thread(target=self.send_listeners)
        self.window_thread.start()
        self.listeners_thread.start()


class Server:
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

    def main_control(self):
        while True:
            data, _ = self.client_socket.recvfrom(self.max_bytes)
            data = data.decode()
            data = data.split(" ")
            if len(data) != 3:
                self.control_mouse(data)
            else:
                self.control_keyboard(data)

    def control_keyboard(self,  data):
        key, press_or_release, enum_or_char = data
        if enum_or_char == "char":
            if press_or_release == "press":
                self.keyboard.press(key)
            else:
                self.keyboard.release(key)
        else:
            try:
                new_key = Key(self.keyboard._KeyCode.from_vk(int(key[1:-1:1])))
            except:
                new_key = Key.space
            if press_or_release == "press":
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
        print("server has started")
        MainClient.stop_waitingpage()
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        self.WIDTH = user32.GetSystemMetrics(0)
        self.HEIGHT = user32.GetSystemMetrics(1)
        self.max_bytes = max_bytes
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.client_ip = "0.0.0.0"
        self.port = secondary_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind((self.client_ip, self.port))
        data, self.address = self.client_socket.recvfrom(self.max_bytes)
        thread = threading.Thread(target=self.send_screen)
        control_thread = threading.Thread(target=self.main_control)
        thread.start()
        control_thread.start()


if __name__ == '__main__':
    main()


