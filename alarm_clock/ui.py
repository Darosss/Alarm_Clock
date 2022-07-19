class AlarmUI:
    # Create ui depends on what user turned on
    # fe. alarm and how many alarms / egg timer / stop watch
    # draw it
    # contains a lot of alarm classes ( depends how much user turned ), stop watch and egg timer class

    def __init__(self, alarms=True, stop_watch=True, egg_timer=True):
        self.alarms = alarms
        self.stop_watch = stop_watch
        self.egg_timer = egg_timer


class Alarms:
    pass


class StopWatch:
    pass


class EggTimer:
    pass
