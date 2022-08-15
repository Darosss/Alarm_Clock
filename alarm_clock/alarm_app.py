from operator import index
import tkinter as tk
from tkinter import PhotoImage, ttk
from datetime import datetime
from config import *
from alarms import Alarms
from stopwatch import Stopwatch
from timer import Timer
from my_widgets import MyButton, MyLabel
# Alarm clock that I wanted to create based on android alam clock but for windows
# Prototype ver 1.0 Kappa
# It's first interract with tkinter

class ConfigProperties:
    CONFIG_NAME = 'config.json'
    ALARMS_CNF_NAME = 'alarms.json'
    SOUNDS_DIR = 'sounds'
    APP_SETTINGS = 'app_settings'
    MENU_OPTIONS = 'menu_options'
    ALARMS_OPTIONS = 'alarms_options'
    ALARMS_LIST = 'alarms_list'
    STOPWATCH_OPTIONS = 'stopwatch_options'
    TIMER_OPTIONS = 'timer_options'
    FOOTER_OPTIONS = 'footer_options'

class AppProperties:
    IMAGES_DIR = 'imgs'
    SOUND_DIR = 'sounds'
    SOUNDS_EXT = ".mp3"
    MENU_IMG = 'menu.png'
    TIMER_IMG = 'timer.png'
    SETTINGS_IMG = 'settings.png'

class AlarmApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.json_conf = ConfigJSON(ConfigProperties.CONFIG_NAME)
        self.json_conf_section = self.json_conf.section
        self.json_alarms = ConfigJSON(ConfigProperties.ALARMS_CNF_NAME)
        self.geometry(self.json_conf_section[ConfigProperties.APP_SETTINGS]["resolution"]["value"])
        self._alarm_app_frame = Alarms(self, AppProperties, self.json_conf_section[ConfigProperties.ALARMS_OPTIONS], self.json_alarms)
        self._stopwatch_app_frame = Stopwatch(self, AppProperties, self.json_conf_section[ConfigProperties.STOPWATCH_OPTIONS], self.json_alarms)
        self._timer_app_frame = Timer(self, AppProperties, self.json_conf_section[ConfigProperties.TIMER_OPTIONS], self.json_alarms)
       

        self._menu = MainMenu(self)
        self._footer_frame = FooterFrame(self, self.json_conf_section[ConfigProperties.FOOTER_OPTIONS])

        self._menu_frame = MenuFrame(self, self.json_conf_section[ConfigProperties.MENU_OPTIONS], 
                                     self._alarm_app_frame, 
                                     self._stopwatch_app_frame, 
                                     self._timer_app_frame
                                    )                                    
        
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=6)
        self.rowconfigure(2, weight=1)
        self.show_frame(self._alarm_app_frame)

        self._footer_frame.grid(column=0, row=2, columnspan=2, sticky="nsew")
        self._menu_frame.grid(column=0, row=0, columnspan=2, sticky="nsew")

    def show_frame(self, show_what):
        show_what.grid(column=0, row=1, columnspan=2, sticky="nsew")

    def upload_file(self):
        print('upload')
      
    def menu_settings(self):
        pass
        SettingsWindow(self.json_conf)
    def quit_app(self):
        self.quit()


class SettingsWindow(tk.Tk):
    #TODO scrolable
    def __init__(self, json_conf, *args, **kwargs):
        self.json_conf = json_conf
        self.fg = json_conf.section[ConfigProperties.APP_SETTINGS]['fg_settings']["value"]
        self.bg = json_conf.section[ConfigProperties.APP_SETTINGS]['bg_settings']["value"]
        self.resolution = json_conf.section[ConfigProperties.APP_SETTINGS]['resolution_settings']["value"]
        self.font_size =  json_conf.section[ConfigProperties.APP_SETTINGS]['settings_font_size']["value"]
        tk.Toplevel.__init__(self, background=self.bg,  *args, **kwargs)
        self.setting_frame = tk.Frame(self, background="green")
        self.setting_frame.pack(side="top", fill="both")
        my_canvas = tk.Canvas(self.setting_frame)
        
        myscrollbar=ttk.Scrollbar(self.setting_frame, orient="vertical", command=my_canvas.yview)
        #myscrollbar.grid(column=3, row=0, rowspan=10, sticky="nw")
        myscrollbar.pack(side="right", fill="y")
        my_canvas.configure(yscrollcommand=myscrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
        
        self.second_frame = tk.Frame(my_canvas)
        my_canvas.create_window((0,0), window=self.second_frame, anchor="nw")
        my_canvas.pack(side="left", fill="both", expand=1)
        
        #TODO DO SCROLL BETTER  ENDEND LAST TIME 9:05
        self.geometry(self.resolution)
        self.title('Settings')
        self.btn_big = PhotoImage(file=f'{AppProperties.IMAGES_DIR}/{AppProperties.SETTINGS_IMG}')
        self.img_section = self.btn_big.subsample(2,2)
        self.img_description = self.btn_big.subsample(1,2)
        for col in range(3): self.columnconfigure(col, weight=1)

        save_btn = MyButton(self.second_frame, 'Save', 
                                self.fg, self.bg, 
                                image=self.btn_big, 
                                name='save_sett_btn'
                              )
        #save_btn.grid(column=2, row=0)
        save_btn.pack(side="right")
        save_btn.config(command = lambda : self.save_settings())
        
        for section in self.json_conf.section:
            self.add_header_label(section)
            for index, subsect in enumerate(self.json_conf.section[section]):
                
                self.add_setting(self.json_conf.section[section][subsect]["description"], 
                                section, subsect, 
                                self.json_conf.section[section][subsect]["value"], 
                                index)

    def save_settings(self):
        
        for slave in self.grid_slaves():
            if slave.widgetName == 'entry':
                option_value = slave.get()
                if option_value.isdigit():
                    option_value = int(option_value)
                sect_and_key = slave.winfo_name().split("/")
                self.json_conf.modify_settings(sect_and_key[0], sect_and_key[1], option_value)
                 
    def add_header_label(self, header_name):
        row_grid = self.grid_size()[1] + 1
        MyLabel(self.second_frame, header_name,
            self.fg, self.bg,
            image=self.img_section,
            font=("default", self.font_size*2),
            ).pack(side="top")#.grid(column=0, columnspan=2, row = row_grid, sticky="e") 
       
    def add_setting(self, sett_descr, section_name, option_name, value, row, width=20):
        row_grid = self.grid_size()[1] + row
        MyLabel(self.second_frame, sett_descr,
            self.fg, self.bg,
            image=self.img_description,
            font=("default", self.font_size),
            ).pack(side="top")#.grid(column=0, row = row_grid, sticky="nse")
        res_entry = tk.Entry(self.second_frame, width=width, 
                    font=("default", self.font_size),
                    background=self.bg,
                    foreground=self.fg,
                    name = f"{section_name}/{option_name}"
                    )
        res_entry.insert(0, value)
        res_entry.pack(side="top")#grid(column = 1, row = row_grid, sticky="nsew")

  #settigns soon  

class MainMenu(tk.Menu):
    @property
    def root(self):
        return self._root

    def __init__(self, root, *args, **kwargs):
        tk.Menu.__init__(self, root, *args, **kwargs)
        self._root = root
        window_menu = WindowMenu(self, tearoff=0)
        self.add_cascade(label="Options", menu=window_menu)
        root.config(menu = self)


class WindowMenu(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)
        
        self.add_command(label="Upload", command=parent.root.upload_file)
        self.add_command(label="Settings", command=parent.root.menu_settings)
        self.add_command(label="Exit", command=parent.root.quit_app)

class MenuFrame(tk.Frame):
    def __init__(self, root, config_sett, alarm_frame, stopwatch_frame, timer_frame, *args, **kwargs):
        self._root = root
        self.img_menu = PhotoImage(file=f"{AppProperties.IMAGES_DIR}/{AppProperties.MENU_IMG}")

        self.config_sett = config_sett
        self.bg_menu = self.config_sett['menu_bg']["value"]
        self.fg_menu = self.config_sett['menu_fg']["value"]
        tk.Frame.__init__(self, root, background=self.bg_menu, borderwidth=1, relief='raised', *args, **kwargs)
        menu_btn_alarms= MyButton(self, 'Alarms', 
                                self.fg_menu, self.bg_menu, 
                                image=self.img_menu, 
                                name="alarms_menu_btn"
                                )
        menu_btn_stopwatch= MyButton(self, 'Stopwatch', 
                                self.fg_menu, self.bg_menu, 
                                image=self.img_menu, 
                                name="stopwatch_menu_btn"
                                )
        menu_btn_timer= MyButton(self, 'Timer', 
                                self.fg_menu, self.bg_menu, 
                                image=self.img_menu, 
                                name="timer_menu_btn"
                                )
        menu_btn_alarms.config(command=lambda f=alarm_frame: self.clear_and_show_clicked(f))
        menu_btn_stopwatch.config(command=lambda f=stopwatch_frame: self.clear_and_show_clicked(f))
        menu_btn_timer.config(command=lambda f=timer_frame: self.clear_and_show_clicked(f))

        menu_btn_alarms.pack(side='left', expand=True)
        menu_btn_stopwatch.pack(side='left', expand=True)
        menu_btn_timer.pack(side='left', expand=True)
        
    def clear_and_show_clicked(self, what, col_grid=0, row_grid=1, colspan=2, stick='nsew'):
        for slave in self._root.grid_slaves(row=1, column=0):
            slave.grid_forget()
            slave.grid_remove()
        what.grid(column=col_grid, row=row_grid, columnspan=colspan, sticky=stick)


class FooterFrame(tk.Frame):
    def __init__(self, root, config_sett, *args, **kwargs):
        self._root = root
        self.config_sett = config_sett
        self.bg_footer = self.config_sett['footer_bg']["value"]
        self.fg_footer = self.config_sett["footer_fg"]["value"] 
        self.img_timer = PhotoImage(file=f"{AppProperties.IMAGES_DIR}/{AppProperties.TIMER_IMG}")
        
        tk.Frame.__init__(self, root, background=self.bg_footer, borderwidth=1, relief='sunken', *args, **kwargs)
        self.time_label = tk.Label(self,
                                justify='center',
                                font=('calibri', 25, 'bold'),
                                image = self.img_timer,
                                compound='center',
                                background=self.bg_footer, 
                                foreground=self.fg_footer,
                                activebackground=self.fg_footer, 
                                )
        self.time()

        self.time_label.grid(column=0, row=0, sticky='nsew')
        self.columnconfigure(0, weight =1)
        

    def time(self):
        time_now = datetime.now().strftime("%H:%M:%S")
        self.time_label['text'] = time_now
        self.time_label.after(1000, self.time)