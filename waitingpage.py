#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    Apr 07, 2020 12:04:08 AM +0300  platform: Windows NT

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

import waitingpage_support


def vp_start_gui(main_client):
    """Starting point when module is the main routine."""
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    waitingpage_support.init(root, top, main_client)
    root.mainloop()


w = None


def create_Toplevel1(rt, *args, **kwargs):
    """Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' ."""
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    waitingpage_support.init(w, top, *args, **kwargs)
    return w, top


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font9 = "-family {Arial Black} -size 9 -weight bold"

        top.geometry("230x100+486+244")
        top.minsize(120, 1)
        top.maxsize(1370, 749)
        top.resizable(0, 0)
        top.title("waiting")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.waiting_label = tk.Label(top)
        self.waiting_label.place(relx=0.026, rely=0.05, height=80, width=210)
        self.waiting_label.configure(activebackground="#f9f9f9")
        self.waiting_label.configure(activeforeground="black")
        self.waiting_label.configure(anchor='nw')
        self.waiting_label.configure(background="#d9d9d9")
        self.waiting_label.configure(disabledforeground="#a3a3a3")
        self.waiting_label.configure(font="-family {Arial Rounded MT Bold} -size 24 -weight bold")
        self.waiting_label.configure(foreground="#000000")
        self.waiting_label.configure(highlightbackground="#d9d9d9")
        self.waiting_label.configure(highlightcolor="black")
        self.waiting_label.configure(text='''Waiting.''')

        self.cancelbutton = tk.Button(top)
        self.cancelbutton.place(relx=0.605, rely=0.584, height=34, width=67)
        self.cancelbutton.configure(activebackground="#ececec")
        self.cancelbutton.configure(activeforeground="#000000")
        self.cancelbutton.configure(background="#00a6ff")
        self.cancelbutton.configure(disabledforeground="#a3a3a3")
        self.cancelbutton.configure(font=font9)
        self.cancelbutton.configure(cursor="hand2")
        self.cancelbutton.configure(foreground="#000000")
        self.cancelbutton.configure(highlightbackground="#d9d9d9")
        self.cancelbutton.configure(highlightcolor="black")
        self.cancelbutton.configure(pady="0")
        self.cancelbutton.configure(text='''Cancel''')
        self.cancelbutton.configure(command=waitingpage_support.cancel)
