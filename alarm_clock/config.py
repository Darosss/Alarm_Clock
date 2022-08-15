import json

class ConfigJSON:
    def __init__(self, config):
        self.config = config
        with open(config, encoding='utf-8', errors='ignore') as config_json:
            self.json_conf = json.loads(config_json.read())
    @property
    def section(self):
         return self.json_conf

    def add_alarm(self, alarm, time, days, sound, description):
        with open(self.config, 'r+') as config_json:
            print(self.json_conf)
            self.json_conf.update( 
                    {   
                        alarm:{
                            "time":time,
                            "days":days,
                            "sound":sound,
                            "state":"disabled",
                            "description":description    
                        }
                    })
            config_json.seek(0)
            json.dump(self.json_conf, config_json, indent=4)
            config_json.truncate()  

    def modify_alarm(self, alarm, time, days, sound, description):
        with open(self.config, 'r+') as config_json:
            self.json_conf[alarm]["time"] = time
            self.json_conf[alarm]["days"] = days
            self.json_conf[alarm]["sound"] = sound
            self.json_conf[alarm]["description"] = description
            
            config_json.seek(0)
            json.dump(self.json_conf, config_json, indent=4)
            config_json.truncate()  

    def modify_section(self, section, option, value):
        with open(self.config, 'r+') as config_json:
            self.json_conf[section][option]= value 
            config_json.seek(0)
            json.dump(self.json_conf, config_json, indent=4)
            config_json.truncate()  
    
    def modify_settings(self, section, subsection, value):
        with open(self.config, 'r+') as config_json:
            self.json_conf[section][subsection]["value"]= value 

            config_json.seek(0)
            json.dump(self.json_conf, config_json, indent=4)
            config_json.truncate()  

  
    def pop_section(self, section):
        del self.json_conf[section]

        with open(self.config, 'r+') as config_json:
            config_json.seek(0)
            json.dump(self.json_conf, config_json, indent=4)
            config_json.truncate()  

    #FIXME REPAIR REAPEATING CODE