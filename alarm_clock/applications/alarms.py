
import datetime
import glob
import random
import re
import tkinter as tk
from tkinter import PhotoImage, XView
from turtle import width
import vlc
from my_widgets import *
from app_properties import *

# TODO Random alarm from list? (could be done, not necessary for now)


class Alarms(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_alarm = ConfigProperties.ALARMS_OPTIONS
        self.alarms_list = ConfigProperties.ALARMS

        tk.Frame.__init__(self, root, *args, **kwargs)

        self.bg_alarms = self.config_alarm["bg_color_alarms"]["value"]
        self.fg_alarms = self.config_alarm["fg_color_alarms"]["value"]
        self.snooze_time = self.config_alarm["snooze_time"]["value"]
        self.day_names = self.config_alarm["day_name"]["value"].split(",")

        self.scrollable_alarms = MyScrollableFrame(
            self, self.bg_alarms)
        self.alarms_frame = self.scrollable_alarms.frame

        self.edit_alarm_obj = None
        self.alarms_frame.columnconfigure(0, weight=1)
        self.alarms_frame.columnconfigure(1, weight=1)
        self.alarms_frame.columnconfigure(2, weight=1)
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
        self.scrollable_alarms.grid(row=0, column=0, sticky=tk.NSEW)
        self.config(background=self.bg_alarms)

    def __create_alarm_boxes_frame(self):
        alarm_title_lbl = MyLabel(
            self.alarms_frame, "Alarms",
            self.fg_alarms, self.bg_alarms,
            image=self.small_widgets,
        )

        add_button = MyButton(
            self.alarms_frame, "Add",
            self.fg_alarms,  self.bg_alarms,
            image=self.small_widgets,
            name="add_alarm_btn",
        )

        add_button.config(command=lambda: self.add_alarm())
        alarm_title_lbl.grid(column=0, row=0, sticky=tk.NSEW)
        add_button.grid(column=4, row=0, padx=5, pady=1, sticky=tk.W)

    def refresh_alarms(self):
        self.alarms_frame.grid_slaves().clear()
        for row, alarm in enumerate(self.alarms_list.section):
            self.create_alarm(self.alarms_frame, alarm, row)

    def toggle_alarm(self, alarm_box, alarm_text, alarm_json):
        state_now = ""
        if alarm_box[ConfigProperties.STATE] == "disabled":
            state_now = "normal"
        else:
            state_now = "disabled"
        alarm_box[ConfigProperties.STATE] = state_now
        alarm_text[ConfigProperties.STATE] = state_now
        self.alarms_list.modify_section(
            alarm_json, ConfigProperties.STATE, state_now)

    def create_alarm(self, append, alarm_json, row_alarm):
        alarm_text = self.alarms_list.section[alarm_json]

        alarm_format = f'''{alarm_text[ConfigProperties.TIME]}
{' '.join([str(elem) for elem in alarm_text[ConfigProperties.DAYS]])}
{alarm_text[ConfigProperties.SOUND]}
Snooze: {alarm_text[ConfigProperties.SNOOZE_TIME]}
V:{alarm_text[ConfigProperties.VOLUME_ALARM]}
'''
        alarm_box = MyButton(
            append,
            alarm_format,
            self.fg_alarms,
            self.bg_alarms,
            image=self.btn_default,
            wraplength=self.btn_default.width(),
            name=f"{AppProperties.ALARM_PREFIX}_{row_alarm}",
        )
        delete_alarm = MyButton(
            append,
            AppProperties.DELETE_STRING,
            self.fg_alarms,
            self.bg_alarms,
            image=self.btn_subsampl52,
            name=f"delete_{AppProperties.ALARM_PREFIX}{row_alarm}",
        )

        alarm_box.config(
            state=alarm_text[ConfigProperties.STATE],
            command=lambda alarm_json=alarm_json, alarm_box=alarm_box: self.edit_alarm(
                alarm_json, alarm_box
            ),
        )
        delete_alarm.config(
            command=lambda alarm_json=alarm_json: [
                self.remove_alarm_box(alarm_json),
                alarm_box.destroy(),
                delete_alarm.destroy(),
            ]
        )

        alarm_box.bind(
            "<Button-3>",
            lambda event, alarm_box=alarm_box, alarm_text=alarm_text, alarm=alarm_json: self.toggle_alarm(
                alarm_box, alarm_text, alarm
            ),
        )

        alarm_box.grid(column=0, columnspan=4, row=row_alarm + 2)
        delete_alarm.grid(column=5, row=row_alarm + 2,
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
        now = datetime.datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today_name = self.day_names[int(now.strftime("%w")) - 1]
        row_alarm_box = self.alarms_frame.grid_size()[1]
        self.alarms_list.add_alarm(
            f"{AppProperties.ALARM_PREFIX}_{row_alarm_box}_{random.randint(0,100)}",
            dt_string,
            [today_name],
            "none",
            self.snooze_time,
            50,
            "",
        )
        self.refresh_alarms()

    def debug_alarm_add(self, frame):
        now = datetime.datetime.now() + datetime.timedelta(seconds=2)
        dt_string = now.strftime("%H:%M:%S")
        today_name = now.strftime("%a")
        row_alarm_box = frame.grid_size()[1]
        self.alarms_list.add_alarm(
            f"{AppProperties.ALARM_PREFIX}{row_alarm_box}",
            dt_string,
            [today_name],
            "3.mp3",
            1,
            "Opis",
        )
        self.refresh_alarms()

    def check_alarms(self):
        alarms = []
        for alarm in self.alarms_frame.grid_slaves():
            if AppProperties.ALARM_PREFIX not in str(alarm):
                continue
            if alarm[ConfigProperties.STATE] == "normal":
                al = alarm["text"].split("\n")
                alarms.append(al)
        for snoozed_alarm in self.snoozed_alarms:
            al = snoozed_alarm.split("\n")
            alarms.append(al)
        return alarms

    # check which alarm is enabled
    def set_alarms(self):
        now = datetime.datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today = self.day_names[int(now.strftime("%w")) - 1]

        for alarm in self.alarms_list.section:
            alarm_prop = self.alarms_list.section[alarm]
            if alarm_prop["state"] == "normal":
                if today in alarm_prop["days"]:
                    if dt_string in alarm_prop["time"]:
                        AlarmPopup(self, alarm_prop)
        self.alarms_frame.after(1000, self.set_alarms)


class AlarmPopup(tk.Tk):
    def __init__(self, root, alarm_popup, *args, **kwargs):
        self.config_alarm = ConfigProperties.ALARMS_OPTIONS
        self.bg = self.config_alarm["bg_color_alarm_popup"]["value"]
        self.fg = self.config_alarm["fg_color_alarm_popup"]["value"]
        self.alarm_popup = alarm_popup
        self.snooze_time = alarm_popup["snooze_time"]
        self.volume_alarm = alarm_popup['volume_alarm']
        tk.Toplevel.__init__(
            self, borderwidth=2, relief="raised", background=self.bg, *args, **kwargs
        )
        self._root = root
        self.eval(f"tk::PlaceWindow {str(self)} center")
        self.sound_play = None
        self.geometry(self.config_alarm["alarm_popup_resolution"]["value"])
        self.protocol("WM_DELETE_WINDOW", self.minimalize)
        self.title(
            f"{self.alarm_popup[ConfigProperties.TIME]} - {self.alarm_popup[ConfigProperties.DESCR]}"
        )
        self.mute_sound_txt = "Mute sound"
        self.play_sound_txt = "Play sound"
        self.img = PhotoImage(file=AppProperties.ALARMS_IMG)
        self.img_button = self.img.subsample(2, 2)
        self.relief_r = ["sunken", "raised", "flat", "ridge", "groove"]
        self.create_popup_widgets()

        if self.config_alarm["animation"]["value"]:
            self.change_relief()

    def minimalize(self):
        self.iconify()

    def create_popup_widgets(self):
        music_to_play = (
            f"{AppProperties.SOUND_DIR}/{self.alarm_popup[ConfigProperties.SOUND]}"
        )
        alarm_format = [
            self.alarm_popup[ConfigProperties.TIME],
            " ".join([str(day)
                     for day in self.alarm_popup[ConfigProperties.DAYS]]),
            self.alarm_popup[ConfigProperties.SOUND],
            self.alarm_popup[ConfigProperties.DESCR],
        ]
        for index, alarm_part in enumerate(alarm_format):

            MyLabel(self, alarm_part, self.fg, self.bg, image=self.img).grid(
                row=index, column=0
            )
        mute_sound_btn = MyButton(
            self, self.mute_sound_txt,
            self.fg, self.bg,
            image=self.img_button,
            name=f"mute_alarm",
        )
        MyButton(
            self, "Stop alarm",
            self.fg, self.bg,
            image=self.img_button, name=f"stop_alarm",
            command=lambda: self.stop_alarm(),
        ).grid(row=0, column=1)

        self.snooze_btn = MyButton(
            self, "Snooze alarm",
            self.fg, self.bg,
            image=self.img_button,
            name=f"snooze_alarm",
        )

        self.snooze_btn.config(
            command=lambda snooze_btn=self.snooze_btn, time=self.snooze_time, snd=music_to_play: self.snooze_alarm(
                snooze_btn, time, snd
            )
        )
        self.snooze_btn.grid(row=0, column=2)
        if self.start_sound(music_to_play):
            mute_sound_btn.config(
                command=lambda mute_sound_btn=mute_sound_btn, music_to_play=music_to_play: self.mute_sound(
                    mute_sound_btn
                )
            )
            mute_sound_btn.grid(row=0, column=3)
        # if sounds != none  toggle music button and play music threading

    def change_relief(self):
        self.config(relief=random.choice(self.relief_r))
        self.after(1000, self.change_relief)

    def stop_alarm(self):
        self.destroy()
        if self.sound_play != None:
            self.sound_play.stop()

    def mute_sound(self, btn):
        self.sound_play.set_pause(1)
        if btn["text"] == self.mute_sound_txt:
            btn["text"] = self.play_sound_txt
            return
        self.sound_play.set_pause(0)
        btn["text"] = self.mute_sound_txt

    def snooze_alarm(self, sn_btn, time, snd):
        snooze_time_now = datetime.datetime.now() + datetime.timedelta(minutes=time)
        time_string = snooze_time_now.strftime("%H:%M:%S")
        sn_btn["text"] = f"Snooze alarm\n {time_string}"
        self.sound_play.stop()
        self.snooze_btn["state"] = "disabled"
        time_ms = time * 60000

        self.minimalize()
        self.after(time_ms, self.start_sound, snd)

    def start_sound(self, snd_to_play):
        self.snooze_btn["state"] = "normal"
        if AppProperties.SOUNDS_EXT in snd_to_play:
            self.sound_play = vlc.MediaPlayer(snd_to_play)
            self.sound_play.audio_set_volume(self.volume_alarm)
            self.sound_play.play()
            return True
        return False


class EditAlarm(tk.Tk):
    def __init__(self, root, alarm, alarm_btn, *args, **kwargs):
        self.img_edit = PhotoImage(file=AppProperties.ALARMS_IMG)
        self.img_check_day = self.img_edit.subsample(5, 4)
        self.btn_title = PhotoImage(file=AppProperties.TITLE_IMG)
        self.btn_action = self.img_edit.subsample(3, 2)
        self.config_edit = ConfigProperties.ALARMS_OPTIONS
        self.alarms_list = ConfigProperties.ALARMS
        self.fg_edit = self.config_edit["fg_color_edit"]["value"]
        self.bg_edit = self.config_edit["bg_color_edit"]["value"]
        self.f_s_hours_entry = self.config_edit["hours_entry_font_size"]["value"]
        self.f_s_select_snd = self.config_edit["select_sound_font_size"]["value"]
        self.font_edit = self.config_edit["font_family_edit"]["value"]
        self.day_names = self.config_edit["day_name"]["value"].split(",")

        tk.Toplevel.__init__(
            self, borderwidth=2, relief="raised",
            background=self.bg_edit,
            *args, **kwargs,
        )
        self.eval(f"tk::PlaceWindow {str(self)} right")
        self.geometry(self.config_edit["alarm_edit_resolution"]["value"])
        self.overrideredirect(True)
        self.checkbox_days = None
        self.checked_days = None
        self.selected_snd = tk.StringVar()
        self.format_title_time = ["Hour", "Minutes", "Seconds"]
        self.hours_entry = []
        self.edit(alarm, alarm_btn)

    def create_edit_entries(self, append, title='', value='', **options):
        entry = MyEntry(
            append, self.fg_edit, self.bg_edit,
            title, self.btn_title,
            value, font=(self.font_edit, self.f_s_hours_entry),
            **options
        )
        return entry

    def sec_min_validation(self, value):
        pattern = r'(0?[0-9]|[1-5][0-9])'
        if re.fullmatch(pattern, value) is None:
            return False
        return True

    def hours_validation(self, value):
        pattern = r'(0?[0-9]|1[0-9]|2[0-3])'
        if re.fullmatch(pattern, value) is None:
            return False
        return True

    def on_invalid(self, entr):
        entr.entry.delete(0, 'end')

    def edit(self, json_alarm, alarm_box):

        self.checkbox_days = []
        self.checked_days = []

        alarm_properties = self.alarms_list.section[json_alarm]
        alarm_format = alarm_properties
        alarm_description = alarm_properties["description"]
        alarm_snooze = alarm_properties["snooze_time"]
        volume = alarm_properties['volume_alarm']
        alarm_format_lbl = f" {alarm_format[ConfigProperties.TIME]} \n {' '.join([str(elem) for elem in alarm_format[ConfigProperties.DAYS]])} \n {alarm_format[ConfigProperties.SOUND]}"
        time_frame = tk.Frame(self)
        sec_min_valid = (self.register(self.sec_min_validation), '%P')
        hours_valid = (self.register(self.hours_validation), '%P')

        hours_split = alarm_format[ConfigProperties.TIME].split(":")
        self.hours_entry.append(
            self.create_edit_entries(time_frame,
                                     self.format_title_time[0],
                                     hours_split[0], width=8,
                                     validate="focusout", validatecommand=hours_valid))
        self.hours_entry[0].entry.config(
            invalidcommand=lambda: self.on_invalid(self.hours_entry[0]))
        self.hours_entry.append(
            self.create_edit_entries(time_frame,
                                     self.format_title_time[1],
                                     hours_split[1], width=8,
                                     validate="focusout", validatecommand=sec_min_valid)
        )
        self.hours_entry[1].entry.config(
            invalidcommand=lambda: self.on_invalid(self.hours_entry[1]))
        self.hours_entry.append(
            self.create_edit_entries(time_frame,
                                     self.format_title_time[2],
                                     hours_split[2], width=8,
                                     validate="focusout", validatecommand=sec_min_valid)
        )
        self.hours_entry[2].entry.config(
            invalidcommand=lambda: self.on_invalid(self.hours_entry[2]))

        description_entry = self.create_edit_entries(self,
                                                     "Description", alarm_description)

        snooze_time_entry = self.create_edit_entries(self,
                                                     "Snooze Time", alarm_snooze, width=3)

        volume_entry = self.create_edit_entries(self,
                                                "Volume", volume, width=3)

        """ ALARM TITLE  """
        MyLabel(
            self, alarm_format_lbl, self.fg_edit, self.bg_edit, image=self.img_edit
        ).grid(column=0, row=0, sticky=tk.NSEW)
        """ ALARM TITLE  """
        save_btn = MyButton(
            self,
            "Save",
            self.fg_edit,
            self.bg_edit,
            image=self.btn_action,
            name=f"save_alarm",
        )
        cancel_btn = MyButton(
            self,
            "Cancel",
            self.fg_edit,
            self.bg_edit,
            image=self.btn_action,
            name=f"cancel_btn",
        )
        choose_music = self.create_sound_selection(
            alarm_format[ConfigProperties.SOUND])

        cancel_btn.config(command=lambda: self.edit_quit())
        save_btn.config(
            command=lambda: self.save_alarm(
                json_alarm,
                alarm_box,
                description_entry.entry.get(),
                self.selected_snd.get(),
                volume_entry.entry.get(),
                snooze_time_entry.entry.get(),
            )
        )
        checkbox_days_frame = self.create_checkbox_days(alarm_format)

        description_entry.grid(column=0, row=1, sticky=tk.NSEW)
        for entr in self.hours_entry:
            entr.pack(side=tk.LEFT)
        time_frame.grid(column=0, row=2, sticky=tk.NSEW)
        snooze_time_entry.grid(column=0, row=3, sticky=tk.NSEW)
        volume_entry.grid(column=1, row=2, sticky=tk.NSEW)
        cancel_btn.grid(column=0, row=5, sticky=tk.NSEW)
        save_btn.grid(column=1, row=5, sticky=tk.NSEW)
        choose_music.grid(column=1, row=0)

        checkbox_days_frame.grid(
            row=4, column=0, columnspan=len(self.day_names), sticky=tk.NSEW
        )

    def create_sound_list_from_dir(self):
        music_list = []
        for file in glob.glob(f"{AppProperties.SOUND_DIR}/*{AppProperties.SOUNDS_EXT}"):
            music_list.append(file)
        return music_list

    def create_sound_selection(self, sound):
        self.selected_snd.set(AppProperties.SOUND_DIR + "\\" + sound)
        choose_music = MyOptionMenu(self, self.fg_edit, self.bg_edit, 'Select sound',
                                    self.btn_title, self.font_edit, self.f_s_select_snd,
                                    self.img_edit, self.selected_snd,
                                    *self.create_sound_list_from_dir(),
                                    wraplength=self.img_edit.width()
                                    )
        return choose_music

    def from_entries_to_hour(self):
        alarm_format = ''
        for entr in self.hours_entry:
            alarm_format += entr.entry.get()+":"
        return alarm_format[:-1]

    def save_alarm(self, alarm_json, alarm_box, descr, snd_save, volume, snooze_time):
        new_days = []
        hour = self.from_entries_to_hour()
        new_sound = snd_save.split("\\")[1]
        for day_check in self.checkbox_days:
            if "selected" in day_check.state():
                new_days.append(day_check["text"])
        alarm_format = f"{hour}\n"
        alarm_format += f"{new_sound}\n"
        alarm_format += f"{' '.join([str(elem) for elem in new_days])}\n"
        alarm_format += f"Snooze: {snooze_time}\n"
        alarm_format += f"V:{volume}\n"
        alarm_box["text"] = alarm_format

        self.alarms_list.modify_alarm(
            alarm_json, hour, new_days, new_sound, snooze_time, volume, descr
        )

        self.edit_quit()

    def create_checkbox_days(self, alarm_format):

        checkbox_days_frame = tk.Frame(self, bg=self.bg_edit)

        s_check_bx = ttk.Style()
        s_check_bx.configure(
            "my.TCheckbutton",
            image=self.img_check_day,
            background=self.bg_edit,
            foreground=self.fg_edit,
        )

        # save editing alarm button and add to grid
        self.checkbox_days.clear()
        self.checked_days.clear()
        for indx, day in enumerate(self.day_names):
            check_button_day = ttk.Checkbutton(
                checkbox_days_frame,
                compound=tk.CENTER,
                text=day,
                style="my.TCheckbutton",
            )
            if day in alarm_format[ConfigProperties.DAYS]:
                self.checked_days.append(tk.IntVar(value=1))
                check_button_day.config(variable=self.checked_days[indx])
            else:
                self.checked_days.append(tk.IntVar(value=0))
            check_button_day.grid(row=0, column=indx, sticky=tk.W)
            self.checkbox_days.append(check_button_day)
        return checkbox_days_frame
        # this loop is creating each day of the week and add it to checkbutton in array and add to grid

    def edit_quit(self):
        self.destroy()
