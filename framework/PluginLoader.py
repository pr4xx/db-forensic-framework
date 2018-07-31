import click

from framework.Core import Core


class PluginLoader(click.MultiCommand):

    def list_commands(self, ctx):
        commands = []
        for plugin in Core.instance.plugin_manager.plugins:
            commands.append('plugin:run:' + plugin.config['name'])

        return commands

    def get_command(self, ctx, name):
        ns = {}
        ctx.obj = Core.instance
        plugin_name = name.split(':')[2]
        plugin = Core.instance.plugin_manager.get_plugin(plugin_name)
        fn = plugin.config['path'] + '/main.py'
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']