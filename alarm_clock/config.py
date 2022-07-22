import configparser


class Config:
    def __init__(self, config_name):
        self.config_name = config_name
        self.config_obj = configparser.ConfigParser()
        self.config_obj.read(config_name)

    def get_section(self, section_name):
        return self.config_obj[section_name]

    def get_key(self, section_name, key_name):
        return self.get_section(section_name)[key_name]

    def get_sections_keys(self, section_name, replace=True, replace_this="#", replace_to_this="\n"):
        array_keys = []
        for key in self.get_section(section_name):
            if replace:
                array_keys.append(key +"/"+self.config_obj[section_name][key].replace(replace_this,replace_to_this))
            else:
                array_keys.append(key +"/"+self.config_obj[section_name][key])
        return array_keys  
    
    def save_config(self, section_name, key_name, value):
        self.config_obj.set(section_name, key_name, value)
        with open(self.config_name, 'w') as configfile:
            self.config_obj.write(configfile)

    def remove_key_name(self, section_name, key_name):
        self.config_obj.remove_option(section_name, key_name)
        with open(self.config_name, 'w') as configfile:
            self.config_obj.write(configfile)

