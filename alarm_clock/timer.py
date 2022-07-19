from tkinter import ttk
import tkinter as tk
from datetime import datetime
from datetime import timedelta


class Timer:
    def __init__(self, config, style):
        self.timer_frame = None
        self.styleName = style  

    def create_timer_frame(self, append):
        self.timer_frame = ttk.Frame(append, style=self.styleName, borderwidth=15, relief='sunken')
        self.timer_frame.pack(expand=True)
        ttk.Label(self.timer_frame, text='Timer').pack()
        ttk.Label(self.timer_frame, text='Timer').pack()
        ttk.Label(self.timer_frame, text='Timer').pack()

    def set_timer(self):
        pass

    def start_timer(self):
        pass

    def pause_timer(self):
        pass
