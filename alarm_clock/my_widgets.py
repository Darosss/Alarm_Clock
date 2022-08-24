import tkinter as tk
from turtle import back


class MyButton(tk.Button):
    def __init__(self, master, text, fg='black', bg='white', **options):
        tk.Button.__init__(
            self, master,
            text=text,
            highlightthickness=0, bd=0,
            foreground=fg,
            activeforeground=fg,
            background=bg,
            activebackground=bg,
            compound='center',
            **options
        )


class MyLabel(tk.Label):
    def __init__(self, master, text, fg='black', bg='white', **options):
        tk.Label.__init__(
            self, master,
            text=text,
            foreground=fg,
            background=bg,
            compound='center',
            **options
        )


class MyEntry(tk.Frame):
    def __init__(self, master, fg='black', bg='white', title='', title_img='', value_entr='', ** options):
        tk.Frame.__init__(
            self, master,
            background=bg
        )
        if len(title) > 0:
            self.title = MyLabel(self, title, fg, bg,
                                 image=title_img
                                 )
            self.title.pack(expand=True, fill='x')

        self.entry = tk.Entry(
            self,
            foreground=fg,
            background=bg,
            **options
        )
        self.entry.insert(0, value_entr)
        self.entry.pack()
