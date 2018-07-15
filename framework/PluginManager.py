import configparser
import os
from framework.Plugin import Plugin


class PluginManager:

    def __init__(self, core):
        self.core = core
        self.plugins = []
        self.__load_plugins()

    def __load_plugins(self):
        """ Reads and parses the plugins directory. """

        for directory in os.listdir('plugins'):
            path = 'plugins/' + directory
            plugin_file = path + '/Pluginfile'
            if os.path.isfile(plugin_file):
                config = configparser.ConfigParser()
                config.read(plugin_file)
                plugin = Plugin(directory, path, {s: dict(config.items(s)) for s in config.sections()})
                self.plugins.append(plugin)

    def get_plugin(self, name):
        """ Returns a plugin object for a given name. """

        for plugin in self.plugins:
            if plugin.config['name'] == name:
                return plugin

        raise Exception('Unknown plugin name!')

    def print_plugins(self):
        """ Prints out a list of all loaded plugins. """

        print('There are %d plugins:' % len(self.plugins))
        for plugin in self.plugins:
            print(plugin)