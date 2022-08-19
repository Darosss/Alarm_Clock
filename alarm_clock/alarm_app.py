import tkinter as tk
from tkinter import PhotoImage, ttk
from datetime import datetime, timedelta
from config import ConfigJSON
from my_widgets import MyButton, MyLabel
from playsound import playsound
import multiprocessing
import glob2 as glob
import pkg_resources
from threading import Timer as tim

pkg_resources.require("playsound==1.2.2")
# Alarm clock that I wanted to create based on android alam clock but for windows
# Prototype ver 1.0 Kappa
# It's first interract with tkinter

class ConfigProperties:
    CONFIG = ConfigJSON('config.json')
    ALARMS = ConfigJSON('alarms.json')
    SAVED_TIMES = ConfigJSON('saved_times.json')
    TIME = 'time'
    DAYS = 'days'
    SOUND = 'sound'
    STATE = 'state'
    SNOOZE_TIME = 'snooze_time'
    DESCR = 'description'
    APP_SETTINGS = CONFIG.section['app_settings']
    MENU_OPTIONS = CONFIG.section['menu_options']
    ALARMS_OPTIONS = CONFIG.section['alarms_options']
    STOPWATCH_OPTIONS = CONFIG.section['stopwatch_options']
    TIMER_OPTIONS = CONFIG.section['timer_options']
    FOOTER_OPTIONS = CONFIG.section['footer_options']

class AppProperties:
    IMAGES_DIR = ConfigProperties.APP_SETTINGS['images_dir']['value']
    SOUND_DIR = ConfigProperties.APP_SETTINGS['sounds_dir']['value']
    SOUNDS_EXT = f".{ConfigProperties.APP_SETTINGS['sounds_ext']['value']}"
    START_TXT = ConfigProperties.APP_SETTINGS['start_txt']['value']
    STOP_TXT = ConfigProperties.APP_SETTINGS['stop_txt']['value']
    PAUSE_TXT = ConfigProperties.APP_SETTINGS['pause_txt']['value']
    RESUME_TXT = ConfigProperties.APP_SETTINGS['resume_txt']['value']
    ALARMS_IMG = f'{IMAGES_DIR}/alarms.png'
    SETTINGS_IMG = f'{IMAGES_DIR}/settings.png'
    MENU_IMG = f'{IMAGES_DIR}/menu.png'
    FOOTER_TIMER_IMG = f'{IMAGES_DIR}/footer_timer.png'
    TIMER_IMG = f'{IMAGES_DIR}/timer.png'
    STOPWATCH_IMG = f'{IMAGES_DIR}/stopwatch.png'
    DELETE_STRING = 'X'
    ALARM_PREFIX = "alarm_box"


class AlarmApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.config_app = ConfigProperties.APP_SETTINGS
        self.geometry(self.config_app["resolution"]["value"])
        self._alarm_app_frame = Alarms(self)
        self._stopwatch_app_frame = Stopwatch(self)
        self._timer_app_frame = Timer(self)
        
        self._menu = MainMenu(self)
        self._footer_frame = FooterFrame(self)
        self._menu_frame = MenuFrame(self, 
                                     self._alarm_app_frame, 
                                     self._stopwatch_app_frame, 
                                     self._timer_app_frame
                                    )                                    
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        # --------------MENU-----------------
        # ALARMS | EDIT or STOPWATCH or TIMER
        # -------------FOOTER----------------

        self.show_frame(self._alarm_app_frame)

        self._footer_frame.grid(column=0, row=2, columnspan=2, sticky=tk.NSEW)
        self._menu_frame.grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)

    def show_frame(self, show_what):
        show_what.grid(column=0, row=1, columnspan=2, sticky=tk.NSEW)

    def upload_file(self):
        print('upload')
      
    def menu_settings(self):
        pass
        SettingsWindow()
    def quit_app(self):
        self.quit()


class SettingsWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.all_config = ConfigProperties.CONFIG
        self.all_sections = self.all_config.section
        self.config_sett = ConfigProperties.APP_SETTINGS
        self.fg = self.config_sett["fg_settings"]["value"]
        self.bg = self.config_sett["bg_settings"]["value"]
        self.resolution = self.config_sett["resolution_settings"]["value"]
        self.font_size =  self.config_sett["font_size_settings"]["value"]
        self.settings_font =  self.config_sett["font_family_settings"]["value"]
        tk.Toplevel.__init__(self, background=self.bg,  *args, **kwargs)
        self.head_frame = tk.Frame(self, background=self.bg)
        self.head_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        self.my_canvas = tk.Canvas(self.head_frame, background=self.bg)
        
        myscrollbar=ttk.Scrollbar(self.head_frame, orient=tk.VERTICAL, command=self.my_canvas.yview)
        #myscrollbar.grid(column=3, row=0, rowspan=10, sticky=tk.NW)
        myscrollbar.pack(side=tk.RIGHT, fill="y")
        self.my_canvas.configure(yscrollcommand=myscrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all")))
        
        self.settings_frame = tk.Frame(self.my_canvas, background=self.bg)
        self.my_canvas.create_window((0,0), window=self.settings_frame, anchor=tk.NW)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        
        self.geometry(self.resolution)
        self.title('Settings')
        self.btn_default = PhotoImage(file=AppProperties.SETTINGS_IMG)
        self.img_section = self.btn_default.subsample(2,2)
        self.img_description = self.btn_default.subsample(1,2)
        for col in range(3): self.columnconfigure(col, weight=1)

        save_btn = MyButton(self.settings_frame, 'Save', 
                                self.fg, self.bg, 
                                image=self.btn_default, 
                                name='save_sett_btn'
                              )
        save_btn.grid(column=2, row=0)
        # save_btn.pack(side=tk.TOP)
        save_btn.config(command = lambda sett_frame=self.settings_frame : self.save_settings(sett_frame))
        for i in range(3):
            self.settings_frame.columnconfigure(i, weight=1)
        
        for section in self.all_sections:
            self.add_header_label(section)
            for index, subsect in enumerate(self.all_sections[section]):
                
                self.add_setting(self.all_sections[section][subsect]["description"], 
                                section, subsect, 
                                self.all_sections[section][subsect]["value"], 
                                index)

    def save_settings(self, sett_frame):
        for slave in sett_frame.grid_slaves():
            print(slave)
            if slave.widgetName == 'entry':
                option_value = slave.get()
                if option_value.isdigit():
                    option_value = int(option_value)
                sect_and_key = slave.winfo_name().split("/")
                self.all_config.modify_settings(sect_and_key[0], sect_and_key[1], option_value)
                 
    def add_header_label(self, header_name):
        row_grid = self.settings_frame.grid_size()[1] + 1
        MyLabel(self.settings_frame, header_name,
            self.fg, self.bg,
            image=self.img_section,
            font=(self.settings_font, self.font_size*2),
            ).grid(column=0,row = row_grid, sticky="e") 
            #.pack(side=tk.TOP)#
            
       
    def add_setting(self, sett_descr, section_name, option_name, value, row, width=20):
        row_grid = self.settings_frame.grid_size()[1] + row
        MyLabel(self.settings_frame, sett_descr,
            self.fg, self.bg,
            image=self.img_description,
            font=(self.settings_font, self.font_size),
            ).grid(column=0, row = row_grid, sticky="nse")#.pack(side=tk.TOP)#
        res_entry = tk.Entry(self.settings_frame, width=width, 
                    font=(self.settings_font, self.font_size),
                    background=self.bg,
                    foreground=self.fg,
                    
                    name = f"{section_name}/{option_name}"
                    )
        res_entry.insert(0, value)
        res_entry.grid(column = 1, row = row_grid, sticky=tk.NSEW)#pack(side=tk.TOP)#

#FIXME Repair init function(make multiple functions from it)
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
    def __init__(self, root, alarm_frame, stopwatch_frame, timer_frame, *args, **kwargs):
        self._root = root
        self.img_menu = PhotoImage(file=AppProperties.MENU_IMG)
        self.config_menu = ConfigProperties.MENU_OPTIONS
        self.bg = self.config_menu['menu_bg']["value"]
        self.fg = self.config_menu['menu_fg']["value"]
        tk.Frame.__init__(self, root, background=self.bg, borderwidth=1, relief='raised', *args, **kwargs)
        menu_btn_alarms= MyButton(self, 'Alarms', self.fg, self.bg, 
                                image=self.img_menu, name="alarms_menu_btn")

        menu_btn_stopwatch= MyButton(self, 'Stopwatch', self.fg, self.bg, 
                                image=self.img_menu, name="stopwatch_menu_btn")

        menu_btn_timer= MyButton(self, 'Timer', self.fg, self.bg, 
                                image=self.img_menu,  name="timer_menu_btn")

        menu_btn_alarms.config(command=lambda f=alarm_frame: self.clear_and_show_clicked(f))
        menu_btn_stopwatch.config(command=lambda f=stopwatch_frame: self.clear_and_show_clicked(f))
        menu_btn_timer.config(command=lambda f=timer_frame: self.clear_and_show_clicked(f))

        menu_btn_alarms.pack(side=tk.LEFT, expand=True)
        menu_btn_stopwatch.pack(side=tk.LEFT, expand=True)
        menu_btn_timer.pack(side=tk.LEFT, expand=True)
        
    def clear_and_show_clicked(self, what, col_grid=0, row_grid=1, colspan=2):
        for slave in self._root.grid_slaves(row=1, column=0):
            slave.grid_forget()
            slave.grid_remove()
        what.grid(column=col_grid, row=row_grid, columnspan=colspan, sticky=tk.NSEW)


class FooterFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_footer = ConfigProperties.FOOTER_OPTIONS
        self.bg_footer = self.config_footer["footer_bg"]["value"]
        self.fg_footer = self.config_footer["footer_fg"]["value"]
        self.f_s_timer = self.config_footer["font_size_label"]["value"]
        self.font_timer = self.config_footer["font_label"]["value"]
        self.img_timer = PhotoImage(file=AppProperties.TIMER_IMG)
        
        tk.Frame.__init__(self, root, background=self.bg_footer, borderwidth=1, relief='sunken', *args, **kwargs)
        self.time_label = MyLabel(self,'', self.fg_footer, self.bg_footer, 
                                    image=self.img_timer,
                                    font=(self.font_timer, self.f_s_timer, 'bold') )
        self.time()

        self.time_label.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight =1)
        
    def time(self):
        time_now = datetime.now().strftime("%H:%M:%S")
        self.time_label['text'] = time_now
        self.time_label.after(1000, self.time)


class Alarms(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_alarm = ConfigProperties.ALARMS_OPTIONS
        self.alarms_list = ConfigProperties.ALARMS

        tk.Frame.__init__(self, root, *args, **kwargs)

        self.bg_alarms = self.config_alarm["bg_alarms"]["value"]
        self.fg_alarms = self.config_alarm["fg_buttons"]["value"]
        self.snooze_time = self.config_alarm["snooze_time"]["value"]
        
        self.edit_frame = self.EditAlarm(self)
        self.alarms_frame = tk.Frame(self, background = self.bg_alarms)
        self.alarms_frame.columnconfigure(0, weight=1)
        self.alarms_frame.columnconfigure(1, weight=1)
        
        #this should be in class Alarms -> alarmslist
        self.btn_default = PhotoImage(file=AppProperties.ALARMS_IMG)
        self.btn_subsampl52 = self.btn_default.subsample(5,2)
        self.small_widgets = self.btn_default.subsample(3,2)
        

        self.check_days = []
        self.snoozed_alarms = []
        self.snoozed_time = 1
        self.checked_days = []
        self.__create_alarm_boxes_frame()
        self.refresh_alarms()
        self.set_alarms()


        #this should be in class Alarms -> alarmslist
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.alarms_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.edit_frame.grid(row=0, column =1, sticky=tk.NSEW)
        self.config(background=self.bg_alarms)

    def __create_alarm_boxes_frame(self):
        alarm_title_lbl = MyLabel(self.alarms_frame, "Alarms",
                                self.fg_alarms, self.bg_alarms,
                                image=self.small_widgets,
                                )
        
        add_button =  MyButton(self.alarms_frame, 'Add', 
                                self.fg_alarms, self.bg_alarms, 
                                image=self.small_widgets, 
                                name='add_alarm_btn'
                              )

        add_button.config(command=lambda f=self.alarms_frame: self.add_alarm(f))
        alarm_title_lbl.grid(column=0, row=0, sticky=tk.NSEW)
        add_button.grid(column=1, row=0, padx=5, pady=1, sticky=tk.W)

    def refresh_alarms(self):
        self.alarms_frame.grid_slaves().clear()
        for row, alarm in enumerate(self.alarms_list.section): 
            self.create_alarm(self.alarms_frame, alarm, row)

    def toggle_alarm(self, alarm_box, alarm_text, alarm_json):
            state_now = ""
            if alarm_box[ConfigProperties.STATE] == 'disabled':
                state_now = 'normal'
            else:
                state_now = "disabled"
            alarm_box[ConfigProperties.STATE] = state_now
            alarm_text[ConfigProperties.STATE] = state_now
            self.alarms_list.modify_section(alarm_json, ConfigProperties.STATE, state_now)

    def create_alarm(self, append, alarm_json, row_alarm):
        alarm_text = self.alarms_list.section[alarm_json]

        alarm_format = f"{alarm_text[ConfigProperties.TIME]} \n {' '.join([str(elem) for elem in alarm_text[ConfigProperties.DAYS]])} \n {alarm_text[ConfigProperties.SOUND]} \n {alarm_text[ConfigProperties.SNOOZE_TIME]}"
        alarm_box = MyButton(append, alarm_format, 
                            self.fg_alarms, self.bg_alarms,
                            image=self.btn_default, 
                            name=f"{AppProperties.ALARM_PREFIX}_{row_alarm}"
                            )
        delete_alarm = MyButton(append, AppProperties.DELETE_STRING, 
                                self.fg_alarms, self.bg_alarms, 
                                image=self.btn_subsampl52, 
                                name=f"delete_{AppProperties.ALARM_PREFIX}{row_alarm}"
                                )
        
        alarm_box.config(state=alarm_text[ConfigProperties.STATE], command=lambda alarm_json=alarm_json, alarm_box=alarm_box: self.edit_frame.edit(alarm_json, alarm_box))
        delete_alarm.config(command=lambda alarm_json=alarm_json : [self.remove_alarm_box(alarm_json), alarm_box.destroy(), delete_alarm.destroy()])
        
        alarm_box.bind("<Button-3>", lambda event, alarm_box=alarm_box, alarm_text=alarm_text, alarm = alarm_json: self.toggle_alarm(alarm_box, alarm_text, alarm))
        
        alarm_box.grid(column=0, row=row_alarm + 2)
        delete_alarm.grid(column=1, row=row_alarm + 2, padx=5, pady=1, sticky=tk.W)
        return alarm_box

    def clear_edit_frame(self):
        for widgets in self.edit_frame.winfo_children():
            widgets.destroy()

    def remove_alarm_box(self, json_alarm):
            self.alarms_list.pop_section(json_alarm)
            self.clear_edit_frame()

    def add_alarm(self, frame):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today_name = now.strftime("%a")
        #FIXME for now its only day in engluish to need to change that
        row_alarm_box = frame.grid_size()[1]
        self.alarms_list.add_alarm(f"{AppProperties.ALARM_PREFIX}{row_alarm_box}", dt_string, [today_name], 'none', self.snooze_time, '')
        self.refresh_alarms()

    def check_alarms(self):
        alarms = []
        for alarm in self.alarms_frame.grid_slaves():
            if AppProperties.ALARM_PREFIX not in str(alarm):
                continue
            if alarm[ConfigProperties.STATE] == "normal":
                al = alarm['text'].split("\n")
                alarms.append(al)
        for snoozed_alarm in self.snoozed_alarms:
            al = snoozed_alarm.split("\n")
            alarms.append(al)
        return alarms
    # check which alarm is enabled

    def set_alarms(self):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today = now.strftime("%A")
        for alarm in self.alarms_list.section:
            alarm_prop = self.alarms_list.section[alarm]

            if alarm_prop['state'] == 'normal':
                if today[0:3] in  alarm_prop['days']:
                    
                    if dt_string in alarm_prop['time'] :
                        self.AlarmPopup(self, self.config_alarm, alarm_prop)
        self.alarms_frame.after(1000, self.set_alarms)

#TODO Changeing colors popup? Option for turn on or off
#TODO Snooze alarm
#TODO Volume of alarm
#TODO Random alarm from list? (could be done)
#TODO Alarm popup without exitic by windows
#TODO Settings(create dynamical buttons fe. App_option, menu_options) which will show options in menu for that section
#But it should be like that: even if button is clicked options doesnt dissapear they are just hidden for save all
#TODO Create default.json for default options?


    class AlarmPopup(tk.Tk):
        def __init__(self, root, config_prop, alarm_popup, *args, **kwargs):
            self.bg = config_prop["bg_alarm_popup"]["value"]
            self.fg = config_prop["fg_alarm_popup"]["value"]
            tk.Toplevel.__init__(self, background=self.bg, *args, **kwargs)
            self._root = root
            self.sound_process = None
            self.geometry(config_prop["alarm_popup_resolution"]["value"])
            self.title('Settings')
            self.mute_sound_txt = 'Mute sound'
            self.play_sound_txt = 'Play sound'
            self.snooze_alarm_txt = 'Snooze alarm'
            self.stop_alarm_txt = 'Stop alarm'
            self.img = PhotoImage(file=AppProperties.ALARMS_IMG)
            self.img_button = self.img.subsample(3,2)
            alarm_format = [alarm_popup[ConfigProperties.TIME],' '.join([str(day) for day in alarm_popup[ConfigProperties.DAYS]]), alarm_popup[ConfigProperties.SOUND], alarm_popup[ConfigProperties.DESCR]]
            for index, alarm_part in enumerate(alarm_format):
                MyLabel(self, alarm_part, self.fg, self.bg, image=self.img
                        ).pack(side=tk.TOP) 
            MyButton(self, self.stop_alarm_txt, self.fg, self.bg, image=self.img_button, 
                    name=f"stop_alarm", command= lambda: self.stop_alarm()
                    ).pack(side=tk.TOP)  
            MyButton(self, self.snooze_alarm_txt, self.fg, self.bg, image=self.img_button, 
                    name=f"snooze_alarm",
                    ).pack(side=tk.TOP)  
                 #TODO SNOOZE alarm
                 # #,command=lambda alarm=text: [snooze_alarm(), stop_alarm()]
            mute_sound_btn = MyButton(self, self.mute_sound_txt, 
                            self.fg, self.bg, 
                            image=self.img_button, 
                            name=f"mute_alarm",
                            )
            if AppProperties.SOUNDS_EXT in alarm_popup[ConfigProperties.SOUND]:
                music_to_play = f"{AppProperties.SOUND_DIR}/{alarm_popup[ConfigProperties.SOUND]}"
                mute_sound_btn.config(command=lambda mute_sound_btn=mute_sound_btn, music_to_play=music_to_play : self.mute_sound(mute_sound_btn, music_to_play))
                mute_sound_btn.pack(side=tk.TOP)
                self.start_sound(music_to_play)
            # if sounds != none  toggle music button and play music threading
        
        def stop_alarm(self):
            self.destroy()
            if self.sound_process != None:
                self.sound_process.kill()

        def mute_sound(self, btn, music_to_play):
            self.sound_process.kill()
            if btn['text'] ==  self.mute_sound_txt:
                btn['text'] = self.play_sound_txt 
                return
            self.start_sound(music_to_play)
            btn['text'] =  self.mute_sound_txt

        def snooze_alarm(self):
            snooze_time_now = datetime.now() + timedelta(minutes=1)
            time_string = snooze_time_now.strftime("%H:%M:%S")
            day_string = snooze_time_now.strftime("%a")
            snoozed_alarm_time = time_string + "\n" + day_string
            self.snoozed_alarms.append(snoozed_alarm_time)
            #FIXME Snooze_alarm should be repaired 

        def start_sound(self, sound):
            self.sound_process = multiprocessing.Process(target=playsound, args=(sound,))
            self.sound_process.start()

    class EditAlarm(tk.Frame):
        def __init__(self, root, *args, **kwargs):
            self._root = root
            self.img_edit = PhotoImage(file=AppProperties.ALARMS_IMG)
            self.img_check_day = self.img_edit.subsample(5,4)
            self.config_edit = ConfigProperties.ALARMS_OPTIONS
            self.alarms_list = ConfigProperties.ALARMS
            self.fg_edit = self.config_edit['fg_edit']["value"]
            self.bg_edit = self.config_edit['bg_edit']["value"]
            self.f_s_hours_entry = self.config_edit['hours_entry_font_size']["value"]
            self.f_s_select_snd = self.config_edit['select_sound_font_size']["value"]
            self.font_edit = self.config_edit['font_family_edit']["value"]
            tk.Frame.__init__(self, root, background=self.bg_edit, *args, **kwargs)


            self.check_days = None
            self.checked_days = None

        def edit(self, json_alarm, alarm_box):
            self.check_days = self._root.check_days
            self.checked_days = self._root.checked_days

            alarm_properties = self.alarms_list.section[json_alarm]
            alarm_format = alarm_properties
            alarm_description = alarm_properties["description"]
            alarm_format_lbl = f" {alarm_format[ConfigProperties.TIME]} \n {' '.join([str(elem) for elem in alarm_format[ConfigProperties.DAYS]])} \n {alarm_format[ConfigProperties.SOUND]}"

            def create_hours_entry(time):
                hours = tk.Entry(self, width=10, 
                                font=(self.font_edit, self.f_s_hours_entry), 
                                background=self.bg_edit,
                                foreground=self.fg_edit
                                )
                hours.insert(0, f"{time}")
                
                return hours

            def create_sound_list_from_dir():
                music_list = []
                for file in glob.glob(f"{AppProperties.SOUND_DIR}/*{AppProperties.SOUNDS_EXT}"):
                    #FIXME sounds = const?  
                    music_list.append(file)
                return music_list

            def create_sound_selection(sound):
                s = ttk.Style()
                
                s.configure('my.TMenubutton', font=(self.font_edit, 
                            self.f_s_select_snd), image=self.img_edit,
                            background=self.bg_edit, foreground=self.fg_edit,
                            compound=tk.CENTER,
                            )
                selected_snd = tk.StringVar()
                selected_snd.set(AppProperties.SOUND_DIR+'\\'+sound)
                choose_music = ttk.OptionMenu(self, selected_snd, "",*create_sound_list_from_dir(), style='my.TMenubutton')
                choose_music.grid(column=2, row=0, sticky=tk.NSEW)
                choose_music.config()
                return selected_snd
    
            def create_checkbox_days():
                day_names = self.config_edit['day_name']["value"].split(",")

                checkbox_days_frame = tk.Frame(self, bg=self.bg_edit)
                checkbox_days_frame.grid(row=5, column=0, columnspan=len(day_names), sticky=tk.NSEW)

                s_check_bx = ttk.Style()
                s_check_bx.configure('my.TCheckbutton', 
                                        image=self.img_check_day, 
                                        background=self.bg_edit,
                                        foreground=self.fg_edit
                                    )

                # save editing alarm button and add to grid
                self.check_days.clear()
                self.checked_days.clear()
                for indx, day in enumerate(day_names):
                    check_button_day = ttk.Checkbutton(checkbox_days_frame, compound=tk.CENTER, text=day, style='my.TCheckbutton')
                    if day[0:3] in alarm_format[ConfigProperties.DAYS]:
                        #FIXME should be first letter from config, but for now it is like this
                        self.checked_days.append(tk.IntVar(value = 1))
                        check_button_day.config(variable=self.checked_days[indx])
                    else:
                        self.checked_days.append(tk.IntVar(value = 0))
                    check_button_day.grid(row=0, column=indx, sticky=tk.W)
                    self.check_days.append(check_button_day)
                # this loop is creating each day of the week and add it to checkbutton in array and add to grid

            def save_alarm(alarm_json, alarm_box, hour, descr, snd_save):
                new_hour = hour.get()
                new_description = descr.get()
                new_days = []
                new_sound = snd_save.split('\\')[1]
                for day_check in self.check_days:
                    if 'selected' in day_check.state():
                        new_days.append(day_check['text'][0:3])
                        #FIXME 0:3 changed to dyunamical
                alarm_format = f"{new_hour} \n{' '.join([str(elem) for elem in new_days])}\n {new_sound}"
                alarm_box['text'] = alarm_format
                self.alarms_list.modify_alarm(alarm_json, new_hour, new_days, new_sound, new_description)

                # add hours and days to editing alarm
            
            def create_edit_appearance():
                hours_entry = create_hours_entry(alarm_format[ConfigProperties.TIME])
                hours_entry.grid(column=1, row=2, sticky=tk.NSEW)
                description_entry = create_hours_entry(alarm_description)
                description_entry.grid(column=1, row=1, sticky=tk.NSEW)
                MyLabel(self, alarm_format_lbl,
                            self.fg_edit, self.bg_edit,
                            image=self.img_edit
                            ).grid(column=1, row=0, sticky=tk.NS)   

                create_sound_list_from_dir()
                selected_snd = create_sound_selection(alarm_format[ConfigProperties.SOUND])
                
                save_btn = MyButton(self, "Save", 
                                    self.fg_edit, self.bg_edit, 
                                    image=self.img_edit, 
                                    name=f"save_alarm"
                                    )
                save_btn.config(command=lambda alarm_json=json_alarm, alarm_box=alarm_box, hour=hours_entry: save_alarm(alarm_json, alarm_box, hour, description_entry, selected_snd.get()))
                save_btn.grid(column=2, row=2, sticky=tk.NSEW)
                create_checkbox_days()
                return
            create_edit_appearance()
        #FIXME fix this lul create_edit_appearance

#TODO Timer description popup?
#FIXME coundown time = end? remove pause add restart etc
class Timer(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_timer = ConfigProperties.TIMER_OPTIONS
        self.bg_timer = self.config_timer['bg_timer']["value"]
        self.fg_timer = self.config_timer['fg_timer']["value"]
        self.f_s_timer = self.config_timer['font_size_timer']["value"]
        self.font_timer = self.config_timer['font_timer']["value"]
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.btn_default = PhotoImage(file=AppProperties.TIMER_IMG)
        self.low_height_widgets = self.btn_default.subsample(3,2)

        self.stopwatch_frame = None
        self.timer_frame = None    
          
        self.str_start = AppProperties.START_TXT
        self.str_resume = AppProperties.RESUME_TXT
        self.str_pause = AppProperties.PAUSE_TXT
        self.stop = AppProperties.STOP_TXT
        self.is_counting = None
        self.timer_time = [0, 0, 0, 0, 0]
        self.count_saved_times = 1

        self.create_timer_frame(self)

    def create_timer_frame(self, append):
        self.timer_frame = tk.Frame(append, borderwidth=1, background=self.bg_timer, relief='sunken')
        self.timer_frame.pack(side='right', expand=True, fill=tk.BOTH)

        self.saved_frame = tk.Frame(append, borderwidth=1, background=self.bg_timer, relief='sunken')
        self.saved_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


        saved_times_title_lbl = MyLabel(self.saved_frame, 'Saved times',
                            self.fg_timer, self.bg_timer,
                            image=self.btn_default,
                            font=(self.font_timer, self.f_s_timer)
                            )

        saved_times_lbl = MyLabel(self.saved_frame, '',
                            self.fg_timer, self.bg_timer,
                            font=(self.font_timer, self.f_s_timer)
                            )
        
        timer_lbl = MyLabel(self.timer_frame, 'Timer',
                            self.fg_timer, self.bg_timer,
                            image=self.btn_default,
                            font=(self.font_timer, self.f_s_timer)
                            )

        time_entry = tk.Entry(self.timer_frame, foreground=self.fg_timer, background=self.bg_timer,  font=(self.font_timer, self.f_s_timer))
        time_entry.insert(1, ':'.join(str(x) for x in self.timer_time))
    
        stop = MyButton(self.timer_frame, self.stop, 
                        self.fg_timer,  self.bg_timer,
                        image=self.low_height_widgets, 
                        name=self.stop.lower()
                        )
        start_pause = MyButton(self.timer_frame, self.str_start, 
                        self.fg_timer,  self.bg_timer,
                        image=self.low_height_widgets, 
                        name=f"{self.str_start.lower()}/{self.str_pause.lower()}"
                        )
        
        start_pause.config(command=lambda tim_entr=time_entry, btn=start_pause, stp=stop: self.toggle_start_pause(btn, tim_entr, stp))
        stop.config(command=lambda tim_entr=time_entry, btn=stop, sp=start_pause: self.stop_timer(btn, sp, tim_entr))

        timer_lbl.pack(side=tk.TOP, fill=tk.BOTH)
        time_entry.pack(expand=True)
        start_pause.pack(side=tk.TOP, fill=tk.BOTH)
        saved_times_title_lbl.pack(side=tk.TOP)
        saved_times_lbl.pack(fill=tk.BOTH)
       


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
                stop_btn.pack(side=tk.TOP, fill=tk.BOTH)
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

#TODO Saved times in json stopwatch/timer = saved_times.json
# "stopwatch_times":{
#   "time 'data': "{
#       value: "4:4:4"
#       description: "cos tam"  
#  }
# "timer_times":{
#   "time 'data': "{
#       value: "4:4:4"
#       description: "cos tam"  
#  }
#
#Descripion?

#TODO add delay start for stopwatch and timer
#TODO Add delete time from saved_time
class Stopwatch(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_stpwch = ConfigProperties.STOPWATCH_OPTIONS
        self.bg_stopwatch = self.config_stpwch["bg_stopwatch"]["value"]
        self.fg_stopwatch = self.config_stpwch["fg_stopwatch"]["value"]
        self.f_s_stopwatch = self.config_stpwch['font_size_stopwatch']["value"]
        self.font_stopwatch = self.config_stpwch['font_stopwatch']["value"]
        #FIXME dictionary config?
        self.saved_times = ConfigProperties.SAVED_TIMES

        tk.Frame.__init__(self, root, *args, **kwargs)

        self.btn_default = PhotoImage(file=AppProperties.STOPWATCH_IMG)
        self.low_height_widgets = self.btn_default.subsample(3,2)

        self.str_start = AppProperties.START_TXT
        self.str_resume = AppProperties.RESUME_TXT
        self.str_pause = AppProperties.PAUSE_TXT
        self.stop = AppProperties.STOP_TXT

        self.counting_interval = None
        self.stopwatch_time = [0, 0, 0, 0, 0]
        self.stopwatch_frame = tk.Frame(self, borderwidth=1, background=self.bg_stopwatch, relief='sunken')
        self.saved_frame = tk.Frame(self, borderwidth=1, background=self.bg_stopwatch, relief='sunken')
        for col in range(3):
            self.saved_frame.columnconfigure(col, weight=0)

        self.saved_times_date = None
        self.saved_times_time = None
        self.saved_times_descript = None

        self.timer = None

        self.stopwatch_frame.pack(side='right', expand=True, fill=tk.BOTH)
        self.saved_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.create_savedtimes_widgets()
        self.create_stopwatch_widgets()       
        self.refresh_saved_times()

    def refresh_saved_times(self):
        date = 'Date:\n'
        time = 'Time:\n'
        descript ='Description:\n'
        for index, section in enumerate(sorted(self.saved_times.section['stopwatch'], reverse=True)):
            date += f"{index+1}. {section}\n"
            time +=f"{self.saved_times.section['stopwatch'][section]['value']}\n"
            descript += f"{self.saved_times.section['stopwatch'][section]['description']}\n"

            self.saved_times_time['text'] = time
            self.saved_times_date['text'] = date
            self.saved_times_descript  ['text'] = descript

    def create_savedtimes_widgets(self):
        saved_times_title_lbl = MyLabel(self.saved_frame, 'Saved times',
                            self.fg_stopwatch, self.bg_stopwatch,
                            image=self.btn_default,
                            font=(self.font_stopwatch, self.f_s_stopwatch)
                            )
        self.saved_times_date = MyLabel(self.saved_frame, 'Data',
                            self.fg_stopwatch, self.bg_stopwatch,
                            font=(self.font_stopwatch, self.f_s_stopwatch)
                            )
        self.saved_times_time = MyLabel(self.saved_frame, 'Time',
                            self.fg_stopwatch, self.bg_stopwatch,
                            font=(self.font_stopwatch, self.f_s_stopwatch)
                            )                            
        self.saved_times_descript = MyLabel(self.saved_frame, 'Description',
                            self.fg_stopwatch, self.bg_stopwatch,
                            font=(self.font_stopwatch, self.f_s_stopwatch)
                            )                            
        saved_times_title_lbl.pack()
        self.saved_times_date.pack(side=tk.LEFT,expand=True)
        self.saved_times_time.pack(side=tk.LEFT, expand=True)
        self.saved_times_descript.pack(side=tk.LEFT,expand=True)


    def create_stopwatch_widgets(self):
        stopwatch_title_lbl = MyLabel(self.stopwatch_frame, 'Stopwatch',
                            self.fg_stopwatch, self.bg_stopwatch,
                            image=self.btn_default,
                            font=(self.font_stopwatch, self.f_s_stopwatch)
                            )
        stopwatch_lbl = MyLabel(self.stopwatch_frame, '',
                            self.fg_stopwatch, self.bg_stopwatch,
                            font=(self.font_stopwatch, self.f_s_stopwatch)
                            )
        delay_entry = tk.Entry(self.stopwatch_frame, width=30, 
                    font=(self.font_stopwatch, self.f_s_stopwatch),
                    background=self.bg_stopwatch,
                    foreground=self.fg_stopwatch,
                    )
        desc_entry = tk.Entry(self.stopwatch_frame, width=30, 
                    font=(self.font_stopwatch, self.f_s_stopwatch),
                    background=self.bg_stopwatch,
                    foreground=self.fg_stopwatch,
                    )
        desc_entry.insert(0, 'Description')
        delay_entry.insert(0, 'Delay if 0 or null = no delay')
        stop =  MyButton(self.stopwatch_frame, self.stop, 
                        self.fg_stopwatch,  self.bg_stopwatch,
                        image=self.low_height_widgets, 
                        name=self.stop.lower()
                        )

        start_pause = MyButton(self.stopwatch_frame, self.str_start, 
                        self.fg_stopwatch,  self.bg_stopwatch, 
                        image=self.low_height_widgets, 
                        name=f"{self.str_start.lower()}/{self.str_pause.lower()}"
                        )
        
        start_pause.config(command=lambda lbl=stopwatch_lbl, btn=start_pause, stp=stop, delay=delay_entry: self.toggle_start_pause(btn, lbl, stp, delay))
        stop.config(command=lambda lbl=stopwatch_lbl, btn=stop, sp=start_pause, entry=desc_entry: self.stop_stopwatch(btn, sp, lbl, entry))
        stopwatch_title_lbl.pack()
        stopwatch_lbl.pack(expand=True)
        desc_entry.pack(side=tk.LEFT)
        delay_entry.pack(side=tk.RIGHT)
        start_pause.pack(side=tk.TOP, fill=tk.BOTH)

    def toggle_start_pause(self, btn, watch_label, stop_btn, delay, stop=False):
        if stop:
            self.countdown_time(watch_label) 
            btn.config(text=self.str_start)
            return
        if btn['text'] == self.str_start:
            print(delay.get())
            def thji():
                print('kappa')
                btn.config(text=self.str_pause)
                self.countdown_time(watch_label, True)
                stop_btn.pack(side=tk.TOP, fill=tk.BOTH)
            dela = int(delay.get())
            self.timer = tim( float(dela), thji)
            self.timer.start()
            
            return
        elif btn['text'] == self.str_pause:
            btn.config(text=self.str_resume)
            self.countdown_time(watch_label)
        elif btn['text'] == self.str_resume:

            btn.config(text=self.str_pause)
            self.countdown_time(watch_label, True)

    def stop_stopwatch(self, stop, start_pause_button, watch_label, entry_val):
        time_now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        self.saved_times.add_time('stopwatch',time_now, ':'.join([str(time) for time in self.stopwatch_time if time>0]), entry_val.get() )
        self.toggle_start_pause(start_pause_button, watch_label, stop, 0, True)
        self.stopwatch_time = [0] * len(self.stopwatch_time)
        stop.pack_forget()
        self.refresh_saved_times()
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
