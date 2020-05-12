#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    Mar 31, 2020 04:17:45 PM +0300  platform: Windows NT

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

import mainpage_support


def vp_start_gui(main_client, user_code):
    '''Starting point when module is the main routine.'''
    global val, w, root, code
    code = user_code
    root = tk.Tk()
    top = RemoteTechnicianPage (root)
    mainpage_support.init(root, top, main_client)
    root.mainloop()


w = None


def create_RemoteTechnicianPage(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_RemoteTechnicianPage(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = RemoteTechnicianPage (w)
    mainpage_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_RemoteTechnicianPage():
    global w
    w.destroy()
    w = None


def user_button_click():
    mainpage_support.user_button_click()


def tech_button_click():
    mainpage_support.tech_button_click()


class RemoteTechnicianPage:
    def __init__(self, top=None):
        global code
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font10 = "-family {Arial Black} -size 12 -weight bold"
        font9 = "-family {Arial Rounded MT Bold} -size 20"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("611x441+352+149")
        top.minsize(120, 1)
        top.maxsize(1370, 729)
        top.resizable(1, 1)
        top.title("Remote Technician")
        top.configure(background="#d9d9d9")

        self.userbutton = tk.Button(top)
        self.userbutton.place(relx=0.295, rely=0.245, height=34, width=77)
        self.userbutton.configure(activebackground="#ececec")
        self.userbutton.configure(activeforeground="#000000")
        self.userbutton.configure(background="#d9d9d9")
        self.userbutton.configure(cursor="hand2")
        self.userbutton.configure(disabledforeground="#a3a3a3")
        self.userbutton.configure(foreground="#000000")
        self.userbutton.configure(highlightbackground="#d9d9d9")
        self.userbutton.configure(highlightcolor="black")
        self.userbutton.configure(pady="0")
        self.userbutton.configure(relief="sunken")
        self.userbutton.configure(text='''User''')
        self.userbutton.configure(command=user_button_click)

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.218, rely=0.084, height=41, width=340)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font9)
        self.Label1.configure(foreground="#487efd")
        self.Label1.configure(highlightbackground="#000000")
        self.Label1.configure(highlightcolor="#00a6ff")
        self.Label1.configure(text='''Remote Technician''')

        self.technicianbutton = tk.Button(top)
        self.technicianbutton.place(relx=0.589, rely=0.245, height=34, width=77)
        self.technicianbutton.configure(activebackground="#ececec")
        self.technicianbutton.configure(activeforeground="#000000")
        self.technicianbutton.configure(background="#d9d9d9")
        self.technicianbutton.configure(cursor="hand2")
        self.technicianbutton.configure(disabledforeground="#a3a3a3")
        self.technicianbutton.configure(foreground="#000000")
        self.technicianbutton.configure(highlightbackground="#d9d9d9")
        self.technicianbutton.configure(highlightcolor="black")
        self.technicianbutton.configure(pady="0")
        self.technicianbutton.configure(text='''Technician''')
        self.technicianbutton.configure(command=tech_button_click)

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.098, rely=0.512, relheight=0.456
                               , relwidth=0.283)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''last connections''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")

        self.lastconnlist = tk.Listbox(self.Labelframe1)
        self.lastconnlist.place(relx=0.064, rely=0.149, relheight=0.771
                                , relwidth=0.832, bordermode='ignore')
        self.lastconnlist.configure(background="white")
        self.lastconnlist.configure(cursor="xterm")
        self.lastconnlist.configure(disabledforeground="#a3a3a3")
        self.lastconnlist.configure(font="TkFixedFont")
        self.lastconnlist.configure(foreground="#000000")
        self.lastconnlist.configure(highlightbackground="#d9d9d9")
        self.lastconnlist.configure(highlightcolor="black")
        self.lastconnlist.configure(selectbackground="#c4c4c4")
        self.lastconnlist.configure(selectforeground="black")

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.491, rely=0.204, relheight=0.29)
        self.TSeparator1.configure(orient="vertical")

        self.Labelframe2 = tk.LabelFrame(top)
        self.Labelframe2.place(relx=0.622, rely=0.512, relheight=0.456
                               , relwidth=0.283)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''friends''')
        self.Labelframe2.configure(background="#d9d9d9")
        self.Labelframe2.configure(highlightbackground="#d9d9d9")
        self.Labelframe2.configure(highlightcolor="black")

        self.friendslist = ScrolledListBox(self.Labelframe2)
        self.friendslist.place(relx=0.069, rely=0.144, relheight=0.756
                               , relwidth=0.873, bordermode='ignore')
        self.friendslist.configure(background="white")
        self.friendslist.configure(cursor="xterm")
        self.friendslist.configure(disabledforeground="#a3a3a3")
        self.friendslist.configure(font="TkFixedFont")
        self.friendslist.configure(foreground="black")
        self.friendslist.configure(highlightbackground="#d9d9d9")
        self.friendslist.configure(highlightcolor="#d9d9d9")
        self.friendslist.configure(selectbackground="#c4c4c4")
        self.friendslist.configure(selectforeground="black")

        self.Labelframe3 = tk.LabelFrame(top)
        self.Labelframe3.place(relx=0.524, rely=0.34, relheight=0.136
                               , relwidth=0.25)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(foreground="black")
        self.Labelframe3.configure(text='''User's code''')
        self.Labelframe3.configure(background="#d9d9d9")
        self.Labelframe3.configure(highlightbackground="#d9d9d9")
        self.Labelframe3.configure(highlightcolor="black")

        self.codetxt = tk.Entry(self.Labelframe3)
        self.codetxt.place(relx=0.131, rely=0.333, height=30, relwidth=0.745
                           , bordermode='ignore')
        self.codetxt.configure(background="white")
        self.codetxt.configure(disabledforeground="#a3a3a3")
        self.codetxt.configure(font="TkFixedFont")
        self.codetxt.configure(foreground="#000000")
        self.codetxt.configure(highlightbackground="#d9d9d9")
        self.codetxt.configure(highlightcolor="black")
        self.codetxt.configure(insertbackground="black")
        self.codetxt.configure(selectbackground="#c4c4c4")
        self.codetxt.configure(selectforeground="black")
        self.codetxt.configure(state="disabled")

        self.connbutton = tk.Button(top)
        self.connbutton.place(relx=0.409, rely=0.558, height=54, width=107)
        self.connbutton.configure(activebackground="#ececec")
        self.connbutton.configure(activeforeground="#000000")
        self.connbutton.configure(background="#00a6ff")
        self.connbutton.configure(cursor="hand2")
        self.connbutton.configure(disabledforeground="#a3a3a3")
        self.connbutton.configure(font="-family {Arial Black} -size 12 -weight bold")
        self.connbutton.configure(foreground="#e9e9e9")
        self.connbutton.configure(highlightbackground="#d9d9d9")
        self.connbutton.configure(highlightcolor="black")
        self.connbutton.configure(pady="0")
        self.connbutton.configure(text='''CONNECT''')
        self.connbutton.configure(command=mainpage_support.connect)

        self.Labelframe4 = tk.LabelFrame(top)
        self.Labelframe4.place(relx=0.213, rely=0.34, relheight=0.136
                               , relwidth=0.25)
        self.Labelframe4.configure(relief='groove')
        self.Labelframe4.configure(foreground="black")
        self.Labelframe4.configure(text='''Your code''')
        self.Labelframe4.configure(background="#d9d9d9")
        self.Labelframe4.configure(highlightbackground="#d9d9d9")
        self.Labelframe4.configure(highlightcolor="black")

        self.selfcode = tk.Label(self.Labelframe4)
        self.selfcode.place(relx=0.131, rely=0.333, height=31, width=114
                            , bordermode='ignore')
        self.selfcode.configure(background="#d9d9d9")
        self.selfcode.configure(cursor="xterm")
        self.selfcode.configure(disabledforeground="#d9d9d9")
        self.selfcode.configure(font=font10)
        self.selfcode.configure(foreground="#487efd")
        self.selfcode.configure(text=code)


# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped


class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

    def size_(self):
        sz = tk.Listbox.size(self)
        return sz


import platform


def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))


def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')


def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')


def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
