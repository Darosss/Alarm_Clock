from multiprocessing.sharedctypes import Value
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from datetime import timedelta
class Timer(tk.Frame):
    def __init__(self, root, json_conf, json_alarms, *args, **kwargs):
        self._root = root
        self.json_conf = json_conf
        self.json_alarms = json_alarms
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.stopwatch_frame = None
        self.timer_frame = None    
          
        self.str_start = "Start"
        self.str_resume = "Resume"
        self.str_pause = "Pause"
        self.stop = "Stop"
        self.is_counting = None
        self.timer_time = [0, 0, 0, 0, 0]
        self.count_saved_times = 1
        self.create_timer_frame(self)

    def create_timer_frame(self, append):
        self.timer_frame = tk.Frame(append, borderwidth=15, relief='sunken')
        self.timer_frame.pack(side='right', expand=True, fill="both")

        self.saved_frame = tk.Frame(append, borderwidth=15, relief='sunken')
        self.saved_frame.pack(side='left', expand=True, fill="both")

        ttk.Label(self.saved_frame, text='Saved times', background=self.json_conf['s_t_title_bg'], font=('default', 25),padding=20).pack(expand=True)
        saved_times = ttk.Label(self.saved_frame, text='', background=self.json_conf["s_t_bg"], font=('default', 25),padding=20)

        
        
        ttk.Label(self.timer_frame, text='Timer', background=self.json_conf["time_title_bg"],  font=('default', 25),padding=20).pack(side="top", fill='both')
        
        time_entry = ttk.Entry(self.timer_frame, background=self.json_conf["time_bg"],  font=('default', 25))
        time_entry.insert(1, ':'.join(str(x) for x in self.timer_time))

        stop = tk.Button(self.timer_frame, background=self.json_conf["btns_bg"], activebackground=self.json_conf["btns_bg_active"], text=self.stop)
        start_pause = tk.Button(self.timer_frame, background=self.json_conf["btns_bg"], activebackground=self.json_conf["btns_bg_active"], text=self.str_start)

        start_pause.config(command=lambda tim_entr=time_entry, btn=start_pause, stp=stop: self.toggle_start_pause(btn, tim_entr, stp))
        stop.config(command=lambda tim_entr=time_entry, btn=stop, sp=start_pause: self.stop_timer(btn, sp, tim_entr))
        
        time_entry.pack(expand=True)
        start_pause.pack(side='top', fill="both")
        saved_times.pack(fill="both")

    def toggle_start_pause(self, btn, entry_timer, stop_btn, stop=False):
        if stop:
            self.countdown_time(entry_timer) 
            btn.config(text=self.str_start)
            return
        if btn['text'] == self.str_start:
            if sum(int(w) for w in entry_timer.get().split(":")) > 0:
                self.timer_time = entry_timer.get().split(":")
                self.timer_time = list(map(int, self.timer_time))
                
                # change this later is a mess kappa
                btn.config(text=self.str_pause)
                self.countdown_time(entry_timer, True)
                stop_btn.pack(side='top', fill="both")
                return
        elif btn['text'] == self.str_pause:
            btn.config(text=self.str_resume)
            self.countdown_time(entry_timer)
        elif btn['text'] == self.str_resume:
            btn.config(text=self.str_pause)
            self.countdown_time(entry_timer, True)

    def stop_timer(self, stop, sp, entry_timer):
        entry_timer.delete(0, 'end')
        self.timer_time = [0] * len(self.timer_time)
        self.toggle_start_pause(sp, entry_timer, stop, True)
        entry_timer.insert(1, ':'.join(str(x) for x in self.timer_time))
        stop.pack_forget()

    def countdown_time(self, time_entry, start=False):
        def time():
            # print(self.format_time_array())
            time_entry.delete(0, 'end')
            time_entry.insert(1, self.format_time_array())
            if sum(int(w) for w in time_entry.get().split(":")) > 0:
                self.is_counting = time_entry.after(1, time)
                self.timer_time[4] = self.timer_time[4] - 1
                return
        if not start:
            time_entry.after_cancel(self.is_counting)
            return
            
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