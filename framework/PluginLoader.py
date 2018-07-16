import os

import click


class PluginLoader(click.MultiCommand):

    def __init__(self, core):
        super().__init__()
        self.core = core

    def list_commands(self, ctx):
        commands = []
        for plugin in self.core.plugin_manager.plugins:
            commands.append('plugin:run:' + plugin.config['name'])

        return commands

    def get_command(self, ctx, name):
        ns = {}
        ctx.obj = self.core
        plugin_name = name.split(':')[2]
        plugin = self.core.plugin_manager.get_plugin(plugin_name)
        fn = plugin.config['path'] + '/main.py'
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']