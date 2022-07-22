import tkinter as tk
from tkinter import ttk
from datetime import datetime
from config import Config
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
        self.config_name = "config.ini"
        self.config = Config(config_name)
        self.style = ttk.Style()
        self.styleName = "new.TFrame"
        self.style.configure(self.styleName, background=self.read_config("app_setting", "style_background")) #from user
        self.geometry(self.read_config("app_setting", "resolution"))
        self.snoozed_time = int(self.read_config("alarms_settings", "snooze_time")) #from user
        self.menu_frame = None
        self.alarm_app_frame = None
        self.stopwatch_app_frame = None
        self.timer_app_frame = None
        self.footer_frame = None
        
    #function for read config.ini(self, config_select?, key, if true check alarms)
    def read_config(self, section_name, option_name):
        config_obj = configparser.ConfigParser()
        config_obj.read("config.ini") 
        return config_obj[section_name][option_name]

    def save_config(self, section_name, key_name, value):
        config_obj = configparser.ConfigParser()
        config_obj.read("config.ini")
        config_obj.set(section_name, key_name, value)
        with open('config.ini', 'w') as configfile:
            config_obj.write(configfile)

    # create scrollbar for more than x alarms
    def create_scrollbar(self):
        pass
    
    # menu: stopwatch, egg timer, alarms
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


    def clear_and_show_clicked(self, what):
        for slave in self.grid_slaves(row=1, column=0):
            print(slave)
            slave.grid_forget()
            slave.grid_remove()
        print(what.grid_slaves())
        what.grid(column=0, row=1, columnspan=2, sticky="nsew")

    def create_footer_app(self):
        self.footer_frame = ttk.Frame(self, style=self.styleName, name='footer')
        self.footer_frame['borderwidth'] = 15
        self.footer_frame['relief'] = 'groove'
        self.footer_frame .columnconfigure(0, weight=1)
        time_label = ttk.Label(self.footer_frame, justify='center',
                               font=('calibri', 25, 'bold'), borderwidth=1, relief="solid")
        time_label.grid(column=2, row=0, sticky='nsew')

        button_setting = ttk.Button(self.footer_frame, text="SETTINGS")
        button_setting.config(command=self.setting_window_popup)
        button_setting.grid(column=0, row=0, sticky="nsw")

        def time():
            time_now = datetime.now().strftime("%H:%M:%S")
            time_label.config(text=time_now)
            time_label.after(1000, time)
        # watch this will be changed for down timer or upper i mean for every other application
        time()

        self.footer_frame.grid(column=0, row=2, columnspan=2, sticky="nsew")

        return self.footer_frame

    def setting_window_popup(self):
        pass
    #     def save_settings():
    #         print(top.grid_slaves())
    #         for slave in top.grid_slaves():
    #             if slave.widgetName == 'entry':
    #                 self.save_config('alarms_config_preferences', slave.winfo_name(), slave.get())

    #     def add_setting(append, sett_name, option_conf, row, width=20):
    #         ttk.Label(append, text=sett_name).grid(column=0, row = row)
    #         res_entry = tk.Entry(append, width=width, name=option_conf)
    #         res_entry.insert(0, self.read_config('alarms_config_preferences',option_conf))
    #         res_entry.grid(column = 1, row = row)

    #     top = tk.Toplevel(self)
    #     top.columnconfigure(0, weight=1)
    #     top.columnconfigure(1, weight=1)
    #     top.columnconfigure(2, weight=1)


    #     save_btn = ttk.Button(top, text="Save")
    #     save_btn.grid(column=2, row=0)
    #     save_btn.config(command = lambda: save_settings())
    #     top.geometry("750x250")
    #     top.title('Settings')

    #     add_setting(top, "Resolution", 'resolution', 0)
    #     add_setting(top, "Names of day", 'day_name', 1, 40)
    #     add_setting(top, "Snooze time(min)", 'snooze_time', 2)
    #     add_setting(top, "Background color", 'style_background', 3)

    #     add_setting(top, "Select sound font size", 's_snd_font_size', 4)
    #     add_setting(top, "Select sound background color", 's_snd_bg', 5)

    #     add_setting(top, "Save button font size", 'save_btn_font_size', 6)
    #     add_setting(top, "Save button background color", 'save_btn_bg', 7)

    #     add_setting(top, "Entry hours background color", 'hours_entry_font_size', 8)
    #     add_setting(top, "Entry hours background color", 'hours_entry_bg', 9)
        
    #     add_setting(top, "Head label font size", 'alarm_label_font_size', 10)
    #     add_setting(top, "Head label background color", 'alarm_label_bg', 11)

    #     add_setting(top, "Day check boxes background color", 'check_box_bg', 12)
    
    #     # that's mess but i'll autoamte this later rather
    def create_alarm_app(self):
        day_names = []
        for day in self.read_config("alarms_settings", "day_name").split(","):
            day_names.append(day)
        
        self.alarm_app_frame = ttk.Frame(self, style=self.styleName, name='alarm_app')
        # self.alarm_app_frame.grid(column=0, row=1, columnspan=2, sticky="nsew")
        self.alarm_app_frame.columnconfigure(0, weight=1)
        self.alarm_app_frame.columnconfigure(1, weight=1)
        self.alarm_app_frame.rowconfigure(0, weight=1)
        alarms = Alarms(self, "config.ini", 'sounds', self.styleName , day_names, self.snoozed_time)
        alarms_list = alarms.create_frames_for_alarm(self.alarm_app_frame)
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
