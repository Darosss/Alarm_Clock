import multiprocessing
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from datetime import timedelta
from playsound import playsound
# Alarm clock that I wanted to create based on android alam clock but for windows
# Prototype ver 1.0 Kappa


class AlarmApp(tk.Tk):
    def __init__(self, height, width, title):
        super().__init__()
        self.title(title)
        self.height = height #from user
        self.width = width #from user
        self.geometry(f'{self.height}x{self.width}')
        self.config(bg='gray') #from user
        self.update_idletasks()
        self.alarms_frame = None
        self.edit_frame = None
        self.snoozed_time = 1 #from user
        self.snoozed_alarms = []
        self.style = ttk.Style()
        self.styleName = "new.TFrame"
        self.style.configure(self.styleName, foreground="gray", background="#0f284f") #from user
        self.day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] #from user
        # describe all days of the week(maybe just for now)
        self.check_days = [None] * len(self.day_names)

    def create_scrollbar(self):
        pass
    # create scrollbar for more than x alarms

    def create_menu_app(self):
        frame = ttk.Frame(self, style=self.styleName)
        frame['borderwidth'] = 15
        frame['relief'] = 'groove'
        menu_btn_alarms = tk.Button(frame, text='Alarms', width=40).pack(side='left', expand=True)
        menu_btn_stopwatch = tk.Button(frame, text='Stopwatch', width=40).pack(side='left', expand=True)
        menu_btn_timer = tk.Button(frame, text='Timer', width=40).pack(side='left', expand=True)
        return frame
    # menu: stopwatch, egg timer, alarms

    def create_edit_alarm_frame(self):
        self.edit_frame = ttk.Frame(self, style=self.styleName, borderwidth=15, relief='sunken')
        self.edit_frame.columnconfigure(1, weight=1)
        return self.edit_frame

    def clear_edit_frame(self):
        for widgets in self.edit_frame.winfo_children():
            widgets.destroy()

    def delete_alarm_box(self, alarm, owner):
        print(f"[delete_alarm_box]: alarm: {alarm} - owner: {owner}")
        alarm.destroy()
        owner.destroy()
        self.clear_edit_frame()
    # that's function that is destroying described above

    def create_alarm(self, append, text, row_alarm):
        def toggle_alarm(alarm, checkbox):
            if "selected" in checkbox.state():
                alarm.config(state="normal")
                return
            alarm.config(state="disabled")
        height = 3
        width = 30
        delete_txt = "x"
        alarm_box = tk.Button(append, text=text, width=width, height=height, name=f"alarm_box{row_alarm}")
        alarm_box.grid(column=0, row=row_alarm + 2)
        alarm_box.config(state="disabled", command=lambda btn=alarm_box: self.edit_alarm(btn))
        #state disabled zamiana na konfig czy wlaczony zy nie

        # plan is that program will read config file at the start and check
        # how many alarms is used and create them at start of program
        # if there are none, it will load default fe. 5 alarms

        delete_alarm = tk.Button(append, text=delete_txt, height=height // 2, width=width // 5)
        delete_alarm.grid(column=3, row=row_alarm + 2, padx=5, pady=1, sticky='w')
        delete_alarm.config(command=lambda btn=alarm_box, dlt=delete_alarm: self.delete_alarm_box(btn, dlt))
        # delete buttons that are right near alarm that user want to delete
        # the buttons are calling function delete_alarm_box which are deleting
        # them and 'their' alarm to which they are bounded to
        turned_on_check = ttk.Checkbutton(append, text="Turned on")
        turned_on_check.grid(column=2, row=row_alarm + 2, padx=5, pady=1, sticky='w')
        turned_on_check.config(command=lambda btn=alarm_box, check=turned_on_check: toggle_alarm(btn, check))


    def add_alarm(self, frame):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        now_day = now.strftime("%a")
        alarm_text = dt_string + " \n " + now_day
        row_alarm_box = frame.grid_size()[1]
        self.create_alarm(frame, alarm_text, row_alarm_box)
    # this function is for adding new alarm, which maybe should be here, idk

    def create_alarm_boxes_frame(self, count, width):
        self.alarms_frame = ttk.Frame(self, style=self.styleName)
        self.alarms_frame['borderwidth'] = 15
        self.alarms_frame['relief'] = 'sunken'
        # frames border for debugging for now
        time_label = ttk.Label(self.alarms_frame, justify='center',
                               font=('calibri', 25, 'bold'), borderwidth=1, relief="solid")
        time_label.grid(column=0, row=0, sticky='new')

        def time():
            time_now = datetime.now().strftime("%H:%M:%S")
            time_label.config(text=time_now)
            time_label.after(1000, time)
        # watch

        add_button = tk.Button(self.alarms_frame, text="Add", height=1, width=width)
        add_button.grid(column=2, row=0, padx=5, pady=1)
        add_button.config(command=lambda f=self.alarms_frame: self.add_alarm(f))

        time()
        # add buttons for adding new alarms
        for i in range(count):
            seconds = 5 + (i*25)
            soon = datetime.now() + timedelta(seconds=seconds)
            dt_string = soon.strftime("%H:%M:%S")
            today = soon.strftime("%a")
            #debug alarm is 5 sec from start program
            self.create_alarm(self.alarms_frame, f"{dt_string} \n {today}", i)
        # for loop for every alarm giving in config or default

        self.alarms_frame.grid(column=0, row=1, sticky=tk.N)
        return self.alarms_frame

    def check_alarms(self):
        alarms = []
        for alarm in self.alarms_frame.grid_slaves():
            # if "alarm_box" in alarm:
            if "alarm_box" not in str(alarm):
                continue
            if alarm['state'] == "normal":
                al = alarm['text'].split("\n")
                alarms.append(al)
        for snoozed_alarm in self.snoozed_alarms:
            al = snoozed_alarm.split("\n")
            alarms.append(al)
        return alarms

    def snooze_alarm(self):
        snooze_time_now = datetime.now() + timedelta(minutes=self.snoozed_time)
        time_string = snooze_time_now.strftime("%H:%M:%S")
        day_string = snooze_time_now.strftime("%a")
        snoozed_alarm_time = time_string + " \n " + day_string
        self.snoozed_alarms.append(snoozed_alarm_time)

    def alarm_popup(self, text, sound):
        def stop_alarm():
            top.destroy()
            p.kill()
        top = tk.Toplevel(self)
        top.geometry("750x250")
        top.title(text)
        p = multiprocessing.Process(target=playsound, args=(sound,))
        p.start()
        ttk.Label(top, text=text, font=('Mistral 18 bold')).pack(side='left')
        ttk.Button(top, text="Stop alarm", command=lambda: stop_alarm()).pack(side='right')
        ttk.Button(top, text="Mute sound", command=lambda: p.kill()).pack(side='right')
        ttk.Button(top, text="Snooze", command=lambda alarm=text: [self.snooze_alarm(), stop_alarm()]
                   ).pack(side='right')
        top.overrideredirect(True)

    def set_alarms(self):
        alarms = self.check_alarms()
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        today = now.strftime("%A")
        now_time = dt_string + " \n " + today[0:3]
        for i in alarms:
            if today[0:3] in str(i[1]):
                if dt_string in str(i[0]):
                    self.alarm_popup(now_time, "sounds/1.mp3")
        self.after(1000, self.set_alarms)
        # plan taki:
        # wyskakuje nowe okno(ktore moze miga?) pokazuje ze czas przepylnal i jest tam wiadomosc(jesli byla napisana)
        # muzyka dzwiek gra przez caly czas az do momentu max. dzwieku
        # po tym czasie zostaje sam alarm bez dzwieku
        # tutaj skonczylem sprawdzic jak to z klasami i co pozmieniac ale moze pozniej

    def edit_alarm(self, alarm):
        # create empty array for checkboxes
        self.clear_edit_frame()
        # clear everything inside edit box
        ttk.Label(self.edit_frame, anchor='center', width=20,
                  font=("default", 20), text=f' {alarm["text"]}'
                  ).grid(column=1, row=0, sticky='ns')
        # ttk.Label(self.edit_frame, padding=20, text=f' {b["text"]}').pack(side='top', expand=False)
        # text about what alarm is edited (i'll create these names later)
        hours = tk.Entry(self.edit_frame, bd=1, width=10, font=("default", 40))
        hours.grid(column=1, row=2, sticky='ns')
        hour_text = alarm['text'].split(" ")[0].split(":")
        hours.insert(0, f"{hour_text[0]}:{hour_text[1]}:{hour_text[2]}")

        # create hour Entry
        # add it to grid
        # add hour from alarm (take text from alarm_button and split it with space and :) that is editing
        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 15))
        # only style, maybe i can change it later
        save_btn = ttk.Button(self.edit_frame, text="Save", padding=25, style='my.TButton')

        save_btn.config(command=lambda timer=alarm, h=hours: self.save_alarm(timer, h))
        save_btn.grid(column=2, row=3, sticky="w")
        # save editing alarm button and add to grid


        for inx, day in enumerate(self.day_names):
            self.check_days[inx] = ttk.Checkbutton(self.edit_frame, text=day)
            self.check_days[inx].grid(row=5 + inx, column=1, sticky='w')
        # this loop is creating each day of the week and add it to checkbutton in array and add to grid

    def save_alarm(self, alarm, hour):
        def info_save(remove=False):
            info_btn_save = ttk.Label(self.edit_frame)
            if not remove:
                info_btn_save.config(text='It has to be at least one day')
                info_btn_save.grid(column=2, row=4, sticky="w")
                return
            info_btn_save.grid_remove()
        # info_save is giving info about what should be added for alarm to work

        new_alarm = f"{hour.get()} \n"
        found = False
        for d in self.check_days:
            if 'selected' in d.state():
                found = True
                info_save(found)
                new_alarm += f"{d['text']} "
        if not found:
            info_save(found)
            return
        # check every check box with day if it's selected
        alarm['text'] = new_alarm
        # add hours and days to editing alarm


def run_program():
    alarm = AlarmApp(1000, 800, 'Alarm Clock')
    # create alarm app(width, height, title name) Soon i'll create resizable and dynamical boxes,
    # for now its just static i guess
    alarm.columnconfigure(0, weight=3)
    alarm.columnconfigure(1, weight=1)
    alarm.columnconfigure(2, weight=1)

    alarm.rowconfigure(1, weight=1)
    menu = alarm.create_menu_app()
    menu.grid(column=0, row=0, columnspan=4, sticky="nsew")
    # menu grid append
    alarm_boxes = alarm.create_alarm_boxes_frame(5, 30)
    alarm_boxes.grid(column=1, columnspan=2, row=1, sticky="nsew")
    # alarm boxes grid append

    edit = alarm.create_edit_alarm_frame()
    edit.grid(column=0, row=1, sticky='nsew')
    # edit box grid append
    alarm.set_alarms()
    alarm.mainloop()


if __name__ == "__main__":
    run_program()
