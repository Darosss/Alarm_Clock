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

    def create_scrollbar(self):
        pass
    # menu: stopwatch, egg timer, alarms
    def create_menu_app(self):
        def create_menu_button(text, bg, bgactive, frame):
            btn = tk.Button(self.menu_frame, text=text, 
                            background=bg, activebackground=bgactive, 
                            width=40,
                            command=lambda f=frame: self.clear_and_show_clicked(f)
                            )
            return btn
        
        menu_btn_bg = self.config.get_key("app_setting", "menu_btn_bg")
        menu_btn_bg_active = self.config.get_key("app_setting", "menu_btn_bg_active")

        self.menu_frame = ttk.Frame(self, style=self.styleName, name="menu", borderwidth=15, relief="sunken")

        menu_btn_alarms = create_menu_button("Alarms", menu_btn_bg, menu_btn_bg_active, self.alarm_app_frame)   
        menu_btn_stopwatch = create_menu_button("Stopwatch", menu_btn_bg, menu_btn_bg_active, self.stopwatch_app_frame)
        menu_btn_timer = create_menu_button("Timer", menu_btn_bg, menu_btn_bg_active, self.timer_app_frame)                                                  
        
        menu_btn_alarms.pack(side='left', expand=True)
        menu_btn_stopwatch.pack(side='left', expand=True)
        menu_btn_timer.pack(side='left', expand=True)
        # pack to self.menu.frame
        self.menu_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")
        # grid app
        return self.menu_frame

    def clear_and_show_clicked(self, what):
        # print(what)
        for slave in self.grid_slaves(row=1, column=0):
            # print(slave)
            slave.grid_forget()
            slave.grid_remove()
        # print(what.grid_slaves())
        what.grid(column=0, row=1, columnspan=2, sticky="nsew")

    def create_footer_app(self):
        def time():
            time_now = datetime.now().strftime("%H:%M:%S")
            time_label.config(text=time_now)
            time_label.after(1000, time)

        self.footer_frame = ttk.Frame(self, style=self.styleName, name='footer', borderwidth=15, relief="groove")
        self.footer_frame .columnconfigure(0, weight=1)
        time_label = ttk.Label(self.footer_frame, justify='center',
                               font=('calibri', 25, 'bold'), borderwidth=1, relief="solid")
        
        button_setting = ttk.Button(self.footer_frame, text="SETTINGS")
        button_setting.config(command=self.setting_window_popup)
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
                    new_key = self.config.get_key(sect_and_key[0], sect_and_key[1], True)
                    new_key = new_key.replace(new_key.split("#")[0], slave.get())
                    self.config.save_config(sect_and_key[0], sect_and_key[1], new_key) 
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
        top.geometry("750x250")
        top.title('Settings')
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)


        save_btn = ttk.Button(top, text="Save")
        save_btn.grid(column=2, row=0)
        save_btn.config(command = lambda : save_settings())
        
        
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
        alarms = Alarms(self, self.config_name, 'sounds', self.styleName , day_names, self.snoozed_time)
        alarms_list = alarms.create_frames_for_alarm(self.alarm_app_frame)
        alarms.set_alarms()
        return self.alarm_app_frame

    def create_stopwatch_app(self):
        self.stopwatch_app_frame = ttk.Frame(self, style=self.styleName, name='stopwatch_app')
        self.stopwatch_app_frame.columnconfigure(0, weight=1)
        self.stopwatch_app_frame.columnconfigure(1, weight=1)
        self.stopwatch_app_frame.rowconfigure(0, weight=1)

        stopwatch = Stopwatch(self.config_name, self.styleName)
        stopwatch.create_stopwatch_frame(self.stopwatch_app_frame)

        return self.stopwatch_app_frame

    def create_timer_app(self):
        self.timer_app_frame = ttk.Frame(self, style=self.styleName, name='timer_app')
        self.timer_app_frame.columnconfigure(0, weight=1)
        self.timer_app_frame.columnconfigure(1, weight=1)
        self.timer_app_frame.rowconfigure(0, weight=1)

        timer = Timer(self.config_name, self.styleName)
        timer.create_timer_frame(self.timer_app_frame)

        return self.timer_app_frame

    def show_app(self, show_what):
        show_what.grid(column=0, row=1, columnspan=2, sticky="nsew")