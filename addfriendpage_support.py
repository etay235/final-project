#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    May 19, 2020 12:45:27 AM +0300  platform: Windows NT

import sys

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


def init(top, gui, main_client, *args, **kwargs):
    global w, top_level, root, client
    w = gui
    top_level = top
    root = top
    client = main_client


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


def add_friend(friend_name):
    global client
    client.add_friend(friend_name)


def change_message(message):
    global w
    w.messagetxt['text'] = message


if __name__ == '__main__':
    import addfriendpage
    addfriendpage.vp_start_gui()




