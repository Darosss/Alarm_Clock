import functools
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from datetime import timedelta


class Stopwatch:
    def __init__(self, config, style):
        self.stopwatch_frame = None
        self.saved_frame = None
        self.styleName = style
        self.str_start = "Start"
        self.str_pause = "Pause"
        self.stop = "Stop"
        self.is_counting = None
        self.stopwatch_time = [0, 0, 0, 0, 0]
        self.count_saved_times = 1

    def create_stopwatch_frame(self, append):
        self.stopwatch_frame = ttk.Frame(append, style=self.styleName, borderwidth=15, relief='sunken')
        self.saved_frame = ttk.Frame(append, style=self.styleName, borderwidth=15, relief='sunken')

        saved_times_title = ttk.Label(self.saved_frame, text='Saved times', font=('default', 25),padding=20)
        saved_times = ttk.Label(self.saved_frame, text='', font=('default', 25),padding=20)

        ttk.Label(self.stopwatch_frame, text='Stopwatch', font=('default', 25),padding=20).pack()
        time_label = ttk.Label(self.stopwatch_frame, padding=20, font=('default', 25), text='Stopwatch')


        stop = ttk.Button(self.stopwatch_frame, name=f"{self.stop.lower()}", text=self.stop)
        start_pause = ttk.Button(self.stopwatch_frame, name=f"{self.str_start.lower()}/{self.str_pause.lower()}",
                                 text=self.str_start)

        start_pause.config(command=lambda lbl=time_label, btn=start_pause, stp=stop: self.toggle_start_pause(btn, lbl, stp))
        stop.config(command=lambda lbl=time_label, btn=stop, sp=start_pause, save=saved_times: self.stop_stopwatch(btn, sp, lbl, save))

        self.stopwatch_frame.pack(side='right', expand=True)
        self.saved_frame.pack(side='left', expand=True)
        time_label.pack(expand=True)
        start_pause.pack(side='left')
        saved_times_title.pack(expand=True)
        saved_times.pack(expand=True)

    def toggle_start_pause(self, btn, watch_label, stop_btn):
        if btn['text'] == self.str_start:
            btn.config(text=self.str_pause)
            self.countdown_time(watch_label, True)
            stop_btn.pack(side='right')
            return
        btn.config(text=self.str_start)
        self.countdown_time(watch_label)

    def stop_stopwatch(self, stop, sp, watch_label, save):
        save.config(text=f"{save['text']}\n{self.count_saved_times}: {self.format_time_array()}")
        self.count_saved_times += 1
        self.toggle_start_pause(sp, watch_label, stop)
        self.stopwatch_time = [0] * len(self.stopwatch_time)
        stop.pack_forget()

    def format_time_array(self):
        # 0 - days, 1 - hours, 2 - minutes, 3 - seconds, 4 miliseconds
        # its just for now, for look how it;ll look and maybe i'll change this
        def check_condition(where, what):
            if self.stopwatch_time[where] > what:
                self.stopwatch_time[where - 1] += 1
                self.stopwatch_time[where] = 0

        check_condition(4, 999)
        check_condition(3, 59)
        check_condition(2, 59)
        check_condition(1, 23)
        days = self.stopwatch_time[0]
        hours = self.stopwatch_time[1]
        minutes = self.stopwatch_time[2]
        seconds = self.stopwatch_time[3]
        ms = self.stopwatch_time[4]
        text_to_show = f"{days}:{hours}:{minutes}:{seconds}:{ms}"
        return text_to_show

    def countdown_time(self, time_lbl, start=False):
        if not start:
            time_lbl.after_cancel(self.is_counting)
            return

        def time():
            time_lbl.config(text=self.format_time_array())
            self.is_counting = time_lbl.after(1, time)
            self.stopwatch_time[4] = self.stopwatch_time[4] + 1
        time()

