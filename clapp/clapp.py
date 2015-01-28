#!/usr/bin/env python
'''
Python 2.x / 3.x

clapp.py

v0.4.6

A library for building command line applications
'''

from __future__ import print_function
import sys
from os import path

__version__ = '0.4.6'
__build__ = '1'
__author__ = 'Kevin K. <kbknapp@gmail.com>'


def _null_func(context):
    """Represents a None for a function"""
    pass


class App(object):
    """The starting point for a command line application"""
    def __init__(self,
                 name='',
                 version='',
                 usage='',
                 about='',
                 author='',
                 main=_null_func):
        """Initializes a new version of the App class
        PARAMS:
            name: A string representing the name of the application
            version: A string representing the version of the application
            about: A string that displays what the application briefly doesn
            main: A function which accepts a dict() and the starting point of
                  the app will be called after all command line argumetns have
                  been processed
        """
        self._name = name
        self._author = author
        self._version = version
        self._args_map = dict()
        self._raw_args = sys.argv
        if self._raw_args[0][0] == '.' and self._raw_args[0][1] == '/':
            self._raw_args[0] = self._raw_args[0][2:]
        self._about = about
        self._usage = usage
        self._has_main = False
        if main != _null_func:
            self._has_main = True
        self._main = main
        self._context = dict()
        self._subcmds_map = dict()
        self._subcmds = []
        self._req_opts = []
        self._flags = []
        self._req_pos_args = []
        self._pos_args = []
        self._opts = []

    def start(self):
        """Called when the user wants to start processing command line arguments
        and start his main(context) function
        RETURN: Returns whatever your main(context) returns in order to allow
                sys.exit(app.start())
        """
        # Add a help command line argument if needed (i.e. -h and --help)
        self._add_help()
        # Add a version command line argument if needed (i.e. -v and --version)
        self._add_version()

        self._context['raw_args'] = sys.argv
        self._do_args(sys.argv[1:])

        if self._has_main:
            return self._main(self._context)
        return self._context

    def _do_args(self, args):
        """Validates the command line arguments passed to the script and performs
        any actions they call for.
        PARAMS:
            args: A list of command line arguments (pulled from sys.argv[1:])
        """

        actions_todo = []
        pos_args = 0
        skip_next = False
        num_to_skip = 0
        possible_pos_args = len(self._pos_args) + len(self._req_pos_args)
        subcmd = None

        for i, arg in enumerate(args):
            if skip_next and num_to_skip > 0:
                num_to_skip -= 1
                continue
            skip_next = False
            num_to_skip = 0
            if arg.find('=') != -1:
                arg, next_arg = arg.split('=')
                args.insert(i+1, next_arg)

            if not arg.startswith('--') and arg[0] == '-' and len(arg) > 2:
                for j, char in enumerate(arg):
                    if char == '-':
                        continue
                    args.insert(i + 1 + j, '-{}'.format(char))
                continue

            if arg not in self._args_map:
                if arg in self._subcmds_map:
                    subcmd = self._subcmds_map[arg]
                    args = args[i:]
                    args[0] = '{} {}'.format(self._raw_args[0], args[0])
                    break
                if possible_pos_args and arg[0] != '-':
                    pos_args += 1
                    index = 'index{}'.format(pos_args)
                    self._context[self._args_map[index].name] = arg
                    self._context[index] = arg
                    arg = self._args_map[index].name
                elif not possible_pos_args:
                    print('Argument error from {}\n{} doesn\'t accept '
                          'positional arguments.'.format(arg,
                                                         self._raw_args[0]))
                    self._display_usage(exit=True)
                else:
                    print('Argument error from {}\n{} doesn\'t accept any '
                          'arguments like {}.'.format(arg,
                                                      self._raw_args[0],
                                                      arg))
                    self._display_usage(exit=True)

            argo = self._args_map[arg]
            if argo.args_taken:
                if i+argo.args_taken == len(args):
                    print('Argument error from {}\n{} expected {} arguments '
                          'but received 0.'.format(arg, arg, argo.args_taken))
                    self._display_usage(exit=True)
                taken_args = []
                for j in range(argo.args_taken):
                    possible_arg = args[i + 1 + j]
                    if possible_arg.startswith('-'):
                        print('Argument error from {}\n{} expected {} '
                              'arguments but '
                              'received {}.'.format(possible_arg,
                                                    arg,
                                                    argo.args_taken,
                                                    len(taken_args)))
                        self._display_usage(exit=True)
                    taken_args.append(possible_arg)
                self._context[argo.name] = taken_args
                if argo.short:
                    self._context[argo.short] = taken_args
                if argo.long:
                    self._context[argo.long] = taken_args
                skip_next = True
                num_to_skip = argo.args_taken
            elif argo in self._flags:
                self._context[argo.name] = True
                if argo.short:
                    self._context[argo.short] = True
                if argo.long:
                    self._context[argo.long] = True
            if argo.has_action:
                actions_todo.append(argo.action)

        for act in actions_todo:
            if act == self._display_version or act == self._display_help:
                act()

        if pos_args < len(self._req_pos_args):
            print('Argument error.\nRequired number of positional arguments '
                  'not found.')
            self._display_usage(exit=True)

        for arg in self._req_opts:
            if arg.name not in self._context:
                display_name = ''
                if arg.long:
                    display_name = arg.long
                else:
                    display_name = arg.short
                print('Argument error.\nRequired option {} not found.'
                      .format(display_name))

        for flag in self._flags:
            if flag.name not in self._context:
                self._context[flag.name] = False
                if flag.short:
                    self._context[flag.short] = False
                if flag.long:
                    self._context[flag.long] = False

        for arg in set(self._args_map.values()):
            if arg.name not in self._context:
                if arg.default:
                    self._context[arg.name] = arg.default
                    if arg.short:
                        self._context[arg.short] = arg.default
                    if arg.long:
                        self._context[arg.long] = arg.default
                    if arg.index:
                        self._context['index{}'.format(arg.index)] = arg.default
                else:
                    self._context[arg.name] = False
                    if arg.short:
                        self._context[arg.short] = False
                    if arg.long:
                        self._context[arg.long] = False
                    if arg.index:
                        self._context['index{}'.format(arg.index)] = False

        for act in actions_todo:
            act(self._context)

        if subcmd:
            subcmd.start(args)

    def _display_usage(self, exit=True):
        ''' Displays usage of app based of flags and options
        name.py [flags] <req_opts> [opt_opts] <req_positional_args>
                [opt_positional_args]
        PARAMS:
            exit: Should sys.exit() be called at the conclusion of the function
        '''
        if self._usage:
            print(self._usage)
            if exit:
                sys.exit(0)

        usage_str = ''
        if self._flags:
            usage_str += '[-{}]'.format(''.join([arg.short.strip('-')
                                                for arg in self._flags]))
        if self._opts:
            usage_str += ' [{}]'.format(' '.join([' '.join([arg.short,
                                                            arg.name])
                                                 for arg in self._opts]))
        if self._req_opts:
            usage_str += ' <{}>'.format(' '.join([' '.join([arg.short,
                                                            arg.name])
                                                 for arg in self._req_opts]))
        if self._req_pos_args:
            usage_str += ' <{}>'.format(' '
                                        .join([arg.name
                                               for arg in self._req_pos_args]))
        if self._pos_args:
            usage_str += ' [{}]'.format(' '.join([arg.name
                                                 for arg in self._pos_args]))
        if self._subcmds:
            usage_str += ' [SUBCOMMANDS]'
        print('\nUSAGE:\n{} {}'.format(path.basename(self._raw_args[0]),
                                       usage_str))
        if exit:
            print('\nFor more information try --help')
            sys.exit(0)

    def _display_help(self):
        """Displays the possible command line arguemnts to the user and
        exits"""
        print('\n{} v{}\n{}\n{}'.format(self.name, self.version, self.author,
                                        self.about))
        self._display_usage(exit=False)
        if self._subcmds:
            print('\nSUB COMMANDS:')
            for sc in self._subcmds:
                print('{}\t\t{}'.format(sc.name, sc.about))

        if self._flags:
            print('\nFLAGS:')
            for f in self._flags:
                if f.short and f.long:
                    print('{},{}\t'.format(f.short, f.long), end='')
                elif f.short:
                    print('{}\t\t'.format(f.short), end='')
                else:
                    print('{}\t'.format(f.long), end='')
                print('{}'.format(f.help))

        if self._opts:
            print('\nOPTIONS:')
            for o in self._opts:
                # o = self._args[f[0:f.find(' ')]]
                print(o.short, end='')
                if o.short and o.long:
                    print(',', end='')
                print('{}={}\t{}'.format(o.long, o.name, o.help))
        if self._req_opts:
            print('\nREQUIRED OPTIONS:')
            for ro in self._req_opts:
                # ro = self._args[f[0:f.find(' ')]]
                print(ro.short, end='')
                if ro.short and ro.long:
                    print(',', end='')
                print('{}={}\t\t{}'.format(ro.long, ro.name, ro.help))
        if self._req_pos_args:
            print('\nREQUIRED POSITIONAL ARGUMENTS:')
            for rpo in self._req_pos_args:
                # rpo = self._args[f]
                print('{}\t\t{}'.format(rpo.name, rpo.help))
        if self._pos_args:
            print('\nOPTIONAL POSITIONAL ARGUMENTS:')
            for po in self._pos_args:
                # po = self._args[f]
                print('{}\t\t{}'.format(po.name, po.help))
        sys.exit(0)

    def _display_version(self, context=None):
        print('\n{} v{}'.format(self._name, self._version))
        sys.exit(0)

    def _add_arg_to_map(self, arg):
        """Builds a dict() of valid command line arguments based on
        Arg()s passed by the user.
        """
        self._args_map[arg.name] = arg
        if arg.short:
            self._args_map[arg.short] = arg
        if arg.long:
            self._args_map[arg.long] = arg
        if arg.index:
            self._args_map['index{}'.format(arg.index)] = arg
            if arg.required:
                self._req_pos_args.append(arg)
            else:
                self._pos_args.append(arg)
        elif arg.required:
            self._req_opts.append(arg)
        else:
            if arg.args_taken:
                self._opts.append(arg)
            else:
                self._flags.append(arg)

    def _add_subcmd_to_map(self, subcmd):
        """Builds a dict() of valid command line arguments based on Arg()s
        passed by the user."""
        self._subcmds_map[subcmd.name] = subcmd
        self._subcmds.append(subcmd)

    def _debug(self):
        """Displays debugging info"""
        print('Args dict:\n{}'.format(self._args))
        print('Args List:\n{}'.format(self.args))
        print('Flags:\n{}'.format(self._flags))
        print('Options:\n{}'.format(self._opts))
        print('Req Opts:\n{}'.format(self._req_opts))
        print('Pos:\n{}'.format(self._pos_args))
        print('Req Pos:\n{}'.format(self._req_pos_args))

    def add_arg(self, arg):
        """Add a single Arg() to the application
        PARAMS:
            arg: the clapp.Arg() to be added to the application
        """
        self._add_arg_to_map(arg)

    def add_args(self, args):
        """Add multiple clapp.Arg()s to the application
        PARAMS:
            args: A collection (list, set, etc.) of clapp.Arg() objects
        """
        for arg in args:
            self._add_arg_to_map(arg)

    def new_arg(self,
                name,
                long='',
                short='',
                help='',
                default='',
                action=_null_func,
                index=0,
                args_taken=0,
                required=False):
        """Create and add a clapp.Arg() to the application on the fly
        PARAMS:
            name: The unique name of the argument as a string
            long: A string of the long version of the argument (if any) i.e.
                  --help
            short: A string of the short version of the argument (if any)
                   i.e. -h
            help: A help string about the argument displayed to the user when
                  they use the --help
            action: A handler to be called if the user calls this argument
                    (must accept a dict())
            index: Used for positional arguments (Note: 1 based, **NOT** 0
                   based)
            args_taken: Int representing how many expected additional
                        arguments i.e. -o <file>
            required: Is this argument mandatory for proper script
                      functionality?"""
        arg = Arg(name,
                  long=long,
                  short=short,
                  help=help,
                  default=default,
                  action=action,
                  index=index,
                  args_taken=args_taken,
                  required=required)

        self._add_arg_to_map(arg)

    def new_subcommand_with_arg(self,
                                name,
                                arg,
                                about='',
                                version='',
                                main=_null_func):
        """Create and add a clapp.Arg() to the application on the fly
        PARAMS:
            name: The unique name of the sub-command as a string
            arg: The clapp.Arg() to add to the sub-command
        """
        subcmd = SubCommand(name, version=version, about=about, main=main)
        subcmd.add_arg(arg)
        self.add_subcommand(subcmd)

    def new_subcommand_with_args(self,
                                 name,
                                 args,
                                 about='',
                                 version='',
                                 main=_null_func):
        """Create and add a clapp.Arg() to the application on the fly
        PARAMS:
            name: The unique name of the sub-command as a string
            arg: The clapp.Arg() to add to the sub-command
        """
        subcmd = SubCommand(name, version=version, about=about, main=main)
        subcmd.add_args(args)
        self.add_subcommand(subcmd)

    def new_subcommand(self,
                       name,
                       about='',
                       version='',
                       main=_null_func):
        """Create and add a clapp.Arg() to the application on the fly
        PARAMS:
            name: The unique name of the sub-command as a string
            arg_name: A unique name of the sub-command argument as a string
            long: A string of the long version of the argument (if any) i.e.
                  --help
            short: A string of the short version of the argument (if any) i.e.
                   -h
            help: A help string about the argument displayed to the user when
                  they use the --help
            action: A handler to be called if the user calls this argument
                    (must accept a dict())
            index: Used for positional arguments (Note: 1 based, **NOT** 0
                   based)
            args_taken: Int representing how many expected additional
                        arguments i.e. -o <file>
            required: Is this argument mandatory for proper script
                      functionality?"""
        subcmd = SubCommand(name, version=version, about=about, main=main)
        self.add_subcommand(subcmd)

    def add_subcommand(self, subcmd):
        self._add_subcmd_to_map(subcmd)

    def add_subcommands(self, subcmds):
        for sc in subcmds:
            self.add_subcommand(sc)

    def _add_help(self):
        """Determines if the user provided his own --help or -h arguments
        and adds a default implementation if it doesn't find any
        """
        help = Arg('help')
        help.action = self._display_help
        help.help = 'Display help information'

        has_short = False
        for arg in set(self._args_map.values()):
            if arg.long == '--help':
                return
            if arg.short == '-h':
                has_short = True
        if not has_short:
            help.short = '-h'
        help.long = '--help'
        self.add_arg(help)

    def _add_version(self):
        """Determines if the user provided his own --version or -v arguments
        and adds a default implementation if it doesn't find any
        """
        version = Arg('version')
        version.action = self._display_version
        version.help = 'Display version information'

        has_short = False
        for arg in set(self._args_map.values()):
            if arg.long == '--version':
                return
            if arg.short == '-v':
                has_short = True

        if not has_short:
            version.short = '-v'
        version.long = '--version'
        self.add_arg(version)

    # Properties
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def about(self):
        return self._about

    @about.setter
    def about(self, value):
        self._about = value

    @property
    def has_main(self):
        return self._has_main

    @property
    def main(self):
        return self._main

    @main.setter
    def main(self, value):
        if value != _null_func:
            self._has_main = True
        self._main = value

    @property
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self, value):
        self._usage = value


class SubCommand(App):
    def __init__(self,
                 name,
                 version='',
                 about='',
                 usage='',
                 main=_null_func):
        if not name or name.find(' ') != -1:
            raise RuntimeError('SubCommand must have a'
                               'unique name with no spaces.')
        super(SubCommand, self).__init__(name)
        self._version = version
        self._about = about
        self._main = main
        self._usage = usage

    def start(self, args):
        """Called when the user wants to start processing command line arguments
        and start his main(context) function
        PARAMS:
            args: a list of arguments supplied to the script
        RETURN: Returns whatever your main(context) returns in order to allow
                sys.exit(app.start())
        """
        # Add a help command line argument if needed (i.e. -h and --help)
        self._add_help()
        # Add a version command line argument if needed (i.e. -v and --version)
        self._add_version()

        self._raw_args = args
        self._context['raw_args'] = args
        self._do_args(args[1:])

        if self._has_main:
            return self._main(self._context)
        return self._context


class Arg(object):
    def __init__(self,
                 name,
                 short='',
                 long='',
                 help='',
                 default='',
                 args_taken=0,
                 action=_null_func,
                 index=0,
                 required=False):
        if not name:
            raise RuntimeError('Arg(name) must have a unique name string.')
        self._short = short
        if self._short and len(self._short) != 2:
            raise RuntimeError('Arg.short wrong format. Must be "-h" style.')
        self._long = long
        self._help = help
        self._default = default
        self._required = required
        self._has_action = False
        if action != _null_func:
            self._has_action = True
        self._action = action
        self._index = index
        self._name = name
        self._args_taken = args_taken

    @property
    def name(self):
        return self._name

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value):
        self._default = value

    @property
    def short(self):
        return self._short

    @short.setter
    def short(self, value):
        if len(value) != 2:
            raise RuntimeError('Arg.short wrong format. Must be "-x" style.')
        if value:
            self._short = value

    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, value):
        if not value.startswith('--'):
            raise RuntimeError('Arg.long wrong format. Must be "--xx" style.')
        self._long = value

    @property
    def help(self):
        return self._help

    @help.setter
    def help(self, value):
        self._help = value

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, value):
        self._required = value

    @property
    def has_action(self):
        return self._has_action

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if value != _null_func:
            self._has_action = True
        self._action = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def args_taken(self):
        return self._args_taken

    @args_taken.setter
    def args_taken(self, value):
        self._args_taken = value
