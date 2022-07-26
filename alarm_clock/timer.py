from multiprocessing.sharedctypes import Value
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from datetime import timedelta

from config import Config


class Timer:
    def __init__(self, config_name, style):
        self.config_name = config_name
        self.section_name = 'timer_appearance'
        self.config = Config(config_name)
        self.stopwatch_frame = None
        self.timer_frame = None      
        self.str_start = "Start"
        self.str_pause = "Pause"
        self.stop = "Stop"
        self.is_counting = None
        self.timer_time = [0, 0, 0, 0, 0]
        self.styleName = style  
        self.count_saved_times = 1

    def get_config_key(self, key_name):
        return self.config.get_key(self.section_name, key_name)
    
    def create_timer_frame(self, append):
        self.timer_frame = ttk.Frame(append, style=self.styleName, borderwidth=15, relief='sunken')
        self.timer_frame.pack(expand=True)
        self.timer_frame = ttk.Frame(append, style=self.styleName, borderwidth=15, relief='sunken')
        self.saved_frame = ttk.Frame(append, style=self.styleName, borderwidth=15, relief='sunken')

        s_t_title_bg = self.get_config_key("s_t_title_bg")
        s_t_bg = self.get_config_key("s_t_bg")
        saved_times_title = ttk.Label(self.saved_frame, text='Saved times', background=s_t_title_bg, font=('default', 25),padding=20)
        saved_times = ttk.Label(self.saved_frame, text='', background=s_t_bg, font=('default', 25),padding=20)

        time_title_bg = self.get_config_key("time_title_bg")
        time_bg = self.get_config_key("time_bg")
        ttk.Label(self.timer_frame, text='Timer', background=time_title_bg,  font=('default', 25),padding=20).pack()
        # time_entry = ttk.Label(self.timer_frame, padding=20, background=time_bg,  font=('default', 25), text='Timerr')
        time_entry = ttk.Entry(self.timer_frame, background=time_bg,  font=('default', 25), text='Timerr')
        time_entry.insert(1, ':'.join(str(x) for x in self.timer_time))

        btns_bg = self.get_config_key("btns_bg")
        btns_bg_active = self.get_config_key("btns_bg_active")
        stop = tk.Button(self.timer_frame, background=btns_bg, activebackground=btns_bg_active, text=self.stop)
        start_pause = tk.Button(self.timer_frame, background=btns_bg, activebackground=btns_bg_active, text=self.str_start)

        start_pause.config(command=lambda tim_entr=time_entry, btn=start_pause, stp=stop: self.toggle_start_pause(btn, tim_entr, stp))
        stop.config(command=lambda tim_entr=time_entry, btn=stop, sp=start_pause: self.stop_timer(btn, sp, tim_entr))

        self.timer_frame.pack(side='right', expand=True)
        self.saved_frame.pack(side='left', expand=True)
        time_entry.pack(expand=True)
        start_pause.pack(side='left')
        saved_times_title.pack(expand=True)
        saved_times.pack(expand=True)

    def toggle_start_pause(self, btn, entry_timer, stop_btn):
        if btn['text'] == self.str_start:
            if sum(int(w) for w in entry_timer.get().split(":")) > 0:
                self.timer_time = entry_timer.get().split(":")
                self.timer_time = list(map(int, self.timer_time))
                # change this later is a mess kappa
                btn.config(text=self.str_pause)
                self.countdown_time(entry_timer, True)
                stop_btn.pack(side='right')
                return
        else:
            btn.config(text=self.str_start)
            self.countdown_time(entry_timer)

    def stop_timer(self, stop, sp, entry_timer):
        self.toggle_start_pause(sp, entry_timer, stop)
        entry_timer.delete(0, 'end')
        self.timer_time = [0] * len(self.timer_time)
        
        entry_timer.insert(1, ':'.join(str(x) for x in self.timer_time))

        stop.pack_forget()

    def countdown_time(self, time_entry, start=False):
        if not start:
            time_entry.after_cancel(self.is_counting)
            return

        def time():
            # print(self.format_time_array())
            time_entry.delete(0, 'end')
            time_entry.insert(1, self.format_time_array())
            self.is_counting = time_entry.after(1, time)
            self.timer_time[4] = self.timer_time[4] - 1
        time()

    def format_time_array(self):
        # 0 - days, 1 - hours, 2 - minutes, 3 - seconds, 4 miliseconds
        # its just for now, for look how it;ll look and maybe i'll change this
        def check_condition(where, what):

            if self.timer_time[where] < 0:
                self.timer_time[where - 1] -= 1
                self.timer_time[where] = what

        check_condition(4, 999)
        check_condition(3, 59)
        check_condition(2, 59)
        check_condition(1, 23)
        days = self.timer_time[0]
        hours = self.timer_time[1]
        minutes = self.timer_time[2]
        seconds = self.timer_time[3]
        ms = self.timer_time[4]
        text_to_show = f"{days}:{hours}:{minutes}:{seconds}:{ms}"
        return text_to_show