import tkinter as tk
from tkinter import PhotoImage, colorchooser, messagebox
from tkinter.filedialog import askopenfilenames
from datetime import datetime
from my_widgets import MyButton, MyLabel, MyScrollableFrame
from app_properties import *
from applications.alarms import Alarms
from applications.timer import Timer
from applications.stopwatch import Stopwatch
import shutil


# Alarm clock that I wanted to create based on android alam clock but for windows
# Prototype ver 1.0 Kappa
# It's first interract with tkinter


class AlarmApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.config_app = ConfigProperties.APP_SETTINGS
        self.geometry(self.config_app["resolution"]["value"])
        self._alarm_app_frame = Alarms(self)
        self._stopwatch_app_frame = Stopwatch(self)
        self._timer_app_frame = Timer(self)
        self.title("Alarm clock")
        self._menu = MainMenu(self)
        self._footer_frame = FooterFrame(self)
        self._menu_frame = MenuFrame(
            self,
            self._alarm_app_frame,
            self._stopwatch_app_frame,
            self._timer_app_frame,
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

    def upload_sounds(self):
        file_path = self.open_file()
        if file_path:
            for path in file_path:
                shutil.copy(path, AppProperties.SOUND_DIR)

    def menu_settings(self):
        SettingsWindow()

    def quit_app(self):
        self.quit()

    def show_info(self):
        messagebox.showinfo(
            'Info', 'Author: Darosss\nhttps://github.com/Darosss', parent=self)

    def open_file(self):
        file_path = askopenfilenames(filetypes=[
            ('Audio files', f'*{AppProperties.SOUNDS_EXT[1:]}')])
        if file_path is not None:
            return file_path


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
        tk.Toplevel.__init__(self, background=self.bg, *args, **kwargs)
        self.geometry(self.resolution)
        self.title("Settings")
        self.attributes("-topmost", "true")
        self.sect_btns = MyScrollableFrame(self, self.bg)
        self.rowconfigure(3, weight=1)
        self.sect_btns.grid(column=0, row=3, sticky=tk.NSEW)
        self.create_settings_widgets()
        self.create_save_btn()
        self.create_default_button()

    def create_save_btn(self):
        save_btn = MyButton(
            self, "Save", self.fg, self.bg, image=self.btn_default, name="save_sett_btn"
        )
        save_btn.grid(column=0, row=0, sticky=tk.W)
        save_btn.config(command=lambda: self.save_settings())

    def create_default_button(self):
        default_btn = MyButton(
            self, "Default", self.fg, self.bg, image=self.btn_default, name="default_btn"
        )
        default_btn.grid(column=0, row=1, sticky=tk.W)
        default_btn.config(command=lambda: self.restore_default())

    def create_settings_widgets(self):
        sect_btns_frame = self.sect_btns.frame
        for index, section in enumerate(self.all_sections):
            section_formated = section.title().replace("_", " ")
            scroll_frame = MyScrollableFrame(
                self, self.bg, name="section_frame_" + str(index))
            sectionFrame = scroll_frame.frame
            MyLabel(
                sectionFrame,
                section_formated,
                self.fg,
                self.bg,
                image=self.img_description,
                font=(self.settings_font, self.font_size),
            ).grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)
            for index, subsect in enumerate(self.all_sections[section]):
                self.add_setting(
                    sectionFrame,
                    self.all_sections[section][subsect]["description"],
                    section,
                    subsect,
                    self.all_sections[section][subsect]["value"],
                    sectionFrame.grid_size()[1] + 1,
                )

            MyButton(
                sect_btns_frame,
                section_formated,
                self.fg,
                self.bg,
                image=self.img_section,
                font=(self.settings_font, int(self.font_size**1.2)),
                name=section + "_btn",
                command=lambda secFram=scroll_frame: self.show_settings(
                    secFram),
            ).pack(side=tk.TOP)

    def choose_color(self, entry):
        color_code = colorchooser.askcolor(title="Choose color", parent=self)

        if color_code[1]:
            entry.delete(0, "end")
            entry.insert(0, color_code[1])

    def add_setting(
        self, append, sett_descr, section_name, option_name, value, row_grid, width=20
    ):
        MyLabel(
            append,
            sett_descr,
            self.fg,
            self.bg,
            image=self.img_description,
            font=(self.settings_font, self.font_size),
        ).grid(column=0, row=row_grid, sticky="nse")
        res_entry = tk.Entry(
            append,
            width=width,
            font=(self.settings_font, self.font_size),
            background=self.bg,
            foreground=self.fg,
            name=f"{section_name}/{option_name}",
        )
        res_entry.insert(0, value)
        res_entry.grid(column=1, row=row_grid, sticky=tk.NSEW)
        if "color" in option_name:
            button = MyButton(
                append,
                "Select color",
                self.fg,
                self.bg,
                image=self.img_section,
                command=lambda: self.choose_color(res_entry),
            )
            button.grid(column=2, row=row_grid, sticky=tk.NSEW)
        # if color font = create color picker near

    def show_settings(self, show):
        for s in self.grid_slaves():
            if "section_frame" in s.winfo_name():
                s.grid_forget()
        show.grid(column=1, row=3, sticky=tk.NSEW)

    def save_settings(self):
        for s in self.winfo_children():
            if "section_frame" in s.winfo_name():
                for option in s.frame.grid_slaves():
                    if option.widgetName == "entry":
                        option_value = option.get()
                        if option_value.isdigit():
                            option_value = int(option_value)
                        sect_and_key = option.winfo_name().split("/")
                        self.all_config.modify_settings(
                            sect_and_key[0], sect_and_key[1], option_value
                        )

    def restore_default(self):
        MsgBox = messagebox.askquestion(
            'Default settings', 'Are you sure you want to set the settings to default?', icon='warning', parent=self)
        if MsgBox == 'yes':
            self.all_config.restore_defaults(ConfigProperties.DEFAULT_CONFIG)
            messagebox.showinfo(
                'Default settings', 'Settings set to default. Restart application to update', parent=self)

    def add_button_section(self, section_name):
        row_grid = self.grid_size()[1] + 1
        return MyButton(
            self,
            section_name,
            self.fg,
            self.bg,
            image=self.img_section,
            font=(self.settings_font, self.font_size * 2),
        ).grid(column=0, row=row_grid, sticky="e")


class MainMenu(tk.Menu):
    @ property
    def root(self):
        return self._root

    def __init__(self, root, *args, **kwargs):
        tk.Menu.__init__(self, root, *args, **kwargs)
        self._root = root
        window_menu = OptionsMenu(self, tearoff=0)
        self.add_cascade(label="Options", menu=window_menu)
        help_menu = HelpMenu(self, tearoff=0)
        self.add_cascade(label="Help", menu=help_menu)
        root.config(menu=self)


class OptionsMenu(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)

        self.add_command(label="Upload sounds",
                         command=parent.root.upload_sounds)
        self.add_command(label="Settings", command=parent.root.menu_settings)
        self.add_command(label="Exit", command=parent.root.quit_app)


class HelpMenu(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)
        self.add_command(label="Info", command=parent.root.show_info)


class MenuFrame(tk.Frame):
    def __init__(
        self, root, alarm_frame, stopwatch_frame, timer_frame, *args, **kwargs
    ):
        self._root = root
        self.img_menu = PhotoImage(file=AppProperties.MENU_IMG)
        self.config_menu = ConfigProperties.MENU_OPTIONS
        self.bg = self.config_menu["menu_color_bg"]["value"]
        self.fg = self.config_menu["menu_color_fg"]["value"]
        tk.Frame.__init__(
            self,
            root,
            background=self.bg,
            borderwidth=1,
            relief="raised",
            *args,
            **kwargs,
        )
        menu_btn_alarms = MyButton(
            self,
            "Alarms",
            self.fg,
            self.bg,
            image=self.img_menu,
            name="alarms_menu_btn",
        )

        menu_btn_stopwatch = MyButton(
            self,
            "Stopwatch",
            self.fg,
            self.bg,
            image=self.img_menu,
            name="stopwatch_menu_btn",
        )

        menu_btn_timer = MyButton(
            self, "Timer", self.fg, self.bg, image=self.img_menu, name="timer_menu_btn"
        )

        menu_btn_alarms.config(
            command=lambda f=alarm_frame: self.clear_and_show_clicked(f)
        )
        menu_btn_stopwatch.config(
            command=lambda f=stopwatch_frame: self.clear_and_show_clicked(f)
        )
        menu_btn_timer.config(
            command=lambda f=timer_frame: self.clear_and_show_clicked(f)
        )

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

        tk.Frame.__init__(
            self,
            root,
            background=self.bg_footer,
            borderwidth=1,
            relief="sunken",
            *args,
            **kwargs,
        )
        self.time_label = MyLabel(
            self,
            "",
            self.fg_footer,
            self.bg_footer,
            image=self.img_timer,
            font=(self.font_timer, self.f_s_timer, "bold"),
        )
        self.time()

        self.time_label.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)

    def time(self):
        time_now = datetime.now().strftime("%H:%M:%S")
        self.time_label["text"] = time_now
        self.time_label.after(1000, self.time)
