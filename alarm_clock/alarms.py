from turtle import back
from numpy import delete
import pkg_resources
pkg_resources.require("playsound==1.2.2")
from playsound import playsound
import multiprocessing
import tkinter as tk
from tkinter import PhotoImage, ttk
from datetime import datetime
from datetime import timedelta
import glob2 as glob


class AlarmsProperties:
    ALARM_PREFIX = 'alarm_box'
    DELETE_STRING = 'X'
    IMAGE_NAME = 'alarms.png'
    TIME = 'time'
    DAYS = 'days'
    SOUND = 'sound'
    STATE = 'state'

class Alarms(tk.Frame):
    def __init__(self, root, app_properties, json_conf, json_alarms, *args, **kwargs):
        self._root = root
        self.app_prop = app_properties
        self.json_conf = json_conf
        self.json_alarms = json_alarms
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.edit_frame = self.EditAlarm(self)
        self.alarms_frame = tk.Frame(self, background = self.json_conf["bg_alarms"])
        
        #this should be in class Alarms -> alarmslist
        self.btn_big = PhotoImage(file=f'{self.app_prop.IMAGES_DIR}/{AlarmsProperties.IMAGE_NAME}')
        self.btn_med = self.btn_big.subsample(5,2)
        self.btn_width_no_height = self.btn_big.subsample(1,2)
        
        
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
        self.alarms_frame.grid(row=0, column=1, sticky='nsew')
        self.edit_frame.grid(row=0, column =0, sticky='nsew')
        self.config(background=self.json_conf['bg_alarms'])
        
    def create_image_button(self, append, text, image, name=''):
        return tk.Button(append, text=text, 
                                image = image,
                                highlightthickness = 0, bd = 0,
                                activebackground=self.json_conf["bg_alarms"],
                                activeforeground=self.json_conf["fg_buttons"],
                                compound='center',
                                bg=self.json_conf["bg_alarms"],
                                border=0,
                                fg=self.json_conf["fg_buttons"],
                                name=name
                                
                                )
        

    def __create_alarm_boxes_frame(self, width=30):
        tk.Label(self.alarms_frame, text='Alarms', 
                background=self.json_conf['lbl_alarms_bg'], 
                justify='center',
                borderwidth=1, relief="solid",
                image=self.btn_width_no_height,
                compound='center',
                bg=self.json_conf["bg_alarms"],
                border=0,
                fg=self.json_conf["fg_buttons"]
                ).grid(column=0, row=0, sticky='new')
        
        # add buttons for adding new alarms
        add_button = self.create_image_button(self.alarms_frame, 'Add', self.btn_width_no_height, 'add_btn')
        
        self.alarms_frame.config(borderwidth=5, relief='sunken')
        self.alarms_frame.grid(column=1, row=1, sticky="nsew")
        self.alarms_frame.columnconfigure(0, weight=1)
        self.alarms_frame.columnconfigure(1, weight=1)
        add_button.grid(column=2, row=0, padx=5, pady=1)
        add_button.config(command=lambda f=self.alarms_frame: self.add_alarm(f))
        
    def refresh_alarms(self):
        self.alarms_frame.grid_slaves().clear()
        for row, alarm in enumerate(self.json_alarms.section): 
            self.create_alarm(self.alarms_frame, alarm, row)

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
        #TODO HERE
        
        alarm_format = f"{alarm_text[AlarmsProperties.TIME]} \n {' '.join([str(elem) for elem in alarm_text[AlarmsProperties.DAYS]])} \n {alarm_text[AlarmsProperties.SOUND]}"
        alarm_box = self.create_image_button(append, alarm_format, self.btn_big, f"{AlarmsProperties.ALARM_PREFIX}_{row_alarm}")

        delete_alarm = self.create_image_button(append, AlarmsProperties.DELETE_STRING, self.btn_med, f"delete_{AlarmsProperties.ALARM_PREFIX}{row_alarm}")
 
        alarm_box.grid(column=0, row=row_alarm + 2)
        alarm_box.config(state=alarm_text[AlarmsProperties.STATE], command=lambda alarm_json=alarm_json, alarm_box=alarm_box: self.edit_frame.edit(alarm_json, alarm_box))

        alarm_box.bind("<Button-3>", lambda event, alarm_box=alarm_box: toggle_alarm(event, alarm_box))

        delete_alarm.grid(column=1, row=row_alarm + 2, padx=5, pady=1, sticky='w')
        delete_alarm.config(command=lambda alarm_json=alarm_json : [self.remove_alarm_box(alarm_json), alarm_box.destroy(), delete_alarm.destroy()])
        return alarm_box

    def clear_edit_frame(self):
        for widgets in self.edit_frame.winfo_children():
            widgets.destroy()

    def remove_alarm_box(self, json_alarm):
            self.json_alarms.pop_section(json_alarm)
            self.clear_edit_frame()

    def add_alarm(self, frame):
     # this function is for adding new alarm, which maybe should be here, idk
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today_name = now.strftime("%a")
        #FIXME for now its only day in engluish to need to change that
        row_alarm_box = frame.grid_size()[1]
        print(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}")
        #FIXME random alarm_box number 
        self.json_alarms.modify_section(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}", AlarmsProperties.TIME, dt_string)
        self.json_alarms.modify_section(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}", AlarmsProperties.DAYS, [today_name])
        self.json_alarms.modify_section(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}", AlarmsProperties.SOUND, 'none')
        self.json_alarms.modify_section(f"{AlarmsProperties.ALARM_PREFIX}{row_alarm_box}", AlarmsProperties.STATE, 'disabled')
        self.refresh_alarms()
    # function which for add new alarm box

    def check_alarms(self):
        alarms = []
        for alarm in self.alarms_frame.grid_slaves():
            if AlarmsProperties.ALARM_PREFIX not in str(alarm):
                continue
            if alarm[AlarmsProperties.STATE] == "normal":
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
        now_time = dt_string + "\n" + today[0:3]
        for alarm in self.json_alarms.section:
            alarm_prop = self.json_alarms.section[alarm]
            if alarm_prop['state'] == 'normal':
                if today[0:3] in  alarm_prop['days']:
                    if dt_string in alarm_prop['time'] :
                        self.AlarmPopup(self, alarm_prop)
        self.alarms_frame.after(1000, self.set_alarms)


    class AlarmPopup(tk.Tk):
        def __init__(self, root, alarm_AlarmsProperties, *args, **kwargs):
            tk.Toplevel.__init__(self, *args, **kwargs)
            self._root = root
            self.sound_process = None
            self.geometry("750x250")
            self.title('Settings')
            self.mute_sound_text = 'Mute sound'
            self.play_sound_text = 'Play sound'
            alarm_format = f"{alarm_AlarmsProperties[AlarmsProperties.TIME]}\n{' '.join([str(day) for day in alarm_AlarmsProperties[AlarmsProperties.DAYS]])}\n {alarm_AlarmsProperties[AlarmsProperties.SOUND]}  "

            ttk.Label(self, text=alarm_format, font='Mistral 18 bold').pack(side='left')
            ttk.Button(self, text="Stop alarm", command=lambda: self.stop_alarm()).pack(side='right')    
            ttk.Button(self, text="Snooze").pack(side='right') #,command=lambda alarm=text: [snooze_alarm(), stop_alarm()]
                #    ).pack(side='right')
            mute_sound_btn = ttk.Button(self, text = self.mute_sound_text )
            if AlarmsProperties.SOUNDS_EXT in alarm_AlarmsProperties[AlarmsProperties.SOUND]:
                music_to_play = f"{self.app_prop.SOUND_DIR}/{alarm_AlarmsProperties[AlarmsProperties.SOUND]}"
                mute_sound_btn.config(command=lambda mute_sound_btn=mute_sound_btn, music_to_play=music_to_play : self.mute_sound(mute_sound_btn, music_to_play))
                mute_sound_btn.pack(side='right')

                self.start_sound(music_to_play)
            # if sounds != none  toggle music button and play music threading
        
        def stop_alarm(self):
            self.destroy()
            if self.sound_process != None:
                self.sound_process.kill()

        def mute_sound(self, btn, music_to_play):
            self.sound_process.kill()
            if btn['text'] ==  self.mute_sound_text:
                btn['text'] = self.play_sound_text 
                return
            self.start_sound(music_to_play)
            btn['text'] =  self.mute_sound_text

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
            self.img_edit = PhotoImage(file=f"{root.app_prop.IMAGES_DIR}/{AlarmsProperties.IMAGE_NAME}")
            self.app_prop = root.app_prop
            tk.Frame.__init__(self, root, background='blue', borderwidth=5,relief='sunken', *args, **kwargs)
            #FIXME blue from config
            self.json_conf = self._root.json_conf
            self.json_alarms = self._root.json_alarms
            self.check_days = None
            self.checked_days = None

        def edit(self, json_alarm, alarm_box):
            self.check_days = self._root.check_days
            self.checked_days = self._root.checked_days

            alarm_format = self.json_alarms.section[json_alarm]
            alarm_format_lbl = f" {alarm_format[AlarmsProperties.TIME]} \n {' '.join([str(elem) for elem in alarm_format[AlarmsProperties.DAYS]])} \n {alarm_format[AlarmsProperties.SOUND]}"

            def create_alarm_name_lbl(txt, anchor='center'):
                alarm_label = tk.Label(self, anchor=anchor,
                                        image = self.img_edit,
                                        background=self.json_conf['bg_edit'],
                                        fg=self.json_conf['fg_edit'],
                                        compound='center',
                                        text=txt
                                    )
                alarm_label.grid(column=1, row=0, sticky='ns')   
                return alarm_label

            def create_hours_entry(time, font_size=self.json_conf['hours_entry_font_size'], bg=self.json_conf['hours_entry_bg'], width=10):
                hours = tk.Entry(self, bd=1, width=width, 
                                font=("default", font_size), 
                                background=bg
                                )
                hours.insert(0, f"{time}")
                hours.grid(column=1, row=2, sticky='nsew')
                return hours

            def create_sound_list_from_dir():
                music_list = []
                for file in glob.glob(f"{self.app_prop.SOUND_DIR}/*{self.app_prop.SOUNDS_EXT}"):
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
                selected_snd.set(self.app_prop.SOUND_DIR+'\\'+sound)
                choose_music = ttk.OptionMenu(self, selected_snd, "",*create_sound_list_from_dir(), style='my.TMenubutton')
                choose_music.grid(column=2, row=0, sticky="nsew")
                choose_music.config()
                return selected_snd

            def create_save_button(hours_entry, selected_snd):
                save_btn = tk.Button(self, text="Save", 
                                    background=self.json_conf['save_btn_bg'],
                                    activebackground=self.json_conf['save_btn_bg_active'], 
                                    font=('Helvetica', self.json_conf['save_btn_font_size'])
                                    )
                save_btn.config(command=lambda alarm_json=json_alarm, alarm_box=alarm_box, hour=hours_entry: save_alarm(alarm_json, alarm_box, hour, selected_snd.get()))
                save_btn.grid(column=2, row=2, sticky="nsew")
    
            def create_checkbox_days():
                day_names = self.json_conf['day_name']

                checkbox_days_frame = tk.Frame(self)
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
    

    #TODO ADD BUTTONS IMG / CHECK ENTRY (image or sth) smae as SELECT SOUND
    # after all images commit and push 
    # remove unused thinsgs in config.json
    # some changes in functions and mostly changed backgrounds into images
    # comment that in settings json {{comment: 'x y etc ' }}
    
    