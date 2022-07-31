from turtle import back
import pkg_resources
pkg_resources.require("playsound==1.2.2")
from playsound import playsound
import multiprocessing
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
import glob2 as glob

class AlarmsProperties:
    ALARM_PREFIX = 'alarm_box'
    TIME = 'time'
    DAYS = 'days'
    SOUND = 'sound'
    STATE = 'state'

class Alarms(tk.Frame):
    def __init__(self, root, json_conf, json_alarms, *args, **kwargs):
        self._root = root
        self.config_name = 'config.ini'
        self.json_conf = json_conf
        self.json_alarms = json_alarms
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.edit_frame = None
        self.alarms_frame = None
        self.check_days = []
        self.snoozed_alarms = []
        self.snoozed_time = 1
        self.checked_days = []
        self.__create_alarm_boxes_frame(root)
        self.__create_edit_alarm_frame(root)  
        # self.set_alarms()
    def refresh_alarms(self):
        self.alarms_frame.grid_slaves().clear()
        for row, alarm in enumerate(self.json_alarms.section): 
            print(alarm)
            self.create_alarm(self.alarms_frame, alarm, row)

    def config_alarms_appearance(self, key_name, section='alarms_options'):
        return self.config.get_key(section, key_name)

    def __create_edit_alarm_frame(self, append):
        self.edit_frame = tk.Frame(append, borderwidth=15, relief='sunken', background=self.json_conf["bg_edit"])
        self.edit_frame.grid(column=0, row=1, sticky="nsew")
    # function for creating editing for alarm frame

    def __create_alarm_boxes_frame(self, append, width=30):

        self.alarms_frame = tk.Frame(append, background = self.json_conf["bg_alarms"])
        tk.Label(self.alarms_frame, text='Alarms' , background=self.json_conf['lbl_alarms_bg'], justify='center',
                  borderwidth=1, relief="solid"
                  ).grid(column=0, row=0, sticky='new')
        
        # add buttons for adding new alarms
        add_button = tk.Button(self.alarms_frame, text="Add", 
                                height=1, width=width, 
                                background=self.json_conf['add_btn_bg_color'], 
                                activebackground=self.json_conf['add_btn_bg_color_active']
                                )

        self.refresh_alarms()
    
        self.alarms_frame.config(borderwidth=15, relief='sunken')
        self.alarms_frame.grid(column=1, row=1, sticky="nsew")
        add_button.grid(column=2, row=0, padx=5, pady=1)
        add_button.config(command=lambda f=self.alarms_frame: self.add_alarm(f))

    #create all alarms etc. it should be from config

    def create_alarm(self, append, alarm_json, row_alarm):
        alarm_text = self.json_alarms.section[alarm_json]
        def toggle_alarm(e, alarm_box):
            state_now = ""
            if alarm_box[AlarmsProperties.STATE] == 'disabled':
                state_now = 'normal'
            else:
                state_now = "disabled"
            alarm_box[AlarmsProperties.STATE] = state_now
            alarm_text[AlarmsProperties.STATE] = state_now
            self.json_alarms.modify_section(alarm_json, AlarmsProperties.STATE, state_now)
            #save to config json(toggle state = disabled / normal)


        alarm_format = f"{alarm_text[AlarmsProperties.TIME]} \n {' '.join([str(elem) for elem in alarm_text[AlarmsProperties.DAYS]])} \n {alarm_text[AlarmsProperties.SOUND]}"
        alarm_box = tk.Button(append, text= alarm_format, 
                            background=self.json_conf["alarm_box_bg"], 
                            activebackground=self.json_conf["alarm_box_bg_active"], 
                            width=30, height=3, name=f"alarm_box{row_alarm}"
                            )
        delete_alarm = tk.Button(append, text='x', 
                                background=self.json_conf["delete_bg_color"], 
                                activebackground=self.json_conf["delete_bg_color_active"], 
                                height=2, width=6)
 
        alarm_box.grid(column=0, row=row_alarm + 2)
        alarm_box.config(state=alarm_text[AlarmsProperties.STATE], command=lambda alarm_json=alarm_json, alarm_box=alarm_box: self.edit_alarm(alarm_json, alarm_box))


        alarm_box.bind("<Button-3>", lambda event, alarm_box=alarm_box: toggle_alarm(event, alarm_box))

        delete_alarm.grid(column=2, row=row_alarm + 2, padx=5, pady=1, sticky='w')
        delete_alarm.config(command=lambda alarm_json=alarm_json : [self.remove_alarm_box(alarm_json), alarm_box.destroy(), delete_alarm.destroy()])

        return alarm_box

    def clear_edit_frame(self):
        for widgets in self.edit_frame.winfo_children():
            widgets.destroy()

    def remove_alarm_box(self, json_alarm):
            self.json_alarms.pop_section(json_alarm)
            self.clear_edit_frame()

    def edit_alarm(self, json_alarm, alarm_box):
        SOUND = 'sounds'
                
        # clear everything inside edit box
        
        alarm_format = self.json_alarms.section[json_alarm]
        alarm_format_lbl = f" {alarm_format[AlarmsProperties.TIME]} \n {' '.join([str(elem) for elem in alarm_format[AlarmsProperties.DAYS]])} \n {alarm_format[AlarmsProperties.SOUND]}"

        def create_alarm_name_lbl(txt, config_name = 'alarm_label_bg', width=20, anchor='center'):
            alarm_label = tk.Label(self.edit_frame, anchor=anchor, width=width, 
                                    background=self.json_conf[config_name],
                                    text=txt
                                  )
            alarm_label.grid(column=1, row=0, sticky='ns')   
            return alarm_label

        def create_hours_entry(time, font_size=self.json_conf['hours_entry_font_size'], bg=self.json_conf['hours_entry_bg'], width=10):
            hours = tk.Entry(self.edit_frame, bd=1, width=width, 
                            font=("default", font_size), 
                            background=bg
                            )
            hours.insert(0, f"{time}")
            hours.grid(column=1, row=2, sticky='nsew')
            return hours

        def create_sound_list_from_dir():
            music_list = []
            for file in glob.glob(f"{SOUND}/*.mp3"):
                #FIXME sounds = const?
                music_list.append(file)
            return music_list

        def create_sound_selection(sound):
            s = ttk.Style()
            
            s.configure('my.TMenubutton', font=('Helvetica', 
                        self.json_conf['select_sound_font_size']), 
                        background=self.json_conf['select_sound_bg']
                        )
            selected_snd = tk.StringVar()
            selected_snd.set(SOUND+'\\'+sound)
            choose_music = ttk.OptionMenu(self.edit_frame, selected_snd, "",*create_sound_list_from_dir(), style='my.TMenubutton')
            choose_music.grid(column=2, row=0, sticky="nsew")
            choose_music.config()
            return selected_snd

        def create_save_button(hours_entry, selected_snd):
            save_btn = tk.Button(self.edit_frame, text="Save", 
                                background=self.json_conf['save_btn_bg'],
                                activebackground=self.json_conf['save_btn_bg_active'], 
                                font=('Helvetica', self.json_conf['save_btn_font_size'])
                                )
            save_btn.config(command=lambda alarm_json=json_alarm, alarm_box=alarm_box, hour=hours_entry: save_alarm(alarm_json, alarm_box, hour, selected_snd.get()))
            save_btn.grid(column=2, row=2, sticky="nsew")
    
        def create_checkbox_days():
            # day_names = self.config.get_key("alarms_options", "day_name").split(",")
            day_names = self.json_conf['day_name']

            checkbox_days_frame = tk.Frame(self.edit_frame)
            checkbox_days_frame.grid(row=5, column=0, columnspan=len(day_names), sticky="nsew")

            s_check_bx = ttk.Style()
            s_check_bx.configure('my.TCheckbutton', background=self.json_conf['check_box_bg'])
  
            # save editing alarm button and add to grid
            self.check_days.clear()
            self.checked_days.clear()
            for indx, day in enumerate(day_names):
                check_button_day = ttk.Checkbutton(checkbox_days_frame, text=day, style='my.TCheckbutton')
                if day[0:3] in alarm_format[AlarmsProperties.DAYS]:
                    #FIXME should be first letter from config, but for now it is like this
                    self.checked_days.append(tk.IntVar(value = 1))
                    check_button_day.config(variable=self.checked_days[indx])
                else:
                    self.checked_days.append(tk.IntVar(value = 0))
                check_button_day.grid(row=0, column=indx, sticky='w')
                self.check_days.append(check_button_day)
            # this loop is creating each day of the week and add it to checkbutton in array and add to grid
 
        def save_alarm(alarm_json, alarm_box, hour, snd_save):
            new_hour = hour.get()
            new_days = []
            new_sound = snd_save.split('\\')[1]
            for day_check in self.check_days:
                if 'selected' in day_check.state():
                    new_days.append(day_check['text'][0:3])
                    #FIXME 0:3 changed to dyunamical
            alarm_format = f"{new_hour} \n{' '.join([str(elem) for elem in new_days])}\n {new_sound}"
            alarm_box['text'] = alarm_format
            self.json_alarms.modify_section(alarm_json, AlarmsProperties.TIME, new_hour)
            self.json_alarms.modify_section(alarm_json, AlarmsProperties.DAYS, new_days)
            self.json_alarms.modify_section(alarm_json, AlarmsProperties.SOUND, new_sound)
            #TODO SAVE ALARM TO CONFIG
            # add hours and days to editing alarm
        
        def create_edit_appearance():
            hours_entry = create_hours_entry(alarm_format[AlarmsProperties.TIME])
            create_alarm_name_lbl(alarm_format_lbl)
            create_sound_list_from_dir()
            selected_snd = create_sound_selection(alarm_format[AlarmsProperties.SOUND])
            create_save_button(hours_entry, selected_snd)
            create_checkbox_days()
            return
        create_edit_appearance()
        #FIXME fix this lul create_edit_appearance


    def add_alarm(self, frame):
     # this function is for adding new alarm, which maybe should be here, idk
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today_name = now.strftime("%a")
        #FIXME for now its only day in engluish to need to change that
        row_alarm_box = frame.grid_size()[1]
        print(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}")
        self.json_alarms.modify_section(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}", AlarmsProperties.TIME, dt_string)
        self.json_alarms.modify_section(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}", AlarmsProperties.DAYS, [today_name])
        self.json_alarms.modify_section(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}", AlarmsProperties.SOUND, 'none')
        self.json_alarms.modify_section(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}", AlarmsProperties.STATE, 'disabled')
        self.refresh_alarms()
    # function which for add new alarm box

    def check_alarms(self):
        alarms = []
        for alarm in self.alarms_frame.grid_slaves():
            if "alarm_box" not in str(alarm):
                continue
            if alarm[AlarmsProperties.STATE] == "normal":
                al = alarm['text'].split("\n")
                alarms.append(al)
        for snoozed_alarm in self.snoozed_alarms:
            al = snoozed_alarm.split("\n")
            alarms.append(al)
        return alarms
    # check which alarm is enabled

    def alarm_popup(self, text, sound):
        def stop_alarm():
            top.destroy()
            p.kill()

        def snooze_alarm():
            snooze_time_now = datetime.now() + timedelta(minutes=self.snoozed_time)
            time_string = snooze_time_now.strftime("%H:%M:%S")
            day_string = snooze_time_now.strftime("%a")
            snoozed_alarm_time = time_string + "\n" + day_string
            self.snoozed_alarms.append(snoozed_alarm_time)

        top = tk.Toplevel(self.root)
        top.geometry("750x250")
        top.title(text)
        top.overrideredirect(True)
        if(sound != 'None'):
            p = multiprocessing.Process(target=playsound, args=(sound,))
            p.start()
        ttk.Label(top, text=text, font='Mistral 18 bold').pack(side='left')
        ttk.Button(top, text="Stop alarm", command=lambda: stop_alarm()).pack(side='right')
        ttk.Button(top, text="Mute sound", command=lambda: p.kill()).pack(side='right')
        ttk.Button(top, text="Snooze", command=lambda alarm=text: [snooze_alarm(), stop_alarm()]
                   ).pack(side='right')
    # if alarm == set time = popup window with alarm

    def set_alarms(self):
        alarms = self.check_alarms()
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today = now.strftime("%A")
        now_time = dt_string + "\n" + today[0:3]
        for current_alarm in alarms:
            if today[0:3] in str(current_alarm[1]):
                if dt_string in str(current_alarm[0]):
                    self.alarm_popup(now_time, f"{current_alarm[2]}")
        self.alarms_frame.after(1000, self.set_alarms)

    
    class EditAlarm(tk.Frame):
        def __init__(self, root, config_txt, *args, **kwargs):
            self._root = root
            tk.Frame.__init__(self, root, *args, **kwargs)
            self.config_txt = config_txt
       
        def save_alarm(self, what_save, hour, snd_save):
            def info_save(remove=False):
                info_btn_save = ttk.Label(self)
                if not remove:
                    info_btn_save.config(text='It has to be at least one day')
                    info_btn_save.grid(column=2, row=4, sticky="w")
                    return
                info_btn_save.grid_remove()
            # info_save is giving info about what should be added for alarm to work
            new_alarm = f"{hour.get()}\n"
            found = False
            for d in self.check_days:
                if 'selected' in d.state():
                    found = True
                    info_save(found)
                    new_alarm += f"{d['text']} "
            new_alarm += f"\n{snd_save}"
            if not found:
                info_save(found)
                return
            # check every check box with day if it's selected
            what_save['text'] = new_alarm
            new_alarm += "/normal"
            self.config.save_config(self.cnf_sect_alarms, self.config_txt[0], new_alarm.replace("\n", '#'))
            # add hours and days to editing alarm
            self.clear_edit_frame()

        # clear everything inside edit box


        # def create_alarm_name_lbl():
        #     bg_color = self.config_alarms_appearance('alarm_label_bg')
        #     font_size = self.config_alarms_appearance('alarm_label_font_size')
           
        #     alarm_label = ttk.Label(self.edit_frame, anchor='center', width=20, background=bg_color,
        #         font=("default", font_size), text=f' {alarm["text"]}'
        #         )
        #     alarm_label.grid(column=1, row=0, sticky='ns')   
        #     return alarm_label
        # # ttk.Label(self.edit_frame, padding=20, text=f' {b["text"]}').pack(side='top', expand=False)
        # # text about what alarm is edited (i'll create these names later)
       
        # def create_hours_entry(txt):
        #     bg_color = self.config_alarms_appearance('hours_entry_bg')
        #     font_size = self.config_alarms_appearance('hours_entry_font_size')
        #     hours = tk.Entry(self.edit_frame, bd=1, width=10, font=("default", font_size), background=bg_color)
        #     hours.grid(column=1, row=2, sticky='nsew')
        #     hour_text = txt[0].split(":")
        #     hours.insert(0, f"{hour_text[0]}:{hour_text[1]}:{hour_text[2]}")
        #     return hours
        # # create hour Entry
        # # add it to grid
        # # add hour from alarm (take text from alarm_button and split it with space and :) that is editing
        # def create_sound_list_from_dir():
        #     music_list = []
        #     for file in glob.glob(f"{SOUNDS_DIR}/*.mp3"):
        #         music_list.append(file)
        #     return music_list

        # def create_sound_selection(txt):
        #     s = ttk.Style()
        #     font_size = self.config_alarms_appearance('s_snd_font_size')
        #     bg_color = self.config_alarms_appearance('s_snd_bg')

        #     s.configure('my.TMenubutton', font=('Helvetica', font_size), background=bg_color)
        #     selected_snd = tk.StringVar()
        #     selected_snd.set(txt[2])
        #     choose_music = ttk.OptionMenu(self.edit_frame, selected_snd, "",*create_sound_list_from_dir(), style='my.TMenubutton')
        #     choose_music.grid(column=2, row=0, sticky="nsew")
        #     choose_music.config()
        #     return selected_snd

        # def create_save_button(hours, selected_snd):
        #     font_size = self.config_alarms_appearance('save_btn_font_size')
        #     bg_color = self.config_alarms_appearance('save_btn_bg')
        #     bg_active = self.config_alarms_appearance('save_btn_bg_active')
        #     save_btn = tk.Button(self.edit_frame, text="Save", background=bg_color, activebackground=bg_active, font=('Helvetica', font_size))
        #     save_btn.config(command=lambda timer=alarm, h=hours: save_alarm(timer, h, selected_snd.get()))
        #     save_btn.grid(column=2, row=2, sticky="nsew")

        # def create_checkbox_days():
        #     s_frame = ttk.Style()
        #     bg_color = self.config.get_key("app_setting", "style_background")
        #     s_frame.configure('my.TFrame', background=bg_color)

        #     checkbox_days_frame = ttk.Frame(self.edit_frame, style="my.TFrame")
        #     checkbox_days_frame.grid(row=5, column=0, columnspan=len(self.day_names), sticky="nsew")

        #     s_check_bx = ttk.Style()
        #     bg_color_check_btn = self.config_alarms_appearance('check_box_bg')
        #     s_check_bx.configure('my.TCheckbutton', background=bg_color_check_btn)
  
        #     # save editing alarm button and add to grid
        #     self.check_days.clear()
        #     self.checked_days.clear()
        #     for indx, day in enumerate(self.day_names):
        #         check_button_day = ttk.Checkbutton(checkbox_days_frame, text=day, style='my.TCheckbutton')
        #         if day in alarm['text']:
        #             self.checked_days.append(tk.IntVar(value = 1))
        #             check_button_day.config(variable=self.checked_days[indx])
        #         else:
        #             self.checked_days.append(tk.IntVar(value = 0))
        #         check_button_day.grid(row=0, column=indx, sticky='w')
        #         self.check_days.append(check_button_day)
        #     # this loop is creating each day of the week and add it to checkbutton in array and add to grid
 
        
        # def create_edit_appearance():
        #     alarm_text = alarm['text'].split("\n")
        #     clear_edit_frame()
        #     alarm_label = create_alarm_name_lbl()
        #     hours_entry = create_hours_entry(alarm_text)
        #     selected_snd = create_sound_selection(alarm_text)
        #     save_btn = create_save_button(hours_entry, selected_snd)
        #     create_checkbox_days()
        
        # create_edit_appearance()

    # plan taki:
    # wyskakuje nowe okno(ktore moze miga?) pokazuje ze czas przepylnal i jest tam wiadomosc(jesli byla napisana)
    # muzyka dzwiek gra przez caly czas az do momentu max. dzwieku
    # po tym czasie zostaje sam alarm bez dzwieku
    # tutaj skonczylem sprawdzic jak to z klasami i co pozmieniac ale moze pozniej
    # klasa1: tworzy framy i ustawia
    # klasa2: tworzy alarm i edity itd?