import pkg_resources
pkg_resources.require("playsound==1.2.2")
from playsound import playsound
import multiprocessing
import os
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from datetime import timedelta
import glob2 as glob


class Alarms:
    def __init__(self, app_window, alarms, style, day_names, snoozed_time):
        # init(self, aplication tk, alarms from config, style from user, day_names from user, snooze time from user)
        self.alarms = alarms
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

    def __create_edit_alarm_frame(self, append):
        self.edit_frame = ttk.Frame(append, style=self.styleName, borderwidth=15, relief='sunken')
        self.edit_frame.grid(column=0, row=0, sticky="nsew")

    def __create_alarm_boxes_frame(self, append, config_sound, count, width=30):
        self.alarms_frame = ttk.Frame(append, style=self.styleName)
        
        ttk.Label(self.alarms_frame, text='Alarms' , justify='center', font=('calibri', 25, 'bold'),
                  borderwidth=1, relief="solid").grid(column=0, row=0, sticky='new')
        
        # add buttons for adding new alarms
        add_button = tk.Button(self.alarms_frame, text="Add", height=1, width=width)
        
        # debug alarm is 5 sec from start program
        # for loop for every alarm giving in config or default
        # should now change it to config 
        for i in range(count):
            seconds = 12 + (i * 25)
            soon = datetime.now() + timedelta(seconds=seconds)
            dt_string = soon.strftime("%H:%M:%S")
            today = soon.strftime("%a")
            self.create_alarm(self.alarms_frame, f"{dt_string}\n{today}\n{config_sound}", i)

        self.alarms_frame.config(borderwidth=15, relief='sunken')
        self.alarms_frame.grid(column=1, row=0, sticky="nsew")
   
        add_button.grid(column=2, row=0, padx=5, pady=1)
        add_button.config(command=lambda f=self.alarms_frame: self.add_alarm(f))

        return self.alarms_frame

    def create_frames_for_alarm(self, append, config_sound, config_count):
        self.__create_alarm_boxes_frame(append, config_sound, config_count)
        self.__create_edit_alarm_frame(append)

    def edit_alarm(self, alarm):
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
            # add hours and days to editing alarm

        def clear_edit_frame():
            for widgets in self.edit_frame.winfo_children():
                widgets.destroy()
        # create empty array for checkboxes
        clear_edit_frame()
        self.music_list.clear()
        for file in glob.glob("sounds/*.mp3"):
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
   
    def delete_alarm_box(self, alarm, checkbox, owner):
            def clear_edit_frame():
                for widgets in self.edit_frame.winfo_children():
                    widgets.destroy()

            print(f"[delete_alarm_box]: alarm: {alarm} - owner: {owner}")
            alarm.destroy()
            owner.destroy()
            checkbox.destroy()
            clear_edit_frame()
        # that's function that is destroying described above

    def create_alarm(self, append, text, row_alarm): 
        # state = 'disabled' should be from config: 
        # is alarm on or off by user

        # plan is that program will read config file at the start and check
        # how many alarms is used and create them at start of program
        # if there are none, it will load default fe. 5 alarms
        def toggle_alarm(alarm, checkbox):
            if "selected" in checkbox.state():
                alarm.config(state="normal")
                return
            alarm.config(state="disabled")

        height = 3
        width = 30
        delete_txt = "x"
        alarm_box = tk.Button(append, text=text, width=width, height=height, name=f"alarm_box{row_alarm}")
        delete_alarm = tk.Button(append, text=delete_txt, height=height // 2, width=width // 5)
        turned_on_check = ttk.Checkbutton(append, text="Turned on")

        alarm_box.grid(column=0, row=row_alarm + 2)
        alarm_box.config(state="disabled", command=lambda btn=alarm_box: self.edit_alarm(btn))
   
        turned_on_check.grid(column=2, row=row_alarm + 2, padx=5, pady=1, sticky='w')
        turned_on_check.config(command=lambda btn=alarm_box, check=turned_on_check: toggle_alarm(btn, check))

        delete_alarm.grid(column=4, row=row_alarm + 2, padx=5, pady=1, sticky='w')
        delete_alarm.config(command=lambda btn=alarm_box, ch_bx=turned_on_check, dlt=delete_alarm: self.delete_alarm_box(btn, ch_bx, dlt))
        # delete buttons that are right near alarm that user want to delete
        # the buttons are calling function delete_alarm_box which are deleting
        # them and 'their' alarm to which they are bounded to

    def add_alarm(self, frame):
     # this function is for adding new alarm, which maybe should be here, idk
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today_name = now.strftime("%a")
        alarm_text = dt_string + "\n" + today_name + "\n None"
        row_alarm_box = frame.grid_size()[1]
        self.create_alarm(frame, alarm_text, row_alarm_box)
   
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
        alarms.after(1000, self.set_alarms)
        # plan taki:
        # wyskakuje nowe okno(ktore moze miga?) pokazuje ze czas przepylnal i jest tam wiadomosc(jesli byla napisana)
        # muzyka dzwiek gra przez caly czas az do momentu max. dzwieku
        # po tym czasie zostaje sam alarm bez dzwieku
        # tutaj skonczylem sprawdzic jak to z klasami i co pozmieniac ale moze pozniej
        # klasa1: tworzy framy i ustawia
        # klasa2: tworzy alarm i edity itd?