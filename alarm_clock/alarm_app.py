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
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.config_name = "config.ini"
        self.config = Config(self.config_name)
        self.style = ttk.Style()
        self.styleName = "new.TFrame"
        self.style.configure(self.styleName, background=self.config.get_key("app_setting", "style_background")) #from user
        self.geometry(self.config.get_key("app_setting", "resolution"))
        self.snoozed_time = int(self.config.get_key("alarms_settings", "snooze_time")) #from user
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
        self.footer_frame = ttk.Frame(self, style=self.styleName, name='footer', borderwidth=15, relief="groove")
        self.footer_frame .columnconfigure(0, weight=1)
        time_label = ttk.Label(self.footer_frame, justify='center',
                               font=('calibri', 25, 'bold'), borderwidth=1, relief="solid")
        
        button_setting = ttk.Button(self.footer_frame, text="SETTINGS")
        button_setting.config(command=self.setting_window_popup)
        

        def time():
            time_now = datetime.now().strftime("%H:%M:%S")
            time_label.config(text=time_now)
            time_label.after(1000, time)
        # watch this will be changed for down timer or upper i mean for every other application
        time()

        button_setting.grid(column=0, row=0, sticky="nsw")
        time_label.grid(column=2, row=0, sticky='nsew')
        self.footer_frame.grid(column=0, row=2, columnspan=2, sticky="nsew")

        return self.footer_frame

    def setting_window_popup(self):
        def save_settings():
            for slave in top.grid_slaves():
                if slave.widgetName == 'entry':
                    sect_and_key = slave.winfo_name().split("/")
                    self.config.save_config(sect_and_key[0], sect_and_key[1], slave.get())
        def add_header_label(header_name):
            row_grid = top.grid_size()[1] + 1
            ttk.Label(top, text=header_name, justify='center', background="lightblue").grid(column=0, columnspan=2, row = row_grid, sticky="e")

        def add_setting(sett_descr, section_name, option_name, row, width=20):
            row_grid = top.grid_size()[1] + row
            ttk.Label(top, text=sett_descr, background="lightblue").grid(column=0, row = row_grid, sticky="nse")
            res_entry = tk.Entry(top, width=width, name=f"{section_name}/{option_name}")
            res_entry.insert(0, self.config.get_key(section_name, option_name))
            res_entry.grid(column = 1, row = row_grid, sticky="nsew")

        def write_config_settings(section_name):
            alarms_appearance = self.config.get_sections_keys(section_name, False)
            add_header_label(section_name)
            for index, sett in enumerate(alarms_appearance):
                sett_split = sett.split("/")
                sett_key_name = sett_split[0]
                sett_descrip = sett_split[1].split("#")[1]
                add_setting(sett_descrip, section_name, sett_key_name, index)
                
        top = tk.Toplevel(self)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)


        save_btn = ttk.Button(top, text="Save")
        save_btn.grid(column=2, row=0)
        save_btn.config(command = lambda : save_settings())
        top.geometry("750x250")
        top.title('Settings')
        
        write_config_settings("app_setting")
        write_config_settings("alarms_settings")
        write_config_settings("alarms_appearance")

        
    def create_alarm_app(self):
        day_names = []
        for day in self.config.get_key("alarms_settings", "day_name").split(","):
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