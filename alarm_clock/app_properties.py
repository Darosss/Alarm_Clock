from config import ConfigJSON


class ConfigProperties:
    JSON_DIR = 'json'
    CONFIG = ConfigJSON(f"{JSON_DIR}/config.json")
    ALARMS = ConfigJSON(f"{JSON_DIR}/alarms.json")
    SAVED_TIMES = ConfigJSON(f"{JSON_DIR}/saved_times.json")
    DEFAULT_CONFIG = f"{JSON_DIR}/default_config.json"
    TIME = "time"
    DAYS = "days"
    SOUND = "sound"
    STATE = "state"
    SNOOZE_TIME = "snooze_time"
    DESCR = "description"
    APP_SETTINGS = CONFIG.section["app_settings"]
    MENU_OPTIONS = CONFIG.section["menu_options"]
    ALARMS_OPTIONS = CONFIG.section["alarms_options"]
    STOPWATCH_OPTIONS = CONFIG.section["stopwatch_options"]
    TIMER_OPTIONS = CONFIG.section["timer_options"]
    FOOTER_OPTIONS = CONFIG.section["footer_options"]


class AppProperties:
    IMAGES_DIR = ConfigProperties.APP_SETTINGS["images_dir"]["value"]
    SOUND_DIR = ConfigProperties.APP_SETTINGS["sounds_dir"]["value"]
    SOUNDS_EXT = f".{ConfigProperties.APP_SETTINGS['sounds_ext']['value']}"
    TIMER_SND = f"timer{SOUNDS_EXT}"
    START_TXT = ConfigProperties.APP_SETTINGS["start_txt"]["value"]
    STOP_TXT = ConfigProperties.APP_SETTINGS["stop_txt"]["value"]
    PAUSE_TXT = ConfigProperties.APP_SETTINGS["pause_txt"]["value"]
    RESUME_TXT = ConfigProperties.APP_SETTINGS["resume_txt"]["value"]
    ALARMS_IMG = f"{IMAGES_DIR}/alarms.png"
    SETTINGS_IMG = f"{IMAGES_DIR}/settings.png"
    MENU_IMG = f"{IMAGES_DIR}/menu.png"
    FOOTER_TIMER_IMG = f"{IMAGES_DIR}/footer_timer.png"
    TIMER_IMG = f"{IMAGES_DIR}/timer.png"
    STOPWATCH_IMG = f"{IMAGES_DIR}/stopwatch.png"
    TITLE_IMG = f"{IMAGES_DIR}/title.png"
    DELETE_STRING = "X"
    ALARM_PREFIX = "alarm_box"
    STOPWATCH_PREFIX = "stopwatch"
    TIMER_PREFIX = "timer"
