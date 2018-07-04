import json


class Connection:

    def __init__(self, name, config):
        new_config = {'name': name}
        new_config.update(config)
        self.config = new_config

    def __str__(self):
        return json.dumps(self.config, indent=2)
