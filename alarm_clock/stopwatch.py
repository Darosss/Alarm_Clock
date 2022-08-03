from tkinter import PhotoImage, ttk
import tkinter as tk


class StopwatchProperties:
    IMAGE_NAME = 'stopwatch.png'


class Stopwatch(tk.Frame):
    def __init__(self, root, app_properties, json_conf, json_alarms, *args, **kwargs):
        self._root = root
        self.app_prop = app_properties
        self.json_conf = json_conf
        self.json_alarms = json_alarms
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.btn_big = PhotoImage(file=f'{self.app_prop.IMAGES_DIR}/{StopwatchProperties.IMAGE_NAME}')
        self.btn_width_no_height = self.btn_big.subsample(1,2)

        self.stopwatch_frame = None
        self.saved_frame = None
        self.str_start = "Start"
        self.str_resume = "Resume"
        self.str_pause = "Pause"
        self.stop = "Stop"
        self.counting_interval = None
        self.stopwatch_time = [0, 0, 0, 0, 0]
        self.count_saved_times = 1
        self.create_stopwatch_frame(self)


    def create_stopwatch_frame(self, append):
        self.stopwatch_frame = tk.Frame(append, borderwidth=5, background=self.json_conf["bg_stopwatch"], relief='sunken')
        self.saved_frame = tk.Frame(append, borderwidth=5, background=self.json_conf["bg_stopwatch"], relief='sunken')

      
        saved_times_title = ttk.Label(self.saved_frame, text='Saved times', compound='center', image=self.btn_big, background=self.json_conf["bg_stopwatch"], foreground=self.json_conf['fg_stopwatch'], font=('default', 25),padding=20)
        saved_times = ttk.Label(self.saved_frame, text='',  background=self.json_conf["bg_stopwatch"], foreground=self.json_conf['fg_stopwatch'], font=('default', 25),padding=20)

        ttk.Label(self.stopwatch_frame, text='Stopwatch', compound='center', image=self.btn_big, background=self.json_conf["bg_stopwatch"], foreground=self.json_conf['fg_stopwatch'],  font=('default', 25),padding=20).pack()
        time_label = ttk.Label(self.stopwatch_frame, padding=20, compound='center', image=self.btn_big, background=self.json_conf["bg_stopwatch"], foreground=self.json_conf['fg_stopwatch'],  font=('default', 25), text='Stopwatch')

        stop = tk.Button(self.stopwatch_frame, compound='center', highlightthickness = 0, bd = 0,image=self.btn_width_no_height, background=self.json_conf["bg_stopwatch"], foreground=self.json_conf['fg_stopwatch'],activebackground=self.json_conf["bg_stopwatch"], activeforeground=self.json_conf['fg_stopwatch'], name=f"{self.stop.lower()}", text=self.stop)
        start_pause = tk.Button(self.stopwatch_frame, compound='center',highlightthickness = 0, bd = 0, image=self.btn_width_no_height, background=self.json_conf["bg_stopwatch"], foreground=self.json_conf['fg_stopwatch'],activebackground=self.json_conf["bg_stopwatch"], activeforeground=self.json_conf['fg_stopwatch'], name=f"{self.str_start.lower()}/{self.str_pause.lower()}",
                                 text=self.str_start)
        start_pause.config(command=lambda lbl=time_label, btn=start_pause, stp=stop: self.toggle_start_pause(btn, lbl, stp))
        stop.config(command=lambda lbl=time_label, btn=stop, sp=start_pause, save=saved_times: self.stop_stopwatch(btn, sp, lbl, save))

        self.stopwatch_frame.pack(side='right', expand=True, fill='both')
        self.saved_frame.pack(side='left', expand=True, fill='both')
        time_label.pack(expand=True)
        start_pause.pack(side='top', fill='both')
        saved_times_title.pack(expand=True)
        saved_times.pack(expand=True)

    def toggle_start_pause(self, btn, watch_label, stop_btn, stop=False):
        if stop:
            self.countdown_time(watch_label) 
            btn.config(text=self.str_start)
            return
        if btn['text'] == self.str_start:
            btn.config(text=self.str_pause)
            self.countdown_time(watch_label, True)
            stop_btn.pack(side='top', fill='both')
            return
        elif btn['text'] == self.str_pause:
            btn.config(text=self.str_resume)
            self.countdown_time(watch_label)
        elif btn['text'] == self.str_resume:

            btn.config(text=self.str_pause)
            self.countdown_time(watch_label, True)


    def stop_stopwatch(self, stop, start_pause_button, watch_label, save):
        
        save.config(text=f"{save['text']}\n{self.count_saved_times}: {self.format_time_array()}")
        self.count_saved_times += 1
        self.toggle_start_pause(start_pause_button, watch_label, stop, True)
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
            time_lbl.after_cancel(self.counting_interval)
            return

        def time():
            time_lbl.config(text=self.format_time_array())
            self.counting_interval = time_lbl.after(1, time)
            self.stopwatch_time[4] = self.stopwatch_time[4] + 1
        time()

