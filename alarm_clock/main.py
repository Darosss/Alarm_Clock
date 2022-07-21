import multiprocessing
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from turtle import bgcolor
from playsound import playsound
from alarms import Alarms
from stopwatch import Stopwatch
from timer import Timer
import configparser
# Alarm clock that I wanted to create based on android alam clock but for windows
# Prototype ver 1.0 Kappa


class AlarmApp(tk.Tk):
    def __init__(self, height, width, title):
        super().__init__()
        self.title(title)
        self.style = ttk.Style()
        self.styleName = "new.TFrame"
        self.style.configure(self.styleName, background=self.read_config("alarms_app_style", "style_background")) #from user
        self.geometry(self.read_config("alarms_config_preferences", "resolution"))
        self.update_idletasks()
        self.snoozed_time = int(self.read_config("alarms_config_preferences", "snooze_time")) #from user
        self.menu_frame = None
        self.alarm_app_frame = None
        self.stopwatch_app_frame = None
        self.timer_app_frame = None
        self.footer_frame = None
        print(self.read_config("list_alarms", "", True))

    def read_config(self, config_name, option_name, alarms=False):
        config_obj = configparser.ConfigParser()
        config_obj.read("config.ini")
        alarms_list = []
        if alarms:
            for key in config_obj[config_name]:
                alarms_list.append(config_obj[config_name][key].replace("#","\n"))
            return alarms_list     
        
        return config_obj[config_name][option_name]

    def create_scrollbar(self):
        pass
    # create scrollbar for more than x alarms

    def create_menu_app(self):
        self.menu_frame = ttk.Frame(self, style=self.styleName, name="menu")
        self.menu_frame['borderwidth'] = 15
        self.menu_frame['relief'] = 'groove'
        menu_btn_alarms = tk.Button(self.menu_frame, text='Alarms', width=40,
                                    command=lambda: self.clear_and_show_clicked(self.alarm_app_frame)
                                    ).pack(side='left', expand=True)

        menu_btn_stopwatch = tk.Button(self.menu_frame, text='Stopwatch', width=40,
                                       command=lambda: self.clear_and_show_clicked(self.stopwatch_app_frame)
                                       ).pack(side='left', expand=True)
        menu_btn_timer = tk.Button(self.menu_frame, text='Timer', width=40,
                                   command=lambda: self.clear_and_show_clicked(self.timer_app_frame)
                                                                               ).pack(side='left', expand=True)

        self.menu_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")
        return self.menu_frame
    # menu: stopwatch, egg timer, alarms

    def clear_and_show_clicked(self, what):
        for slave in self.grid_slaves(row=1, column=0):
            print(slave)
            slave.grid_forget()
            slave.grid_remove()
        print(what.grid_slaves())
        what.grid(column=0, row=1, columnspan=2, sticky="nsew")
        # self.show_app(what)

    def create_footer_app(self):
        self.footer_frame = ttk.Frame(self, style=self.styleName, name='footer')
        self.footer_frame['borderwidth'] = 15
        self.footer_frame['relief'] = 'groove'
        self.footer_frame .columnconfigure(0, weight=1)
        time_label = ttk.Label(self.footer_frame, justify='center',
                               font=('calibri', 25, 'bold'), borderwidth=1, relief="solid")
        time_label.grid(column=2, row=0, sticky='nsew')

        def time():
            time_now = datetime.now().strftime("%H:%M:%S")
            time_label.config(text=time_now)
            time_label.after(1000, time)
        # watch this will be changed for down timer or upper i mean for every other application
        time()

        self.footer_frame.grid(column=0, row=2, columnspan=2, sticky="nsew")

        return self.footer_frame

    def create_alarm_app(self):
        alarm_config = self.read_config("list_alarms", "", True)
        day_names = []
        for day in self.read_config("alarms_config_preferences", "day_name").split(","):
            day_names.append(day)
        
        self.alarm_app_frame = ttk.Frame(self, style=self.styleName, name='alarm_app')
        # self.alarm_app_frame.grid(column=0, row=1, columnspan=2, sticky="nsew")
        self.alarm_app_frame.columnconfigure(0, weight=1)
        self.alarm_app_frame.columnconfigure(1, weight=1)
        self.alarm_app_frame.rowconfigure(0, weight=1)
        alarms = Alarms(self, alarm_config, self.styleName , day_names, self.snoozed_time)
        alarms_list = alarms.create_frames_for_alarm(self.alarm_app_frame, 'sounds\\3.mp3', 5)
        alarms.set_alarms()
        return self.alarm_app_frame

    def create_stopwatch_app(self, config):
        self.stopwatch_app_frame = ttk.Frame(self, style=self.styleName, name='stopwatch_app')
        self.stopwatch_app_frame.columnconfigure(0, weight=1)
        self.stopwatch_app_frame.columnconfigure(1, weight=1)
        self.stopwatch_app_frame.rowconfigure(0, weight=1)

        stopwatch = Stopwatch(config, self.styleName)
        stopwatch.create_stopwatch_frame(self.stopwatch_app_frame)

        return self.stopwatch_app_frame

    def create_timer_app(self, config):
        self.timer_app_frame = ttk.Frame(self, style=self.styleName, name='timer_app')
        self.timer_app_frame.columnconfigure(0, weight=1)
        self.timer_app_frame.columnconfigure(1, weight=1)
        self.timer_app_frame.rowconfigure(0, weight=1)

        timer = Timer(config, self.styleName)
        timer.create_timer_frame(self.timer_app_frame)

        return self.timer_app_frame



    def show_app(self, show_what):
        show_what.grid(column=0, row=1, columnspan=2, sticky="nsew")

def run_program():
    app = AlarmApp(1000, 800, 'Alarm Clock')
    # create alarm app(width, height, title name) Soon i'll create resizable and dynamical boxes,
    # for now its just static i guess
    app.columnconfigure(0, weight=3)
    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=6)
    app.rowconfigure(2, weight=1)
    # alarm.rowconfigure(0, weight=1) jesli wieksze menu

    menu = app.create_menu_app()
    footer = app.create_footer_app()

    # menu grid append
    alarms = app.create_alarm_app()
    stopwatch = app.create_stopwatch_app(None)
    timer = app.create_timer_app(None)
    app.show_app(alarms)
    app.mainloop()


if __name__ == "__main__":
    run_program()
