import json

class ConfigJSON:
    def __init__(self, config):
        self.config = config
        with open(config, encoding='utf-8', errors='ignore') as config_json:
            self.json_conf = json.loads(config_json.read())
    @property
    def section(self):
         return self.json_conf
    
    def modify_section(self, alarm, option, value):
        with open(self.config, 'r+') as config_json:
            if alarm not in self.json_conf:
                self.json_conf.update( {alarm:{}})
            self.json_conf[alarm]["value"][option]= value 

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