from re import M
import tkinter as tk
from tkinter import PhotoImage, ttk, colorchooser
from datetime import datetime, timedelta
from config import ConfigJSON
from my_widgets import MyButton, MyLabel, MyEntry
from playsound import playsound
import multiprocessing
import glob2 as glob
import pkg_resources
import threading
import random

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
    TITLE_IMG = f'{IMAGES_DIR}/title.png'
    DELETE_STRING = 'X'
    ALARM_PREFIX = "alarm_box"
    STOPWATCH_PREFIX = 'stopwatch'
    TIMER_PREFIX = 'timer'


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
        self.fg = self.config_sett["fg_color_settings"]["value"]
        self.bg = self.config_sett["bg_color_settings"]["value"]
        self.resolution = self.config_sett["resolution_settings"]["value"]
        self.font_size = self.config_sett["font_size_settings"]["value"]
        self.settings_font = self.config_sett["font_family_settings"]["value"]
        self.btn_default = PhotoImage(file=AppProperties.SETTINGS_IMG)
        self.img_section = self.btn_default.subsample(2, 2)
        self.img_description = self.btn_default.subsample(1, 2)

        tk.Toplevel.__init__(self, background=self.bg,  *args, **kwargs)
        self.geometry(self.resolution)
        self.title('Settings')
        self.attributes('-topmost', 'true')
        self.create_settings_widgets()
        self.create_save_btn()

    def create_save_btn(self):
        save_btn = MyButton(self, 'Save',
                            self.fg, self.bg, image=self.btn_default,
                            name='save_sett_btn')
        save_btn.grid(column=0, row=0, sticky=tk.W)
        save_btn.config(
            command=lambda: self.save_settings())

    def create_settings_widgets(self):
        for index, section in enumerate(self.all_sections):

            sectionFrame = tk.Frame(
                self, background=self.bg, name='section_frame_'+str(index))
            for index, subsect in enumerate(self.all_sections[section]):
                self.add_setting(sectionFrame, self.all_sections[section][subsect]["description"],
                                 section, subsect,
                                 self.all_sections[section][subsect]["value"],
                                 sectionFrame.grid_size()[1]+1)

            MyButton(self, section.capitalize(),
                     self.fg, self.bg,
                     image=self.img_section,
                     font=(self.settings_font, int(self.font_size**1.2)),
                     name=section+'_btn',
                     command=lambda secFram=sectionFrame: self.show_settings(
                         secFram)
                     ).grid(column=self.grid_size()[0]+1, row=1, sticky=tk.W)

    def choose_color(self, entry):
        color_code = colorchooser.askcolor(
            title="Choose color", parent=self)

        if color_code[1]:
            entry.delete(0, 'end')
            entry.insert(0, color_code[1])

    def add_setting(self, append, sett_descr, section_name, option_name, value, row_grid, width=20):
        MyLabel(append, sett_descr,
                self.fg, self.bg,
                image=self.img_description,
                font=(self.settings_font, self.font_size),
                ).grid(column=0, row=row_grid, sticky="nse")
        res_entry = tk.Entry(append, width=width,
                             font=(self.settings_font, self.font_size),
                             background=self.bg,
                             foreground=self.fg,
                             name=f"{section_name}/{option_name}"
                             )
        res_entry.insert(0, value)
        res_entry.grid(column=1, row=row_grid, sticky=tk.NSEW)
        if 'color' in option_name:
            button = MyButton(append, "Select color", self.fg,
                              self.bg, image=self.img_section,
                              command=lambda: self.choose_color(res_entry))
            button.grid(column=2, row=row_grid, sticky=tk.NSEW)
        # if color font = create color picker near

    def show_settings(self, show):
        for s in self.grid_slaves():
            if 'section_frame' in s.winfo_name():
                s.grid_forget()
        show.grid(column=0, row=3)

    def save_settings(self):
        for s in self.winfo_children():
            if 'section_frame' in s.winfo_name():
                for option in s.grid_slaves():
                    if option.widgetName == 'entry':
                        option_value = option.get()
                        if option_value.isdigit():
                            option_value = int(option_value)
                        sect_and_key = option.winfo_name().split("/")
                        self.all_config.modify_settings(
                            sect_and_key[0], sect_and_key[1], option_value)

    def add_button_section(self, section_name):
        row_grid = self.grid_size()[1] + 1
        return MyButton(self, section_name,
                        self.fg, self.bg,
                        image=self.img_section,
                        font=(self.settings_font, self.font_size*2),
                        ).grid(column=0, row=row_grid, sticky="e")


class MainMenu(tk.Menu):
    @property
    def root(self):
        return self._root

    def __init__(self, root, *args, **kwargs):
        tk.Menu.__init__(self, root, *args, **kwargs)
        self._root = root
        window_menu = WindowMenu(self, tearoff=0)
        self.add_cascade(label="Options", menu=window_menu)
        root.config(menu=self)


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
        self.bg = self.config_menu['menu_color_bg']["value"]
        self.fg = self.config_menu['menu_color_fg']["value"]
        tk.Frame.__init__(self, root, background=self.bg,
                          borderwidth=1, relief='raised', *args, **kwargs)
        menu_btn_alarms = MyButton(self, 'Alarms', self.fg, self.bg,
                                   image=self.img_menu, name="alarms_menu_btn")

        menu_btn_stopwatch = MyButton(self, 'Stopwatch', self.fg, self.bg,
                                      image=self.img_menu, name="stopwatch_menu_btn")

        menu_btn_timer = MyButton(self, 'Timer', self.fg, self.bg,
                                  image=self.img_menu,  name="timer_menu_btn")

        menu_btn_alarms.config(
            command=lambda f=alarm_frame: self.clear_and_show_clicked(f))
        menu_btn_stopwatch.config(
            command=lambda f=stopwatch_frame: self.clear_and_show_clicked(f))
        menu_btn_timer.config(
            command=lambda f=timer_frame: self.clear_and_show_clicked(f))

        menu_btn_alarms.pack(side=tk.LEFT, expand=True)
        menu_btn_stopwatch.pack(side=tk.LEFT, expand=True)
        menu_btn_timer.pack(side=tk.LEFT, expand=True)

    def clear_and_show_clicked(self, what, col_grid=0, row_grid=1, colspan=2):
        for slave in self._root.grid_slaves(row=1, column=0):
            slave.grid_forget()
            slave.grid_remove()
        what.grid(column=col_grid, row=row_grid,
                  columnspan=colspan, sticky=tk.NSEW)


class FooterFrame(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_footer = ConfigProperties.FOOTER_OPTIONS
        self.bg_footer = self.config_footer["footer_color_bg"]["value"]
        self.fg_footer = self.config_footer["footer_color_fg"]["value"]
        self.f_s_timer = self.config_footer["font_size_label"]["value"]
        self.font_timer = self.config_footer["font_label"]["value"]
        self.img_timer = PhotoImage(file=AppProperties.FOOTER_TIMER_IMG)

        tk.Frame.__init__(self, root, background=self.bg_footer,
                          borderwidth=1, relief='sunken', *args, **kwargs)
        self.time_label = MyLabel(self, '', self.fg_footer, self.bg_footer,
                                  image=self.img_timer,
                                  font=(self.font_timer, self.f_s_timer, 'bold'))
        self.time()

        self.time_label.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)

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

        self.bg_alarms = self.config_alarm["bg_color_alarms"]["value"]
        self.fg_alarms = self.config_alarm["fg_color_alarms"]["value"]
        self.snooze_time = self.config_alarm["snooze_time"]["value"]

        self.alarms_frame = tk.Frame(self, background=self.bg_alarms)
        self.edit_alarm_obj = None
        self.alarms_frame.columnconfigure(0, weight=1)
        self.alarms_frame.columnconfigure(1, weight=1)

        self.btn_default = PhotoImage(file=AppProperties.ALARMS_IMG)
        self.btn_subsampl52 = self.btn_default.subsample(5, 2)
        self.small_widgets = self.btn_default.subsample(3, 2)

        self.__create_alarm_boxes_frame()
        # self.debug_alarm_add(self.alarms_frame)
        self.refresh_alarms()
        self.set_alarms()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.alarms_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.config(background=self.bg_alarms)

    def __create_alarm_boxes_frame(self):
        alarm_title_lbl = MyLabel(self.alarms_frame, "Alarms",
                                  self.fg_alarms, self.bg_alarms,
                                  image=self.small_widgets,
                                  )

        add_button = MyButton(self.alarms_frame, 'Add',
                              self.fg_alarms, self.bg_alarms,
                              image=self.small_widgets,
                              name='add_alarm_btn'
                              )

        add_button.config(
            command=lambda: self.add_alarm())
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
        self.alarms_list.modify_section(
            alarm_json, ConfigProperties.STATE, state_now)

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

        alarm_box.config(state=alarm_text[ConfigProperties.STATE],
                         command=lambda alarm_json=alarm_json,
                         alarm_box=alarm_box: self.edit_alarm(alarm_json, alarm_box))
        delete_alarm.config(command=lambda alarm_json=alarm_json: [
                            self.remove_alarm_box(alarm_json), alarm_box.destroy(), delete_alarm.destroy()])

        alarm_box.bind("<Button-3>", lambda event, alarm_box=alarm_box, alarm_text=alarm_text,
                       alarm=alarm_json: self.toggle_alarm(alarm_box, alarm_text, alarm))

        alarm_box.grid(column=0, row=row_alarm + 2)
        delete_alarm.grid(column=1, row=row_alarm + 2,
                          padx=5, pady=1, sticky=tk.W)
        return alarm_box

    def destroy_edit_alarm(self):
        if self.edit_alarm_obj:
            self.edit_alarm_obj.destroy()

    def edit_alarm(self, alarm, btn):
        self.destroy_edit_alarm()
        self.edit_alarm_obj = EditAlarm(self, alarm, btn)

    def remove_alarm_box(self, json_alarm):
        self.alarms_list.pop_section(json_alarm)
        self.destroy_edit_alarm()
        self.refresh_alarms()

    def add_alarm(self):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today_name = now.strftime("%a")
        # FIXME for now its only day in engluish to need to change that
        row_alarm_box = self.alarms_frame.grid_size()[1]
        self.alarms_list.add_alarm(f"{AppProperties.ALARM_PREFIX}_{row_alarm_box}_{random.randint(0,100)}", dt_string, [
                                   today_name], 'none', self.snooze_time, '')
        self.refresh_alarms()

    def debug_alarm_add(self, frame):
        now = datetime.now() + timedelta(seconds=2)
        dt_string = now.strftime("%H:%M:%S")
        today_name = now.strftime("%a")
        # FIXME for now its only day in engluish to need to change that
        row_alarm_box = frame.grid_size()[1]
        self.alarms_list.add_alarm(f"{AppProperties.ALARM_PREFIX}{row_alarm_box}", dt_string, [
                                   today_name], '3.mp3', 1, 'Opis')
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
                if today[0:3] in alarm_prop['days']:

                    if dt_string in alarm_prop['time']:
                        AlarmPopup(self, self.config_alarm, alarm_prop)
        self.alarms_frame.after(1000, self.set_alarms)


class AlarmPopup(tk.Tk):
    def __init__(self, root, config_prop, alarm_popup, *args, **kwargs):
        self.bg = config_prop["bg_color_alarm_popup"]["value"]
        self.fg = config_prop["fg_color_alarm_popup"]["value"]
        self.alarm_popup = alarm_popup
        self.snooze_time = alarm_popup['snooze_time']
        tk.Toplevel.__init__(
            self, borderwidth=2, relief='raised', background=self.bg, *args, **kwargs)
        self._root = root
        self.eval(f'tk::PlaceWindow {str(self)} center')
        self.sound_process = None
        self.geometry(config_prop["alarm_popup_resolution"]["value"])
        self.protocol("WM_DELETE_WINDOW", self.minimalize)
        self.title(
            f"{self.alarm_popup[ConfigProperties.TIME]} - {self.alarm_popup[ConfigProperties.DESCR]}")
        self.mute_sound_txt = 'Mute sound'
        self.play_sound_txt = 'Play sound'
        self.img = PhotoImage(file=AppProperties.ALARMS_IMG)
        self.img_button = self.img.subsample(2, 2)
        self.relief_r = ['sunken', 'raised', 'flat', 'ridge', 'groove']
        self.create_popup_widgets()

        if config_prop["animation"]["value"]:
            self.change_relief()

    def minimalize(self):
        self.iconify()

    def create_popup_widgets(self):

        music_to_play = f"{AppProperties.SOUND_DIR}/{self.alarm_popup[ConfigProperties.SOUND]}"
        alarm_format = [self.alarm_popup[ConfigProperties.TIME],
                        ' '.join(
            [str(day) for day in self.alarm_popup[ConfigProperties.DAYS]]),
            self.alarm_popup[ConfigProperties.SOUND],
            self.alarm_popup[ConfigProperties.DESCR]]
        for index, alarm_part in enumerate(alarm_format):

            MyLabel(self, alarm_part, self.fg, self.bg, image=self.img
                    ).grid(row=index, column=0)
        mute_sound_btn = MyButton(self, self.mute_sound_txt,
                                  self.fg, self.bg,
                                  image=self.img_button,
                                  name=f"mute_alarm",
                                  )
        MyButton(self, 'Stop alarm', self.fg, self.bg, image=self.img_button,
                 name=f"stop_alarm", command=lambda: self.stop_alarm()
                 ).grid(row=0, column=1)

        self.snooze_btn = MyButton(self, 'Snooze alarm', self.fg, self.bg, image=self.img_button,
                                   name=f"snooze_alarm"
                                   )

        self.snooze_btn.config(command=lambda snooze_btn=self.snooze_btn, time=self.snooze_time,
                               snd=music_to_play: self.snooze_alarm(snooze_btn, time, snd))
        self.snooze_btn.grid(row=0, column=2)
        if self.start_sound(music_to_play):
            mute_sound_btn.config(command=lambda mute_sound_btn=mute_sound_btn,
                                  music_to_play=music_to_play: self.mute_sound(mute_sound_btn, music_to_play))
            mute_sound_btn.grid(row=0, column=3)
        # if sounds != none  toggle music button and play music threading

    def change_relief(self):

        self.config(relief=random.choice(self.relief_r))
        self.after(1000, self.change_relief)

    def stop_alarm(self):
        self.destroy()
        if self.sound_process != None:
            self.sound_process.kill()

    def mute_sound(self, btn, music_to_play):
        self.sound_process.kill()
        if btn['text'] == self.mute_sound_txt:
            btn['text'] = self.play_sound_txt
            return
        self.start_sound(music_to_play)
        btn['text'] = self.mute_sound_txt

    def snooze_alarm(self, sn_btn, time, snd):
        snooze_time_now = datetime.now() + timedelta(minutes=time)
        time_string = snooze_time_now.strftime("%H:%M:%S")
        sn_btn['text'] = f'Snooze alarm\n {time_string}'
        self.sound_process.kill()
        self.snooze_btn['state'] = 'disabled'
        time_ms = time * 60000

        self.minimalize()
        self.after(time_ms, self.start_sound, snd)

    def start_sound(self, snd_to_play):
        self.snooze_btn['state'] = 'normal'
        if AppProperties.SOUNDS_EXT in snd_to_play:

            self.sound_process = multiprocessing.Process(
                target=playsound, args=(snd_to_play,))
            self.sound_process.start()
            return True
        return False


class EditAlarm(tk.Tk):
    def __init__(self, root, alarm, alarm_btn, *args, **kwargs):
        self.img_edit = PhotoImage(file=AppProperties.ALARMS_IMG)
        self.img_check_day = self.img_edit.subsample(5, 4)
        self.btn_title = PhotoImage(file=AppProperties.TITLE_IMG)
        self.config_edit = ConfigProperties.ALARMS_OPTIONS
        self.alarms_list = ConfigProperties.ALARMS
        self.fg_edit = self.config_edit['fg_color_edit']["value"]
        self.bg_edit = self.config_edit['bg_color_edit']["value"]
        self.f_s_hours_entry = self.config_edit['hours_entry_font_size']["value"]
        self.f_s_select_snd = self.config_edit['select_sound_font_size']["value"]
        self.font_edit = self.config_edit['font_family_edit']["value"]
        self.day_names = self.config_edit['day_name']["value"].split(",")

        tk.Toplevel.__init__(
            self, borderwidth=2, relief='raised', background=self.bg_edit, *args, **kwargs)
        self.eval(f'tk::PlaceWindow {str(self)} right')
        self.geometry('500x500')
        self.overrideredirect(True)
        self.checkbox_days = None
        self.checked_days = None
        self.selected_snd = tk.StringVar()
        self.edit(alarm, alarm_btn)

    def edit(self, json_alarm, alarm_box):

        self.checkbox_days = []
        self.checked_days = []

        alarm_properties = self.alarms_list.section[json_alarm]
        alarm_format = alarm_properties
        alarm_description = alarm_properties["description"]
        alarm_snooze = alarm_properties["snooze_time"]
        alarm_format_lbl = f" {alarm_format[ConfigProperties.TIME]} \n {' '.join([str(elem) for elem in alarm_format[ConfigProperties.DAYS]])} \n {alarm_format[ConfigProperties.SOUND]}"

        hours_entry = MyEntry(self, self.fg_edit, self.bg_edit,
                              "Alarm's hours", self.btn_title,
                              alarm_format[ConfigProperties.TIME],
                              font=(self.font_edit, self.f_s_hours_entry))

        description_entry = MyEntry(self, self.fg_edit, self.bg_edit,
                                    'Description', self.btn_title, alarm_description,
                                    font=(self.font_edit, self.f_s_hours_entry))

        snooze_time_entry = MyEntry(self, self.fg_edit, self.bg_edit,
                                    'Snooze Time', self.btn_title, alarm_snooze,
                                    width=10,
                                    font=(self.font_edit, self.f_s_hours_entry))

        ''' ALARM TITLE  '''
        MyLabel(self, alarm_format_lbl,
                self.fg_edit, self.bg_edit,
                image=self.img_edit
                ).grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)
        ''' ALARM TITLE  '''
        save_btn = MyButton(self, "Save", self.fg_edit, self.bg_edit,
                            image=self.img_edit, name=f"save_alarm"
                            )
        cancel_btn = MyButton(self, "Cancel", self.fg_edit, self.bg_edit,
                              image=self.img_edit, name=f"cancel_btn"
                              )
        choose_music = self.create_sound_selection(
            alarm_format[ConfigProperties.SOUND])

        cancel_btn.config(command=lambda: self.edit_quit())
        save_btn.config(command=lambda: self.save_alarm(
            json_alarm, alarm_box, hours_entry.entry.get(),
            description_entry.entry.get(), self.selected_snd.get(),
            snooze_time_entry.entry.get())
        )
        checkbox_days_frame = self.create_checkbox_days(alarm_format)

        description_entry.grid(column=1, row=1, sticky=tk.NSEW)
        hours_entry.grid(column=1, row=2, sticky=tk.NSEW)
        snooze_time_entry.grid(column=1, row=3, sticky=tk.NSEW)
        cancel_btn.grid(column=0, row=5, sticky=tk.NSEW)
        save_btn.grid(column=1, row=5, sticky=tk.NSEW)
        choose_music.grid(column=0, row=1, rowspan=3, sticky=tk.NSEW)

        checkbox_days_frame.grid(
            row=4, column=0, columnspan=len(self.day_names), sticky=tk.NSEW)

    def create_sound_list_from_dir(self):
        music_list = []
        for file in glob.glob(f"{AppProperties.SOUND_DIR}/*{AppProperties.SOUNDS_EXT}"):
            music_list.append(file)
        return music_list

    def create_sound_selection(self, sound):
        s = ttk.Style()
        s.configure('my.TMenubutton', font=(self.font_edit,
                    self.f_s_select_snd), image=self.img_edit,
                    background=self.bg_edit, foreground=self.fg_edit,
                    compound=tk.CENTER,
                    )

        self.selected_snd.set(AppProperties.SOUND_DIR+'\\'+sound)
        choose_music = ttk.OptionMenu(
            self, self.selected_snd, "", *self.create_sound_list_from_dir(), style='my.TMenubutton')
        return choose_music

    def save_alarm(self, alarm_json, alarm_box, hour, descr, snd_save, snooze_time):
        new_days = []
        new_sound = snd_save.split('\\')[1]
        for day_check in self.checkbox_days:
            if 'selected' in day_check.state():
                new_days.append(day_check['text'][0:3])
                # FIXME 0:3 changed to dyunamical
        alarm_format = f"{hour} \n{' '.join([str(elem) for elem in new_days])}\n {new_sound} \n {snooze_time}"
        alarm_box['text'] = alarm_format
        self.alarms_list.modify_alarm(
            alarm_json, hour, new_days, new_sound, snooze_time, descr)

        self.edit_quit()

    def create_checkbox_days(self, alarm_format):

        checkbox_days_frame = tk.Frame(self, bg=self.bg_edit)

        s_check_bx = ttk.Style()
        s_check_bx.configure('my.TCheckbutton',
                             image=self.img_check_day,
                             background=self.bg_edit,
                             foreground=self.fg_edit
                             )

        # save editing alarm button and add to grid
        self.checkbox_days.clear()
        self.checked_days.clear()
        for indx, day in enumerate(self.day_names):
            check_button_day = ttk.Checkbutton(
                checkbox_days_frame, compound=tk.CENTER, text=day, style='my.TCheckbutton')
            if day[0:3] in alarm_format[ConfigProperties.DAYS]:
                # FIXME should be first letter from config, but for now it is like this
                self.checked_days.append(tk.IntVar(value=1))
                check_button_day.config(
                    variable=self.checked_days[indx])
            else:
                self.checked_days.append(tk.IntVar(value=0))
            check_button_day.grid(row=0, column=indx, sticky=tk.W)
            self.checkbox_days.append(check_button_day)
        return checkbox_days_frame
        # this loop is creating each day of the week and add it to checkbutton in array and add to grid

    def edit_quit(self):
        self.destroy()

# TODO Timer description popup?
# TODO My widgets = checkbox, opiotnmenu?
# TODO playsound change for other function with volume down? if can


class Timer(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_timer = ConfigProperties.TIMER_OPTIONS
        self.saved_times = ConfigProperties.SAVED_TIMES
        self.bg_timer = self.config_timer['bg_color_timer']["value"]
        self.fg_timer = self.config_timer['fg_color_timer']["value"]
        self.f_s_timer = self.config_timer['font_size_timer']["value"]
        self.font_timer = self.config_timer['font_timer']["value"]
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.btn_default = PhotoImage(file=AppProperties.TIMER_IMG)
        self.low_height_widgets = self.btn_default.subsample(3, 2)
        self.btn_title = PhotoImage(file=AppProperties.TITLE_IMG)

        self.timer_frame = tk.Frame(
            self, borderwidth=1, background=self.bg_timer, relief='sunken')

        self.saved_frame = tk.Frame(
            self, borderwidth=1, background=self.bg_timer, relief='sunken')

        self.timer_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.saved_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.is_counting = None
        self.timer_time = [0, 0, 0, 0, 0]
        self.timer_start_value = 0

        self.time_frame = tk.Frame(
            self.saved_frame, background=self.bg_timer)
        for i in range(3):
            self.time_frame.columnconfigure(i, weight=1)

        self.create_savedtimes_widgets()
        self.time_frame.pack(side=tk.TOP, fill='x', expand=True)
        self.refresh_saved_times()
        self.create_timer_widgets()

    def refresh_saved_times(self):
        for slave in self.time_frame.grid_slaves():
            if "time_value" in slave.winfo_name():
                slave.destroy()

        for index, section in enumerate(sorted(self.saved_times.section[AppProperties.TIMER_PREFIX], reverse=True)):
            sec_lbl = MyLabel(self.time_frame, str(index+1) + ". " + section,
                              self.fg_timer, self.bg_timer,
                              name=section+'/time_value_data',
                              borderwidth=2, relief='raised',
                              font=(self.font_timer, self.f_s_timer),
                              )
            # Data and index
            sec_lbl.grid(column=0, row=index+1, sticky=tk.NSEW)
            MyLabel(self.time_frame, self.saved_times.section[AppProperties.TIMER_PREFIX][section]['value'],
                    self.fg_timer, self.bg_timer,
                    borderwidth=2, relief='raised',
                    font=(self.font_timer, self.f_s_timer),
                    name='time_value_time'+str(index)
                    ).grid(column=1, row=index+1, sticky=tk.NSEW)
            # Time
            MyLabel(self.time_frame, self.saved_times.section[AppProperties.TIMER_PREFIX][section]['description'],
                    self.fg_timer, self.bg_timer,
                    font=(self.font_timer, self.f_s_timer),
                    name='time_value_description'+str(index),
                    borderwidth=2, relief='raised',
                    wraplength=100, justify=tk.LEFT
                    ).grid(column=2, row=index+1, sticky=tk.NSEW)
            # Description
            MyButton(self.time_frame, 'x',
                     self.fg_timer, self.bg_timer,
                     image=self.low_height_widgets,
                     font=(self.font_timer, self.f_s_timer),
                     name='time_value_delete'+str(index),
                     command=lambda sect_nam=sec_lbl.winfo_name().split("/")[0]: self.pop_and_refresh(
                         sect_nam)
                     ).grid(column=3, row=index+1, sticky=tk.E)

    def pop_and_refresh(self, sect_name):
        self.saved_times.pop_section(AppProperties.TIMER_PREFIX, sect_name)
        self.refresh_saved_times()

    def create_timer_widgets(self):
        timer_title_lbl = MyLabel(self.timer_frame, 'Timer',
                                  self.fg_timer, self.bg_timer,
                                  image=self.btn_default,
                                  font=(self.font_timer,
                                        self.f_s_timer)
                                  )

        self.time_entry = MyEntry(
            self.timer_frame, self.fg_timer, self.bg_timer, 'Timer',
            self.btn_title,
            ':'.join(str(x) for x in self.timer_time))

        delay_entry = MyEntry(
            self.timer_frame, self.fg_timer, self.bg_timer, 'Delay', self.btn_title)

        self.desc_entry = MyEntry(
            self.timer_frame, self.fg_timer, self.bg_timer, 'Description', self.btn_title)

        self.stop_btn = MyButton(self.timer_frame, AppProperties.STOP_TXT,
                                 self.fg_timer,  self.bg_timer,
                                 image=self.low_height_widgets,
                                 name=AppProperties.STOP_TXT.lower()
                                 )

        self.start_pause_btn = MyButton(self.timer_frame, AppProperties.START_TXT,
                                        self.fg_timer,  self.bg_timer,
                                        image=self.low_height_widgets,
                                        name=f"{AppProperties.START_TXT.lower()}/{AppProperties.PAUSE_TXT.lower()}"
                                        )

        self.start_pause_btn.config(command=lambda entry_timer=self.time_entry.entry, btn=self.start_pause_btn, stp=self.stop_btn,
                                    delay=delay_entry.entry: self.toggle_start_pause(btn, entry_timer, stp, delay))
        self.stop_btn.config(command=lambda entry_timer=self.time_entry.entry, btn=self.stop_btn,
                             sp_btn=self.start_pause_btn: self.stop_timer(btn, sp_btn, entry_timer, self.desc_entry))

        timer_title_lbl.pack(side=tk.TOP)
        self.time_entry.pack(expand=True)
        self.desc_entry.pack(side=tk.LEFT)
        delay_entry.pack(side=tk.RIGHT)
        self.start_pause_btn.pack(side=tk.TOP, fill=tk.BOTH)

    def create_savedtimes_widgets(self):
        MyLabel(self.saved_frame, 'Saved times',
                self.fg_timer, self.bg_timer,
                image=self.btn_default,
                font=(self.font_timer,
                      self.f_s_timer)
                ).pack()
        self.saved_times_date = MyLabel(self.time_frame, 'Data',
                                        self.fg_timer, self.bg_timer,
                                        font=(self.font_timer,
                                              self.f_s_timer)
                                        )
        self.saved_times_time = MyLabel(self.time_frame, 'Time',
                                        self.fg_timer, self.bg_timer,
                                        font=(self.font_timer,
                                              self.f_s_timer)
                                        )
        self.saved_times_descript = MyLabel(self.time_frame, 'Description',
                                            self.fg_timer, self.bg_timer,
                                            font=(self.font_timer,
                                                  self.f_s_timer)
                                            )
        self.saved_times_date.grid(column=0, row=0)
        self.saved_times_time.grid(column=1, row=0)
        self.saved_times_descript.grid(column=2, row=0)

    def toggle_start_pause(self, btn, entry_timer, stop_btn, delay='0', stop=False):
        if stop:
            self.countdown_time(entry_timer)
            btn.config(text=AppProperties.START_TXT)
            return
        if btn['text'] == AppProperties.START_TXT:
            def start_counting():
                self.timer_start_value = self.format_time_array()
                btn.config(text=AppProperties.PAUSE_TXT)
                self.countdown_time(entry_timer, True)
                stop_btn.pack(side=tk.TOP, fill=tk.BOTH)
            if sum(int(w) for w in entry_timer.get().split(":")) > 0:
                self.timer_time = entry_timer.get().split(":")
                self.timer_time = list(map(int, self.timer_time))
                if delay.get().isdigit() and int(delay.get()) > 0:
                    delay_int = int(delay.get())
                    timer = threading.Timer(float(delay_int), start_counting)
                    timer.start()
                else:
                    start_counting()
        elif btn['text'] == AppProperties.PAUSE_TXT:
            btn.config(text=AppProperties.RESUME_TXT)
            self.countdown_time(entry_timer)
        elif btn['text'] == AppProperties.RESUME_TXT:
            btn.config(text=AppProperties.PAUSE_TXT)
            self.countdown_time(entry_timer, True)

    def stop_timer(self, stop, sp_btn, entry_timer, entry_desc):
        time_now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        timer_value = f"{self.timer_start_value} {':'.join([str(time) for time in self.timer_time if time > 0])}"
        self.saved_times.add_time(
            AppProperties.TIMER_PREFIX, time_now, timer_value, entry_desc.get())
        entry_timer.delete(0, 'end')
        self.timer_time = [0] * len(self.timer_time)
        self.toggle_start_pause(sp_btn, entry_timer, stop, '0', True)
        entry_timer.insert(1, ':'.join(str(x) for x in self.timer_time))
        stop.pack_forget()
        self.refresh_saved_times()

    def countdown_time(self, time_entry, start=False):
        def time():
            time_entry.delete(0, 'end')
            time_entry.insert(1, self.format_time_array())

            if sum(t for t in self.timer_time) > 0:
                print(self.format_time_array())
                self.is_counting = time_entry.after(1, time)
                self.timer_time[4] = self.timer_time[4] - 1
                return
            else:
                self.stop_timer(
                    self.stop_btn, self.start_pause_btn, self.time_entry.entry, self.desc_entry.entry)
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
        text_to_show = ""
        found_more_0 = False
        for time_val in self.timer_time:
            if time_val > 0:
                found_more_0 = True
                text_to_show += str(time_val) + ":"
            elif found_more_0:
                text_to_show += str(time_val) + ":"
        # text_to_show = f"{days}:{hours}:{minutes}:{seconds}:{ms}"
        return text_to_show[:-1]

# FIXME delay bug start multiple
# TODO Create default.json for default options?

# TODO Volume of alarm(probbaly not with playsound )
# TODO Random alarm from list? (could be done, not necessary for now)


class Stopwatch(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_stpwch = ConfigProperties.STOPWATCH_OPTIONS
        self.saved_times = ConfigProperties.SAVED_TIMES
        self.bg_stopwatch = self.config_stpwch["bg_color_stopwatch"]["value"]
        self.fg_stopwatch = self.config_stpwch["fg_color_stopwatch"]["value"]
        self.f_s_stopwatch = self.config_stpwch['font_size_stopwatch']["value"]
        self.font_stopwatch = self.config_stpwch['font_stopwatch']["value"]
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.btn_default = PhotoImage(file=AppProperties.STOPWATCH_IMG)
        self.low_height_widgets = self.btn_default.subsample(3, 2)
        self.btn_title = PhotoImage(file=AppProperties.TITLE_IMG)

        self.counting_interval = None
        self.stopwatch_time = [0, 0, 0, 0, 0]

        self.stopwatch_frame = tk.Frame(
            self, borderwidth=1, background=self.bg_stopwatch, relief='sunken')

        self.saved_frame = tk.Frame(
            self, borderwidth=1, background=self.bg_stopwatch, relief='sunken')

        self.stopwatch_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.saved_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.time_frame = tk.Frame(
            self.saved_frame, background=self.bg_stopwatch)
        for i in range(3):
            self.time_frame.columnconfigure(i, weight=1)

        self.create_savedtimes_widgets()
        self.time_frame.pack(side=tk.TOP, fill='x', expand=True)
        self.refresh_saved_times()
        self.create_stopwatch_widgets()

    def refresh_saved_times(self):
        for slave in self.time_frame.grid_slaves():
            if "time_value" in slave.winfo_name():
                slave.destroy()
        for index, section in enumerate(sorted(self.saved_times.section[AppProperties.STOPWATCH_PREFIX], reverse=True)):
            sec_lbl = MyLabel(self.time_frame, str(index+1) + ". " + section,
                              self.fg_stopwatch, self.bg_stopwatch,
                              name=section+'/time_value_data',
                              borderwidth=2, relief='raised',
                              font=(self.font_stopwatch, self.f_s_stopwatch)
                              )
            # Data and index
            sec_lbl.grid(column=0, row=index+1, sticky=tk.NSEW)
            MyLabel(self.time_frame, self.saved_times.section[AppProperties.STOPWATCH_PREFIX][section]['value'],
                    self.fg_stopwatch, self.bg_stopwatch,
                    borderwidth=2, relief='raised',
                    font=(self.font_stopwatch, self.f_s_stopwatch),
                    name='time_value_time'+str(index)
                    ).grid(column=1, row=index+1, sticky=tk.NSEW)
            # Time

            MyLabel(self.time_frame, self.saved_times.section[AppProperties.STOPWATCH_PREFIX][section]['description'],
                    self.fg_stopwatch, self.bg_stopwatch,
                    font=(self.font_stopwatch, self.f_s_stopwatch),
                    name='time_value_description'+str(index),
                    borderwidth=2, relief='raised',
                    wraplength=100, justify=tk.LEFT
                    ).grid(column=2, row=index+1, sticky=tk.NSEW)
            # Description
            MyButton(self.time_frame, 'x',
                     self.fg_stopwatch, self.bg_stopwatch,
                     image=self.low_height_widgets,
                     font=(self.font_stopwatch, self.f_s_stopwatch),
                     name='time_value_delete'+str(index),
                     command=lambda sect_nam=sec_lbl.winfo_name().split("/")[0]: self.pop_and_refresh(
                         sect_nam)
                     ).grid(column=3, row=index+1, sticky=tk.E)

    def pop_and_refresh(self, sect_name):
        self.saved_times.pop_section(AppProperties.STOPWATCH_PREFIX, sect_name)
        self.refresh_saved_times()

    def create_savedtimes_widgets(self):
        MyLabel(self.saved_frame, 'Saved times',
                self.fg_stopwatch, self.bg_stopwatch,
                image=self.btn_default,
                font=(self.font_stopwatch,
                      self.f_s_stopwatch)
                ).pack()
        self.saved_times_date = MyLabel(self.time_frame, 'Data',
                                        self.fg_stopwatch, self.bg_stopwatch,
                                        font=(self.font_stopwatch,
                                              self.f_s_stopwatch)
                                        )
        self.saved_times_time = MyLabel(self.time_frame, 'Time',
                                        self.fg_stopwatch, self.bg_stopwatch,
                                        font=(self.font_stopwatch,
                                              self.f_s_stopwatch)
                                        )
        self.saved_times_descript = MyLabel(self.time_frame, 'Description',
                                            self.fg_stopwatch, self.bg_stopwatch,
                                            font=(self.font_stopwatch,
                                                  self.f_s_stopwatch)
                                            )
        self.saved_times_date.grid(column=0, row=0)
        self.saved_times_time.grid(column=1, row=0)
        self.saved_times_descript.grid(column=2, row=0)

    def create_stopwatch_widgets(self):
        stopwatch_title_lbl = MyLabel(self.stopwatch_frame, 'Stopwatch',
                                      self.fg_stopwatch, self.bg_stopwatch,
                                      image=self.btn_default,
                                      font=(self.font_stopwatch,
                                            self.f_s_stopwatch)
                                      )
        stopwatch_lbl = MyLabel(self.stopwatch_frame, '',
                                self.fg_stopwatch, self.bg_stopwatch,
                                font=(self.font_stopwatch, self.f_s_stopwatch)
                                )

        delay_entry = MyEntry(self.stopwatch_frame, self.fg_stopwatch, self.bg_stopwatch,
                              'Delay', self.btn_title)

        desc_entry = MyEntry(self.stopwatch_frame, self.fg_stopwatch, self.bg_stopwatch,
                             'Description', self.btn_title)

        stop = MyButton(self.stopwatch_frame, AppProperties.STOP_TXT,
                        self.fg_stopwatch,  self.bg_stopwatch,
                        image=self.low_height_widgets,
                        name=AppProperties.STOP_TXT.lower()
                        )

        start_pause = MyButton(self.stopwatch_frame, AppProperties.START_TXT,
                               self.fg_stopwatch,  self.bg_stopwatch,
                               image=self.low_height_widgets,
                               name=f"{AppProperties.START_TXT.lower()}/{AppProperties.PAUSE_TXT.lower()}"
                               )

        start_pause.config(command=lambda: self.toggle_start_pause(
            start_pause, stopwatch_lbl, stop, delay_entry.entry.get()))

        stop.config(command=lambda: self.stop_stopwatch(
            stop, start_pause, stopwatch_lbl, desc_entry.entry.get()))

        stopwatch_title_lbl.pack()
        stopwatch_lbl.pack(expand=True)
        desc_entry.pack(side=tk.LEFT)
        delay_entry.pack(side=tk.RIGHT)
        start_pause.pack(side=tk.TOP, fill=tk.BOTH)

    def toggle_start_pause(self, btn, watch_label, stop_btn, delay='0', stop=False):
        if stop:
            self.countdown_time(watch_label)
            btn.config(text=AppProperties.START_TXT)
            return
        print(delay)
        if btn['text'] == AppProperties.START_TXT:
            def start_counting():
                btn.config(text=AppProperties.PAUSE_TXT)
                self.countdown_time(watch_label, True)
                stop_btn.pack(side=tk.TOP, fill=tk.BOTH)
            if delay.isdigit() and int(delay) > 0:
                delay_int = int(delay)
                timer = threading.Timer(float(delay_int), start_counting)
                timer.start()
            else:
                start_counting()
        elif btn['text'] == AppProperties.PAUSE_TXT:
            btn.config(text=AppProperties.RESUME_TXT)
            self.countdown_time(watch_label)
        elif btn['text'] == AppProperties.RESUME_TXT:

            btn.config(text=AppProperties.PAUSE_TXT)
            self.countdown_time(watch_label, True)

    def stop_stopwatch(self, stop, start_pause_button, watch_label, entry_desc):
        time_now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        self.saved_times.add_time(AppProperties.STOPWATCH_PREFIX, time_now, ':'.join(
            [str(time) for time in self.stopwatch_time if time > 0]), entry_desc)
        self.toggle_start_pause(
            start_pause_button, watch_label, stop, '0', True)
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
        text_to_show = ""
        found_more_0 = False
        for time_val in self.stopwatch_time:
            if time_val > 0:
                found_more_0 = True
                text_to_show += str(time_val) + ":"
            elif found_more_0:
                text_to_show += str(time_val) + ":"
        return text_to_show[:-1]

    def countdown_time(self, time_lbl, start=False):
        if not start:
            time_lbl.after_cancel(self.counting_interval)
            return

        def time():
            time_lbl.config(text=self.format_time_array())
            self.counting_interval = time_lbl.after(1, time)
            self.stopwatch_time[4] = self.stopwatch_time[4] + 1
        time()
