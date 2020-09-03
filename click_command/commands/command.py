from importlib import import_module
import imp
import os
from os.path import dirname
# dir_path = os.path.dirname(os.path.realpath(__file__))

class BaseCommand():
    def __init__(self, **args):
        for arg, value in args.items():
            setattr(self, '_%s' % arg, value)

        self.info('Debug mode is %s' % ('on' if self._debug else 'off'))

    @property
    def cli(self):
        return self._cli

    def exec(self):
        self.error('"%s" Not implemented' % self._command)

    def error(self, message):
        self.cli.echo(self.cli.style(message, fg='red'))

    def info(self, message):
        self.cli.echo(self.cli.style(message, fg='green'))

    def debug(self, message):
        if self.debug:
            self.cli.echo(self.cli.style(message, fg='green'))


class Factory():
    def factory(self, command, command_arguments):
        command_class = self._dynamic_import(command)
        return command_class(command=command, **command_arguments)

    def _find_and_load_module(self, name, path=None):
        """
        Finds and loads it. But if there's a . in the name, handles it
        properly.
        """
        bits = name.split('.')
        while len(bits) > 1:
            # Treat the first bit as a package
            packagename = bits.pop(0)
            package = self._find_and_load_module(packagename, path)
            try:
                path = package.__path__
            except AttributeError:
                # This could be e.g. moves.
                flog.debug('Package {0} has no __path__.'.format(package))
                if name in sys.modules:
                    return sys.modules[name]
                flog.debug('What to do here?')

        name = bits[0]
        module_info = imp.find_module(name, path)
        return imp.load_module(name, *module_info)

    def _dynamic_import(self, command):
        command = '%s.command' % command
        mod = self._find_and_load_module(command, path=[dirname(__file__)])

        return mod.Command