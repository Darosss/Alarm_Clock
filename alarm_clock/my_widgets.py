import tkinter as tk


class MyButton(tk.Button):
    def __init__(self, master, text, fg='black', bg='white', **options):
        tk.Button.__init__(
                            self, master, 
                            text = text,
                            highlightthickness = 0, bd = 0, 
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
                            text = text,
                            foreground=fg,
                            background=bg,
                            compound='center',
                            **options
             )