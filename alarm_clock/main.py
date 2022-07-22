from alarm_app import AlarmApp

def run_program():
    app = AlarmApp('Alarm Clock')
    # create alarm app(width, height, title name) Soon i'll create resizable and dynamical boxes,
    # for now its just static i guess
    app.columnconfigure(0, weight=3)
    app.columnconfigure(1, weight=1)
    app.rowconfigure(1, weight=6)
    app.rowconfigure(2, weight=1)
    # alarm.rowconfigure(0, weight=1) jesli wieksze menu

    footer = app.create_footer_app()

    # menu grid append
    alarms = app.create_alarm_app()
    stopwatch = app.create_stopwatch_app(None)
    timer = app.create_timer_app(None)
    menu = app.create_menu_app()
    app.show_app(alarms)
    app.mainloop()


if __name__ == "__main__":
    run_program()