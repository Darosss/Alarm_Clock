from re import A
import re
import tkinter as tk
from tkinter import PhotoImage
from app_properties import *
from my_widgets import *
import datetime
import threading


class Stopwatch(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        self._root = root
        self._root.update()

        self.config_stpwch = ConfigProperties.STOPWATCH_OPTIONS
        self.saved_times = ConfigProperties.SAVED_TIMES
        self.bg_stopwatch = self.config_stpwch["bg_color_stopwatch"]["value"]
        self.fg_stopwatch = self.config_stpwch["fg_color_stopwatch"]["value"]
        self.f_s_stopwatch = self.config_stpwch["font_size_stopwatch"]["value"]
        self.font_stopwatch = self.config_stpwch["font_stopwatch"]["value"]
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.btn_default = PhotoImage(file=AppProperties.STOPWATCH_IMG)
        self.low_height_widgets = self.btn_default.subsample(3, 2)
        self.btn_title = PhotoImage(file=AppProperties.TITLE_IMG)

        self.counting_interval = None
        self.stopwatch_time = [0, 0, 0, 0, 0]

        self.stopwatch_frame = tk.Frame(
            self, borderwidth=1, background=self.bg_stopwatch, relief="sunken"
        )
        self.stopwatch_lbl = None
        self.start_pause_btn = None
        self.btn_stop_delay = None
        self.timer_delay = None
        self.entry_desc = None
        self.delay_entry = None
        self.saved_frame_scroll = MyScrollableFrame(self, self.bg_stopwatch)
        self.saved_frame = self.saved_frame_scroll.frame

        self.stopwatch_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.saved_frame_scroll.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.time_frame = tk.Frame(
            self.saved_frame, background=self.bg_stopwatch)
        for i in range(3):
            self.time_frame.columnconfigure(i, weight=1)

        self.create_savedtimes_widgets()
        self.time_frame.pack(side=tk.TOP, fill="x", expand=True)
        self.refresh_saved_times()
        self.create_stopwatch_widgets()

    def refresh_saved_times(self):
        root_res = self._root.winfo_width()
        for slave in self.time_frame.grid_slaves():
            if "time_value" in slave.winfo_name():
                slave.destroy()

        for index, section in enumerate(
            sorted(
                self.saved_times.section[AppProperties.STOPWATCH_PREFIX], reverse=True)
        ):
            sec_lbl = self.create_label(self.time_frame,
                                        str(index + 1) + ". " +
                                        section, name=section + "/time_value_data",
                                        borderwidth=2, relief="raised",
                                        width=root_res//60,
                                        )

            sec_lbl.grid(column=0, row=index + 1, sticky=tk.NSEW)
            # Data and index here
            self.create_label(self.time_frame,
                              self.saved_times.section[AppProperties.STOPWATCH_PREFIX][section]["value"],
                              name="time_value_time" + str(index),
                              borderwidth=2, relief="raised",
                              ).grid(column=1, row=index + 1, sticky=tk.NSEW)
            # Time here
            self.create_label(self.time_frame,
                              self.saved_times.section[AppProperties.STOPWATCH_PREFIX][section]["description"],
                              name="time_value_description" + str(index),
                              borderwidth=2, relief="raised", width=root_res//35,
                              ).grid(column=2, row=index + 1, sticky=tk.NSEW)
            # Descirpition

            MyButton(
                self.time_frame,
                "x",
                self.fg_stopwatch,
                self.bg_stopwatch,
                image=self.low_height_widgets,
                font=(self.font_stopwatch, self.f_s_stopwatch),
                name="time_value_delete" + str(index),
                command=lambda sect_nam=sec_lbl.winfo_name().split("/")[
                    0
                ]: self.pop_and_refresh(sect_nam),
            ).grid(column=3, row=index + 1, sticky=tk.E)

    def pop_and_refresh(self, sect_name):
        self.saved_times.pop_section(AppProperties.STOPWATCH_PREFIX, sect_name)
        self.refresh_saved_times()

    def create_entry(self, title, value="", **options):
        entry = MyEntry(
            self.stopwatch_frame,
            self.fg_stopwatch, self.bg_stopwatch,
            title, self.btn_title,
            value,
            **options
        )
        return entry

    def int_validation(self, value):
        pattern = r'^[-+]?[0-9]+$'
        if re.fullmatch(pattern, value) is None:
            return False
        return True

    def create_stopwatch_btn(self, text, name):
        button = MyButton(
            self.stopwatch_frame, text,
            self.fg_stopwatch, self.bg_stopwatch,
            image=self.low_height_widgets,
            name=name,
        )
        return button

    def create_stopwatch_widgets(self):
        stopwatch_title_lbl = MyLabel(
            self.stopwatch_frame, "Stopwatch",
            self.fg_stopwatch, self.bg_stopwatch, image=self.btn_default,
            font=(self.font_stopwatch, self.f_s_stopwatch),
        )
        self.stopwatch_lbl = MyLabel(
            self.stopwatch_frame, "", self.fg_stopwatch, self.bg_stopwatch,
            font=(self.font_stopwatch, self.f_s_stopwatch),
        )

        int_valid = (self.register(self.int_validation), '%S')
        self.delay_entry = self.create_entry(
            "Delay", "0", validate='key', validatecommand=int_valid)
        self.entry_desc = self.create_entry("Description")
        self.stop_btn = self.create_stopwatch_btn(
            AppProperties.STOP_TXT, AppProperties.STOP_TXT.lower())
        self.start_pause_btn = self.create_stopwatch_btn(AppProperties.START_TXT,
                                                         f"{AppProperties.START_TXT.lower()}/{AppProperties.PAUSE_TXT.lower()}")
        self.btn_stop_delay = self.create_stopwatch_btn(
            AppProperties.STOP_TXT + " delay", name=f"{AppProperties.STOP_TXT.lower()}_delay")

        self.start_pause_btn.config(
            command=lambda: self.toggle_start_pause()
        )

        self.stop_btn.config(
            command=lambda: self.stop_stopwatch()
        )
        self.btn_stop_delay.config(command=lambda: self.stop_delay())
        stopwatch_title_lbl.pack()
        self.stopwatch_lbl.pack(expand=True)
        self.entry_desc.pack(side=tk.LEFT)
        self.delay_entry.pack(side=tk.RIGHT)
        self.start_pause_btn.pack(side=tk.TOP, fill=tk.BOTH)

    def create_label(self, append, text='', **options):
        label = MyLabel(
            append,
            text,
            self.fg_stopwatch,
            self.bg_stopwatch,
            font=(self.font_stopwatch, self.f_s_stopwatch),
            **options
        )
        return label

    def create_savedtimes_widgets(self):
        MyLabel(
            self.saved_frame,
            "Saved times",
            self.fg_stopwatch,
            self.bg_stopwatch,
            image=self.btn_default,
            font=(self.font_stopwatch, self.f_s_stopwatch),
        ).pack()
        self.saved_times_date = self.create_label(self.time_frame, "Data")
        self.saved_times_time = self.create_label(self.time_frame, "Time")
        self.saved_times_descript = self.create_label(
            self.time_frame, "Description")

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
        self.start_pause_btn.config(text=AppProperties.PAUSE_TXT)
        self.countdown_time(self.stopwatch_lbl, True)
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
            def start_counting():
                self.btn_stop_delay.pack_forget()
                self.start_pause_btn["state"] = "normal"
                self.start_pause_btn.config(text=AppProperties.PAUSE_TXT)
                self.countdown_time(self.stopwatch_lbl, True)
                self.stop_btn.pack(side=tk.TOP, fill=tk.BOTH)

            # if delay stop delay
            if self.delay_entry.entry.get().isdigit() and int(self.delay_entry.entry.get()) > 0:
                self.delay_condition(False)

                delay_int = int(self.delay_entry.entry.get())
                self.timer_delay = threading.Timer(
                    float(delay_int), start_counting)
                self.timer_delay.start()
            else:
                start_counting()

        elif self.start_pause_btn["text"] == AppProperties.PAUSE_TXT:
            self.start_pause_btn.config(text=AppProperties.RESUME_TXT)
            self.countdown_time(self.stopwatch_lbl)
        elif self.start_pause_btn["text"] == AppProperties.RESUME_TXT:

            self.start_pause_btn.config(text=AppProperties.PAUSE_TXT)
            self.countdown_time(self.stopwatch_lbl, True)

    def stop_stopwatch(self):
        time_now = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        self.saved_times.add_time(
            AppProperties.STOPWATCH_PREFIX,
            time_now,
            ":".join([str(time) for time in self.stopwatch_time if time > 0]),
            self.entry_desc.entry.get(),
        )

        self.start_pause_btn['text'] = AppProperties.START_TXT
        self.countdown_time(self.stopwatch_lbl)
        self.stopwatch_time = [0] * len(self.stopwatch_time)
        self.stop_btn.pack_forget()
        self.refresh_saved_times()

    def countdown_time(self, time_lbl, start=False):
        if not start:
            time_lbl.after_cancel(self.counting_interval)
            return

        def time():
            time_lbl.config(text=self.format_time_array())
            self.counting_interval = time_lbl.after(1, time)
            self.stopwatch_time[4] = self.stopwatch_time[4] + 1

        time()

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
