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
            **options
        )
        self.option_menu = ttk.OptionMenu(
            self,
            value,
            "",
            *values,
            style="my.TMenubutton",
        )
        self.option_menu.pack()


class MyScrollableFrame(tk.Frame):
    def __init__(self, container, bg='white', orient='vertical', * args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self, bg=bg, bd=0, highlightthickness=0)
        # scrollbar = ttk.Scrollbar(
        #     self, orient=orient)
        scrollbar = AutoScrollbar(self)
        if orient == 'vertical':
            scrollbar.config(command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
        else:
            scrollbar.config(command=canvas.xview)
            canvas.configure(xscrollcommand=scrollbar.set)

        self.frame = tk.Frame(canvas, background=bg)

        self.frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        canvas.pack(side="left", fill="both", expand=True)


class AutoScrollbar(tk.Scrollbar):
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.tk.call("pack", "forget", self)
        else:
            self.pack(side=tk.RIGHT, fill="y")
        tk.Scrollbar.set(self, low, high)
