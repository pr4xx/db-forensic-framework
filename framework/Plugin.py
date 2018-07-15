import json


class Plugin:

    def __init__(self, name, path, config):
        new_config = {'name': name, 'path': path}
        new_config.update(config)
        self.config = new_config

    def __str__(self):
        return json.dumps(self.config, indent=2)
