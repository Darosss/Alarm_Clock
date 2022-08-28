import multiprocessing
import random
import re
from my_widgets import *
from app_properties import *
import tkinter as tk
from tkinter import PhotoImage
from playsound import playsound
import datetime
import threading


class Timer(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self.config_timer = ConfigProperties.TIMER_OPTIONS
        self.saved_times = ConfigProperties.SAVED_TIMES
        self.bg_timer = self.config_timer["bg_color_timer"]["value"]
        self.fg_timer = self.config_timer["fg_color_timer"]["value"]
        self.f_s_timer = self.config_timer["font_size_timer"]["value"]
        self.font_timer = self.config_timer["font_timer"]["value"]
        self.sound_timer = self.config_timer["sound_timer"]["value"]
        tk.Frame.__init__(self, root, borderwidth=2, *args, **kwargs)
        self.btn_default = PhotoImage(file=AppProperties.TIMER_IMG)
        self.low_height_widgets = self.btn_default.subsample(3, 2)
        self.btn_title = PhotoImage(file=AppProperties.TITLE_IMG)

        self.timer_frame = tk.Frame(
            self, borderwidth=1, background=self.bg_timer, relief="sunken"
        )
        self.start_pause_btn = None
        self.stop_btn = None
        self.entry_desc = None
        self.delay_entry = None
        self.time_entry = []
        self.timer_delay = None
        self.selected_snd = tk.StringVar()
        self.saved_frame = tk.Frame(
            self, borderwidth=1, background=self.bg_timer, relief="sunken"
        )

        self.timer_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.saved_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.is_counting = None
        self.timer_time = [0, 0, 0, 0, 0]
        self.timer_start_value = 0

        self.time_frame = tk.Frame(self.saved_frame, background=self.bg_timer)
        for i in range(3):
            self.time_frame.columnconfigure(i, weight=1)

        self.create_savedtimes_widgets()
        self.time_frame.pack(side=tk.TOP, fill="x", expand=True)
        self.refresh_saved_times()
        self.create_timer_widgets()

    def refresh_saved_times(self):
        for slave in self.time_frame.grid_slaves():
            if "time_value" in slave.winfo_name():
                slave.destroy()

        for index, section in enumerate(
            sorted(
                self.saved_times.section[AppProperties.TIMER_PREFIX], reverse=True)
        ):
            sec_lbl = MyLabel(
                self.time_frame,
                str(index + 1) + ". " + section,
                self.fg_timer,
                self.bg_timer,
                name=section + "/time_value_data",
                borderwidth=2,
                relief="raised",
                font=(self.font_timer, self.f_s_timer),
            )
            # Data and index
            sec_lbl.grid(column=0, row=index + 1, sticky=tk.NSEW)
            MyLabel(
                self.time_frame,
                self.saved_times.section[AppProperties.TIMER_PREFIX][section]["value"],
                self.fg_timer,
                self.bg_timer,
                borderwidth=2,
                relief="raised",
                font=(self.font_timer, self.f_s_timer),
                name="time_value_time" + str(index),
            ).grid(column=1, row=index + 1, sticky=tk.NSEW)
            # Time
            MyLabel(
                self.time_frame,
                self.saved_times.section[AppProperties.TIMER_PREFIX][section][
                    "description"
                ],
                self.fg_timer,
                self.bg_timer,
                font=(self.font_timer, self.f_s_timer),
                name="time_value_description" + str(index),
                borderwidth=2,
                relief="raised",
                wraplength=100,
                justify=tk.LEFT,
            ).grid(column=2, row=index + 1, sticky=tk.NSEW)
            # Description
            MyButton(
                self.time_frame,
                "x",
                self.fg_timer,
                self.bg_timer,
                image=self.low_height_widgets,
                font=(self.font_timer, self.f_s_timer),
                name="time_value_delete" + str(index),
                command=lambda sect_nam=sec_lbl.winfo_name().split("/")[
                    0
                ]: self.pop_and_refresh(sect_nam),
            ).grid(column=3, row=index + 1, sticky=tk.E)

    def pop_and_refresh(self, sect_name):
        self.saved_times.pop_section(AppProperties.TIMER_PREFIX, sect_name)
        self.refresh_saved_times()

    def create_entry(self, title='', value='', **options):
        entry = MyEntry(
            self.timer_frame,
            self.fg_timer, self.bg_timer,
            title, self.btn_title,
            value,
            justify='center',
            **options
        )
        return entry

    def int_validation(self, value):
        pattern = r'^[-+]?[0-9]+$'
        if re.fullmatch(pattern, value) is None:
            return False
        return True

    def time_validation(self, value):
        pattern = r'^[-+]?[0-9]+$'
        if re.fullmatch(pattern, value) is None:
            return False
        return True

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

    def ms_validation(self, value):
        pattern = r'\d{0,3}'
        if re.fullmatch(pattern, value) is None:
            return False
        return True

    def create_timer_btn(self, text, name):
        button = MyButton(
            self.timer_frame, text,
            self.fg_timer, self.bg_timer,
            image=self.low_height_widgets,
            name=name,
        )
        return button

    def create_timer_widgets(self):
        timer_title_lbl = MyLabel(
            self.timer_frame, "Timer",
            self.fg_timer, self.bg_timer, image=self.btn_default,
            font=(self.font_timer, self.f_s_timer)
        )
        int_valid = (self.register(self.int_validation), '%S')
        sec_min_valid = (self.register(self.sec_min_validation), '%S')
        hours_valid = (self.register(self.hours_validation), '%S')
        ms_valid = (self.register(self.ms_validation), '%P')
        self.time_entry.append(self.create_entry(
            'Days', '00',
            validate="focusout", validatecommand=int_valid)
        )
        self.time_entry.append(self.create_entry(
            'Hours', '00',
            validate="focusout", validatecommand=hours_valid)
        )
        self.time_entry.append(self.create_entry(
            'Minutes', '00',
            validate="focusout", validatecommand=sec_min_valid)
        )
        self.time_entry.append(self.create_entry(
            'Seconds', '00',
            validate="focusout", validatecommand=sec_min_valid)
        )
        self.time_entry.append(self.create_entry(
            'Miliseconds', '00',
            validate="focusout", validatecommand=ms_valid)
        )

        self.delay_entry = self.create_entry(
            'Delay', "0", validate="key", validatecommand=int_valid)

        self.entry_desc = self.create_entry('Description')

        self.stop_btn = self.create_timer_btn(
            AppProperties.STOP_TXT, AppProperties.STOP_TXT.lower())

        self.start_pause_btn = self.create_timer_btn(
            AppProperties.START_TXT, f"{AppProperties.START_TXT.lower()}/{AppProperties.PAUSE_TXT.lower()}")

        self.btn_stop_delay = self.create_timer_btn(
            AppProperties.STOP_TXT + " delay", name=f"{AppProperties.STOP_TXT.lower()}_delay")

        self.start_pause_btn.config(
            command=lambda: self.toggle_start_pause())
        self.stop_btn.config(command=lambda: self.stop_timer())
        self.btn_stop_delay.config(command=lambda: self.stop_delay())
        timer_title_lbl.pack(side=tk.TOP)
        for entry in self.time_entry:
            entry.pack(side=tk.TOP)
        self.entry_desc.pack(side=tk.LEFT)
        self.delay_entry.pack(side=tk.RIGHT)
        self.start_pause_btn.pack(side=tk.TOP, fill=tk.BOTH)

    def create_label(self, text):
        label = MyLabel(
            self.time_frame, text,
            self.fg_timer, self.bg_timer,
            font=(self.font_timer, self.f_s_timer)
        )
        return label

    def create_savedtimes_widgets(self):
        MyLabel(
            self.saved_frame, "Saved times",
            self.fg_timer, self.bg_timer,
            image=self.btn_default,
            font=(self.font_timer, self.f_s_timer)
        ).pack()

        self.saved_times_date = self.create_label('Data')

        self.saved_times_time = self.create_label('Time')
        self.saved_times_descript = self.create_label('Description')

        self.saved_times_date.grid(column=0, row=0)
        self.saved_times_time.grid(column=1, row=0)
        self.saved_times_descript.grid(column=2, row=0)

    def stop_delay(self):
        self.timer_delay.cancel()
        self.start_pause_btn['state'] = 'normal'
        self.start_pause_btn['text'] = AppProperties.START_TXT
        self.btn_stop_delay.pack_forget()

    def start_counting(self):
        self.delay_condition()
        self.timer_start_value = self.format_time_array()
        self.start_pause_btn['text'] = AppProperties.PAUSE_TXT
        self.countdown_time(True)
        self.stop_btn.pack(side=tk.TOP, fill=tk.BOTH)

    def delay_condition(self, no_delay=True):
        if no_delay:
            self.btn_stop_delay.pack_forget()
            self.start_pause_btn["state"] = "normal"
        else:
            self.btn_stop_delay.pack(side=tk.TOP, fill=tk.BOTH)
            self.start_pause_btn["state"] = "disabled"
            self.start_pause_btn["text"] = AppProperties.START_TXT + " delay"

    def toggle_start_pause(self):
        if self.start_pause_btn["text"] == AppProperties.START_TXT:
            self.timer_time.clear()
            for entr in self.time_entry:
                if (len(entr.entry.get()) <= 0):
                    # must be at least 0
                    return
                self.timer_time.append(int(entr.entry.get()))

            if sum(w for w in self.timer_time) > 0:
                self.delay_condition(False)
                self.timer_time = list(map(int, self.timer_time))
                if self.delay_entry.entry.get().isdigit() and int(self.delay_entry.entry.get()) > 0:
                    delay_int = int(self.delay_entry.entry.get())
                    self.timer_delay = threading.Timer(
                        float(delay_int), self.start_counting)
                    self.timer_delay.start()
                else:
                    self.start_counting()

        elif self.start_pause_btn["text"] == AppProperties.PAUSE_TXT:
            self.start_pause_btn.config(text=AppProperties.RESUME_TXT)
            self.countdown_time()
        elif self.start_pause_btn["text"] == AppProperties.RESUME_TXT:
            self.start_pause_btn.config(text=AppProperties.PAUSE_TXT)
            self.countdown_time(True)

    def stop_timer(self):
        time_now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        timer_value = f"{self.timer_start_value} {':'.join([str(time) for time in self.timer_time if time > 0])}"
        self.saved_times.add_time(
            AppProperties.TIMER_PREFIX, time_now, timer_value, self.entry_desc.entry.get()
        )
        self.countdown_time()
        self.start_pause_btn.config(text=AppProperties.START_TXT)
        # self.time_entry.entry.delete(0, "end")
        self.timer_time = [0] * len(self.timer_time)
        # self.time_entry.entry.insert(1, ":".join(str(x)
        #  for x in self.timer_time))
        self.stop_btn.pack_forget()
        self.refresh_saved_times()

    def insert_to_entries(self):
        for index, entr in enumerate(self.time_entry):
            entr.entry.delete(0, "end")
            entr.entry.insert(1, self.timer_time[index])

    def countdown_time(self, start=False):
        ms_entry = self.time_entry[len(self.time_entry)-1]
        # last entry = miliseconds entry

        def time():
            self.insert_to_entries()
            # self.time_entry.entry.delete(0, "end")
            # self.time_entry.entry.insert(1, self.format_time_array())

            if sum(t for t in self.timer_time) > 0:
                self.is_counting = ms_entry.entry.after(1, time)
                self.timer_time[4] = self.timer_time[4] - 1
                return
            else:
                TimerPopup(self, self.entry_desc.entry.get(),
                           self.timer_start_value)
                self.stop_timer()
                return

        if not start:
            ms_entry.after_cancel(self.is_counting)
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
        return text_to_show[:-1]


class TimerPopup(tk.Tk):
    def __init__(self, root, description, start_time, *args, **kwargs):
        self.config_timer = ConfigProperties.TIMER_OPTIONS
        self.bg = self.config_timer["bg_color_timer"]["value"]
        self.fg = self.config_timer["fg_color_timer"]["value"]
        self.res = self.config_timer["timer_popup_resolution"]["value"]
        self.btn_default = PhotoImage(file=AppProperties.ALARMS_IMG)
        self.btn_small = self.btn_default.subsample(3, 2)

        tk.Toplevel.__init__(
            self, borderwidth=2, relief="raised", background=self.bg, *args, **kwargs
        )
        self._root = root
        self.eval(f"tk::PlaceWindow {str(self)} center")
        self.sound_process = None
        self.geometry(self.res)
        self.title(description)
        self.start_time = start_time
        self.sound_process = None
        self.music_to_play = (
            f"{AppProperties.SOUND_DIR}/{AppProperties.TIMER_SND}"
        )

        self.create_popup_widgets(description)
        self.start_sound()
        self.relief_r = ["sunken", "raised", "flat", "ridge", "groove"]
        if self.config_timer["animation"]["value"]:
            self.change_relief()

    def change_relief(self):
        self.config(relief=random.choice(self.relief_r))
        self.after(1000, self.change_relief)

    def create_popup_widgets(self, desc):
        txt_format = f"Description: \n{desc}\nStarter timer: \n {self.start_time}"
        MyLabel(self, txt_format, self.fg, self.bg, image=self.btn_default).grid(
            row=0, column=0
        )

        MyButton(
            self,
            "Stop timer",
            self.fg,
            self.bg,
            image=self.btn_small,
            name=f"stop_timer",
            command=lambda: self.stop_timer(),
        ).grid(row=0, column=1)

    def stop_timer(self):
        if self.sound_process != None:
            self.sound_process.kill()
        self.destroy()

    def start_sound(self):
        if AppProperties.SOUNDS_EXT in self.music_to_play:
            self.sound_process = multiprocessing.Process(
                target=playsound, args=(self.music_to_play,)
            )
            self.sound_process.start()
