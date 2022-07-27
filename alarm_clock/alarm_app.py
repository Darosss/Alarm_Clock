import tkinter as tk
from tkinter import ttk
from datetime import datetime
from config import Config
from alarms import Alarms
from stopwatch import Stopwatch
from timer import Timer
# Alarm clock that I wanted to create based on android alam clock but for windows
# Prototype ver 1.0 Kappa


class AlarmApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.config_name = "config.ini"
        self.config_ini = Config(self.config_name)

        self.geometry(self.config_ini.get_key("app_setting", "resolution"))
        self.styleName = "new.TFrame"
        self.style = ttk.Style().configure(self.styleName, background=self.config_ini.get_key("app_setting", "style_background"))

        self._alarm_app_frame = AlarmsFrame(self)
        self._stopwatch_app_frame = StopwatchFrame(self)
        self._timer_app_frame = TimerFrame(self)
        
        self._menu = MainMenu(self)
        self._menu_frame = MenuFrame(self, self._alarm_app_frame, self._stopwatch_app_frame, self._timer_app_frame)
        self._footer_frame = FooterFrame(self)

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=6)
        self.rowconfigure(2, weight=1)
        # self.create_footer_app()
        # self.create_menu_app()
        self.show_frame(self._alarm_app_frame)

    def show_frame(self, show_what):
        show_what.grid(column=0, row=1, columnspan=2, sticky="nsew")

    def upload_file(self):
        print('upload')
      
    def menu_settings(self):
        window = SettingsWindow(self, self.config_ini)

    def quit_app(self):
        print('quit')


class SettingsWindow(tk.Tk):
    def __init__(self, root, config_settings, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.config_sett = config_settings
        self.geometry("750x250")
        self.title('Settings')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        save_btn = ttk.Button(self, text="Save")
        save_btn.grid(column=2, row=0)
        save_btn.config(command = lambda : self.save_settings())
        
        for section in self.config_sett.get_all_sections():
            if not section[0] == "_":
                self.write_config_settings(section)
        
    def save_settings(self):
        for slave in self.grid_slaves():
            if slave.widgetName == 'entry':
                sect_and_key = slave.winfo_name().split("/")
                new_key = self.config_sett.get_key(sect_and_key[0], sect_and_key[1], True)
                new_key = new_key.replace(new_key.split("#")[0], slave.get())
                self.config_sett.save_config(sect_and_key[0], sect_and_key[1], new_key) 
    def add_header_label(self, header_name):
        row_grid = self.grid_size()[1] + 1
        ttk.Label(self, text=header_name, justify='center', background="lightblue").grid(column=0, columnspan=2, row = row_grid, sticky="e")

    def add_setting(self, sett_descr, section_name, option_name, row, width=20):
        row_grid = self.grid_size()[1] + row
        ttk.Label(self, text=sett_descr, background="lightblue").grid(column=0, row = row_grid, sticky="nse")
        res_entry = tk.Entry(self, width=width, name=f"{section_name}/{option_name}")
        res_entry.insert(0, self.config_sett.get_key(section_name, option_name))
        res_entry.grid(column = 1, row = row_grid, sticky="nsew")

    def write_config_settings(self, section_name):
        alarms_appearance = self.config_sett.get_sections_keys(section_name, False)
        self.add_header_label(section_name)
        for index, sett in enumerate(alarms_appearance):
            sett_split = sett.split("/")
            sett_key_name = sett_split[0]
            sett_descrip = sett_split[1].split("#")[1]
            self.add_setting(sett_descrip, section_name, sett_key_name, index)
    
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
    """Creates Window menu."""
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)
        
        self.add_command(label="Upload", command=parent.root.upload_file)
        self.add_command(label="Settings", command=parent.root.menu_settings)
        self.add_command(label="Exit", command=parent.root.quit_app)


class AlarmsFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, *args, **kwargs)
        alarms = Alarms(self, 'config.ini', 'new.TFrame')
        alarms.create_frames_for_alarm(self)
        alarms.set_alarms()


class StopwatchFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, *args, **kwargs)
        stopwatch = Stopwatch('config.ini', 'new.TFrame')
        stopwatch.create_stopwatch_frame(self)
        

class TimerFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, *args, **kwargs)
        timer = Timer('config.ini', 'new.TFrame')
        timer.create_timer_frame(self)


class MenuFrame(tk.Frame):
    def __init__(self, root, alarm_frame, stopwatch_frame, timer_frame, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, *args, **kwargs)
        # menu_btn_bg = self.config_ini.get_key("app_setting", "menu_btn_bg")
        # menu_btn_bg_active = self.config_ini.get_key("app_setting", "menu_btn_bg_active")

        menu_btn_alarms = self.create_menu_button("Alarms", '', '', alarm_frame)   
        menu_btn_stopwatch = self.create_menu_button("Stopwatch", '', '', stopwatch_frame)
        menu_btn_timer = self.create_menu_button("Timer", '', '', timer_frame)                                                  
        
        menu_btn_alarms.pack(side='left', expand=True)
        menu_btn_stopwatch.pack(side='left', expand=True)
        menu_btn_timer.pack(side='left', expand=True)
        # pack to self.menu.frame
        self.grid(column=0, row=0, columnspan=2, sticky="nsew")

    def create_menu_button(self, text, bg, bgactive, frame):
        btn = tk.Button(self, text=text, 
                        # background=bg, activebackground=bgactive, 
                        width=40,
                        command=lambda f=frame: self.clear_and_show_clicked(f)
                        )
        return btn
    def clear_and_show_clicked(self, what, col_grid=0, row_grid=1, colspan=2, stick='nsew'):
        for slave in self._root.grid_slaves(row=1, column=0):
            slave.grid_forget()
            slave.grid_remove()
        what.grid(column=col_grid, row=row_grid, columnspan=colspan, sticky=stick)

class FooterFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        tk.Frame.__init__(self, root, background='blue', *args, **kwargs)
        self.time_label = ttk.Label(self, justify='center',
                               font=('calibri', 25, 'bold'), borderwidth=1, relief="solid")
        self.time()

        self.time_label.grid(column=2, row=0, sticky='nsew')
        self.grid(column=0, row=2, columnspan=2, sticky="nsew")

    def time(self):
        time_now = datetime.now().strftime("%H:%M:%S")
        self.time_label['text'] = time_now
        self.time_label.after(1000, self.time)