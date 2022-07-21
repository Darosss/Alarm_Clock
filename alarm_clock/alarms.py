import configparser
from distutils.command.config import config
import pkg_resources
pkg_resources.require("playsound==1.2.2")
from playsound import playsound
import multiprocessing
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from datetime import timedelta
import glob2 as glob



class Alarms:
    def __init__(self, app_window, config_name, snd_dir,style, day_names, snoozed_time):
        # init(self, aplication tk, alarms from config, style from user, day_names from user, snooze time from user)
        self.config_name = config_name
        self.sect_alarm_n = "list_alarms"
        self.alarms = self.read_config_alarms(self.config_name, self.sect_alarm_n)
        self.styleName = style
        self.app_window = app_window
        self.day_names = day_names
        self.edit_frame = None
        self.alarms_frame = None
        self.check_days = [None] * len(self.day_names)
        # check if i can do it without assigning None
        self.snoozed_alarms = []
        self.snoozed_time = snoozed_time
        self.music_list = []
        self.check_day = tk.IntVar(value=1)
        self.sounds_dir = snd_dir

    def read_config(self, config_name, key_name, option_name):
        config_obj = configparser.ConfigParser()
        config_obj.read(config_name) 
        return config_obj[key_name][option_name]

    def read_config_alarms(self, config_name, key_name):
        config_obj = configparser.ConfigParser()
        config_obj.read(config_name)
        alarms_list = []
        for key in config_obj[key_name]:
            alarms_list.append(key +"/"+config_obj[key_name][key].replace("#","\n"))
        return alarms_list     

    def save_config(self, config_name, section, key_name, value="", new=False, remove=False):
        config_obj = configparser.ConfigParser()
        config_obj.read(config_name)
        if new:
            config_obj.set(section, key_name, value)
        elif not new and not remove:
            config_obj.set(section, key_name, value)
        if remove:
            config_obj.remove_option(section, key_name)
        with open(config_name, 'w') as configfile:
            config_obj.write(configfile)

    def __create_edit_alarm_frame(self, append):
        self.edit_frame = ttk.Frame(append, style=self.styleName, borderwidth=15, relief='sunken')
        self.edit_frame.grid(column=0, row=0, sticky="nsew")
    # function for creating editing for alarm frame

    def __create_alarm_boxes_frame(self, append, width=30):
        self.alarms_frame = ttk.Frame(append, style=self.styleName)
        
        ttk.Label(self.alarms_frame, text='Alarms' , justify='center', font=('calibri', 25, 'bold'),
                  borderwidth=1, relief="solid").grid(column=0, row=0, sticky='new')
        
        # add buttons for adding new alarms
        add_button = tk.Button(self.alarms_frame, text="Add", height=1, width=width)

        for index, alarm_text in enumerate(self.alarms):
            self.create_alarm(self.alarms_frame, alarm_text, index)

        self.alarms_frame.config(borderwidth=15, relief='sunken')
        self.alarms_frame.grid(column=1, row=0, sticky="nsew")
   
        add_button.grid(column=2, row=0, padx=5, pady=1)
        add_button.config(command=lambda f=self.alarms_frame: self.add_alarm(f))

        return self.alarms_frame
    #create all alarms etc. it should be from config

    def create_frames_for_alarm(self, append):
        self.__create_alarm_boxes_frame(append)
        self.__create_edit_alarm_frame(append)
    #create inside frames for editing and normal alarms

    def edit_alarm(self, alarm, alarm_config_txt):
        def save_alarm(what_save, hour, snd_save):
            def info_save(remove=False):
                info_btn_save = ttk.Label(self.edit_frame)
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
            self.save_config(self.config_name, self.sect_alarm_n, alarm_config_txt[0], new_alarm.replace("\n", '#'))
            # add hours and days to editing alarm

        def clear_edit_frame():
            for widgets in self.edit_frame.winfo_children():
                widgets.destroy()
        # create empty array for checkboxes
        clear_edit_frame()
        self.music_list.clear()
        for file in glob.glob(f"{self.sounds_dir}/*.mp3"):
            self.music_list.append(file)
        # clear everything inside edit box
        ttk.Label(self.edit_frame, anchor='center', width=20,
                  font=("default", 20), text=f' {alarm["text"]}'
                  ).grid(column=1, row=0, sticky='ns')
        alarm_text = alarm['text'].split("\n")
        # ttk.Label(self.edit_frame, padding=20, text=f' {b["text"]}').pack(side='top', expand=False)
        # text about what alarm is edited (i'll create these names later)
        hours = tk.Entry(self.edit_frame, bd=1, width=10, font=("default", 40))
        hours.grid(column=1, row=2, sticky='ns')
        hour_text = alarm_text[0].split(":")
        hours.insert(0, f"{hour_text[0]}:{hour_text[1]}:{hour_text[2]}")

        selected_snd = tk.StringVar()
        selected_snd.set(alarm_text[2])
        choose_music = tk.OptionMenu(self.edit_frame, selected_snd, "",*self.music_list)
        choose_music.grid(column=2, row=0)
        choose_music.config()

        # create hour Entry
        # add it to grid
        # add hour from alarm (take text from alarm_button and split it with space and :) that is editing
        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 15))
        # only style, maybe i can change it later
        save_btn = ttk.Button(self.edit_frame, text="Save", padding=25, style='my.TButton')
        save_btn.config(command=lambda timer=alarm, h=hours: save_alarm(timer, h, selected_snd.get()))
        save_btn.grid(column=2, row=2, sticky="w")
        # save editing alarm button and add to grid

        for inx, day in enumerate(self.day_names):
            self.check_days[inx] = ttk.Checkbutton(self.edit_frame, text=day)
            if day in alarm['text']:
                self.check_days[inx].config(variable=self.check_day)
            self.check_days[inx].grid(row=5 + inx, column=1, sticky='w')
    # this loop is creating each day of the week and add it to checkbutton in array and add to grid
   
    def delete_alarm_box(self, alarm, owner, alarm_text):
            def clear_edit_frame():
                for widgets in self.edit_frame.winfo_children():
                    widgets.destroy()

            print(f"[delete_alarm_box]: alarm: {alarm} - owner: {owner}")
            self.save_config(self.config_name, self.sect_alarm_n, alarm_text[0],'', False, True)
            alarm.destroy()
            owner.destroy()
            clear_edit_frame()
    # that's function that is destroying described above

    def create_alarm(self, append, text, row_alarm):
        config_alarm_text = text.split("/") 
        # plan is that program will read config file at the start and check
        # how many alarms is used and create them at start of program
        # if there are none, it will load default fe. 5 alarms
        def toggle_alarm(e, alarm):
            text_alarm = self.read_config(self.config_name, self.sect_alarm_n, config_alarm_text[0])
            if alarm['state'] == 'disabled':
                alarm.config(state="normal") 
                
                self.save_config(self.config_name, self.sect_alarm_n, config_alarm_text[0], text_alarm.replace("disabled","normal"))
                return
            self.save_config(self.config_name, self.sect_alarm_n, config_alarm_text[0], text_alarm.replace("normal","disabled"))
            alarm.config(state="disabled")
        height = 3
        width = 30
        
        alarm_box = tk.Button(append, text=config_alarm_text[1], width=width, height=height, name=f"alarm_box{row_alarm}")
        delete_alarm = tk.Button(append, text='x', height=height // 2, width=width // 5)
 
        alarm_box.grid(column=0, row=row_alarm + 2)
        alarm_box.config(state=config_alarm_text[2], command=lambda btn=alarm_box, alarm_text=config_alarm_text: self.edit_alarm(btn, alarm_text))


        alarm_box.bind("<Button-3>",lambda event, alarm=alarm_box: toggle_alarm(event, alarm))

        delete_alarm.grid(column=2, row=row_alarm + 2, padx=5, pady=1, sticky='w')
        delete_alarm.config(command=lambda btn=alarm_box, dlt=delete_alarm, alarm_text=config_alarm_text: self.delete_alarm_box(btn, dlt, alarm_text))

        return alarm_box
    
    # delete buttons that are right near alarm that user want to delete
    # the buttons are calling function delete_alarm_box which are deleting
    # them and 'their' alarm to which they are bounded to


    def add_alarm(self, frame):
     # this function is for adding new alarm, which maybe should be here, idk
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today_name = now.strftime("%a")

        row_alarm_box = frame.grid_size()[1]
        alarm_text = f"alarm_box{row_alarm_box}/"+dt_string + "\n" + today_name + "\nNone/disabled"
        name_alarm = self.create_alarm(frame, alarm_text, row_alarm_box)
        config_alarm_txt = alarm_text.split("/")[1].replace("\n", '#') +"/"+ alarm_text.split("/")[2].replace("\n", '#')
        self.save_config(self.config_name, self.sect_alarm_n, f"alarm_box{row_alarm_box}", config_alarm_txt, True)
    # function which for add new alarm box

    def check_alarms(self):
        alarms = []
        for alarm in self.alarms_frame.grid_slaves():
            if "alarm_box" not in str(alarm):
                continue
            if alarm['state'] == "normal":
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

        top = tk.Toplevel(self.app_window)
        top.geometry("750x250")
        top.title(text)
        top.overrideredirect(True)
        if(sound != None):
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
    # plan taki:
    # wyskakuje nowe okno(ktore moze miga?) pokazuje ze czas przepylnal i jest tam wiadomosc(jesli byla napisana)
    # muzyka dzwiek gra przez caly czas az do momentu max. dzwieku
    # po tym czasie zostaje sam alarm bez dzwieku
    # tutaj skonczylem sprawdzic jak to z klasami i co pozmieniac ale moze pozniej
    # klasa1: tworzy framy i ustawia
    # klasa2: tworzy alarm i edity itd?