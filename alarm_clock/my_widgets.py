from textwrap import wrap
import tkinter as tk
from tkinter import ttk
# TODO My widgets = checkbox


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
            wraplength=200,
            **options
        )


class MyLabel(tk.Label):
    def __init__(self, master, text, fg='black', bg='white', wraplength=200, **options):
        tk.Label.__init__(
            self, master,
            text=text,
            foreground=fg,
            background=bg,
            compound='center',
            wraplength=wraplength,
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


class MyOptionMenu(tk.Frame):
    def __init__(self, master, fg='black', bg='white', title='', title_img='',
                 font='default', font_size='10', img_option='', value='', *values,
                 ** options):
        tk.Frame.__init__(
            self, master,
            background=bg
        )
        if len(title) > 0:
            self.title = MyLabel(self, title, fg, bg,
                                 image=title_img
                                 )
            self.title.pack(expand=True, fill='x')
        s = ttk.Style()
        s.configure(
            "my.TMenubutton",
            font=(font, font_size),
            image=img_option,
            background=bg,
            foreground=fg,
            compound=tk.CENTER,
            wraplength=200
        )
        self.option_menu = ttk.OptionMenu(
            self,
            value,
            "",
            *values,
            style="my.TMenubutton",
        )
        self.option_menu.pack()


class MyScrollableFrame(ttk.Frame):
    def __init__(self, container, bg='white', fg='black', * args, **kwargs):
        super().__init__(container, *args, **kwargs)
        style = ttk.Style()
        style.theme_use('classic')
        style.configure("Vertical.TScrollbar", background=bg,
                        troughcolor=bg, bordercolor=bg, foreground=fg)
        style.map('Vertical.TScrollbar', background=[('active', fg)])
        canvas = tk.Canvas(self, bg=bg, bd=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self, orient="vertical",
            command=canvas.yview)
        self.frame = tk.Frame(canvas, background=bg)

        self.frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
