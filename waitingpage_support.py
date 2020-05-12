#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    Apr 07, 2020 12:04:13 AM +0300  platform: Windows NT

import sys
import time
import threading


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


def init(top, gui, *args, **kwargs):
    global w, top_level, root, stop
    w = gui
    top_level = top
    root = top
    waiting_thread = threading.Thread(target=change_text, args=())
    waiting_thread.start()


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


def change_text():
    global w
    global stop
    stop = False
    text = ["Waiting.", "Waiting..", "Waiting..."]
    while True:
        for word in text:
            time.sleep(0.2)
            w.waiting_label['text'] = word
        if stop:
            if w is not None:
                destroy_window()
            break
        time.sleep(0.2)


if __name__ == '__main__':
    import waitingpage
    waitingpage.vp_start_gui()
