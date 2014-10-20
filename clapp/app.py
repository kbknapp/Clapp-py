#!/usr/bin/env python
'''
Python 3.x

app.py

v0.3.1

A library for building command line applications
'''
import sys
from clapp import arg

__version__ = '0.3.1'
__author__ = 'Kevin K. <kbknapp@gmail.com>'

def _null_func(context):
    pass


class Clapp(object):
    def __init__(self, name='', version='', about='', main=_null_func):
        self._name = name
        self._version = version
        self._args_map = dict()
        self._valid_args = []
        self._raw_args = []
        self._about = about
        self._has_main = False
        if main != _null_func:
            self._has_main = True
        self._main = main
        self._context = dict()
        
        # self._args_parsed = False
        self._req_opts = []
        self._flags = []
        self._req_pos_args = []
        self._pos_args = []
        self._opts = []

    def start(self):
        self._add_help()
        self._add_version()
        self._raw_args = sys.argv

        if len(sys.argv) > 1:
            self._context['raw_args'] = sys.argv
            self._do_args(sys.argv[1:])

        if self._has_main:
            self._main(self._context)

    def _do_args(self, args):
        actions_todo = []
        pos_args = 0

        for arg in args:
            if arg not in self._args_map:
                pos_args += 1
                self._context['index{}'.format(pos_args)] = arg


    def _display_usage(self, exit=True):
        ''' Displays usage of app based of flags and options
        name.py [flags] <req_opts> [opt_opts] <req_positional_args> [opt_positional_args]
        '''
        usage_str = ''
        if self._flags:
            usage_str += '[-{}]'.format(''.join([arg.short.strip('-') for arg in self._flags]))
        if self._opts:
            usage_str += ' [{}]'.format(' '.join([' '.join([arg.short, arg.name]) for arg in self._opts]))
        if self._req_opts:
            usage_str += ' <{}>'.format(' '.join([' '.join([arg.short, arg.name]) for arg in self._req_opts]))
        if self._req_pos_args:
            usage_str += ' <{}>'.format(' '.join([arg.name for arg in self._req_pos_args]))
        if self._pos_args:
            usage_str += ' [{}]'.format(' '.join([arg.name for arg in self._pos_args]))
        print('\nUSAGE:\n{} {}'.format(self._raw_args[0], usage_str))
        if exit:
            print('\nFor more information try --help')
            sys.exit(0)

    def _display_help(self, context=None):
        print('\n{} v{}\n{}'.format(self.name, self.version, self.about))
        self._display_usage(exit=False)
        if self._flags:
            print('\nFLAGS:')
            for f in self._flags:
                a = self._args[f]
                print(a.short, end='')
                if a.short and a.long:
                    print(',', end='')
                else:
                    print('\t', end='')
                print('{}\t\t{}'.format(a.long, a.help))

        if self._opts:
            print('\nOPTIONS:')
            for f in self._opts:
                o = self._args[f[0:f.find(' ')]]
                print(o.short, end='')
                if o.short and o.long:
                    print(',', end='')
                print('{}={}\t{}'.format(o.long, o.name, o.help))
        if self._req_opts:
            print('\nREQUIRED OPTIONS:')
            for f in self._req_opts:
                ro = self._args[f[0:f.find(' ')]]
                print(ro.short, end='')
                if ro.short and ro.long:
                    print(',', end='')
                print('{}={}\t\t{}'.format(ro.long, ro.name, ro.help))
        if self._req_pos_args:
            print('\nREQUIRED POSITIONAL ARGUMENTS:')
            for f in self._req_pos_args:
                rpo = self._args[f]
                print('{}\t\t{}'.format(rpo.name, rpo.help))
        if self._pos_args:
            print('\nOPTIONAL POSITIONAL ARGUMENTS:')
            for f in self._pos_args:
                po = self._args[f]
                print('{}\t\t{}'.format(po.name, po.help))
        sys.exit(0)

    def _display_version(self, context=None):
        print('\n{} v{}'.format(self._name, self._version))
        sys.exit(0)

    def _add_arg_to_map(self, arg):
        """Builds a dict of possible valid arguments."""
        self._args_map[arg.name] = arg
        if arg.short:
            self._args_map[arg.name.short] = arg
        if arg.long:
            self._args_map[arg.name.long] = arg
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

    def _debug(self):
        print('Args dict:\n{}'.format(self._args))
        print('Args List:\n{}'.format(self.args))
        print('Flags:\n{}'.format(self._flags))
        print('Options:\n{}'.format(self._opts))
        print('Req Opts:\n{}'.format(self._req_opts))
        print('Pos:\n{}'.format(self._pos_args))
        print('Req Pos:\n{}'.format(self._req_pos_args))

    def add_arg(self, arg):
        self._add_arg_to_map(arg)

    def add_args(self, args):
        for arg in args:
            self._add_arg_to_map(arg)

    def new_arg(self, name, long='', short='', help='', action=_null_func, index=0, args_taken=0, required=False):
        arg = Arg(name,
                  long=long,
                  short=short,
                  help=help,
                  action=action,
                  index=index,
                  args_taken=args_taken,
                  required=required)
        # if long:
        #     arg.long = long
        # if short:
        #     arg.short = short
        # if help:
        #     arg.help = help
        # if action != _null_func:
        #     arg.action = action
        # if args_taken:
        #     arg.args_taken = args_taken
        # if required:
        #     arg.required = required
        # if index:
        #     arg.index = index

        self._add_arg_to_map(arg)

    def _add_help(self):
        help = Arg('help')
        help.action = self._display_help()
        help.help = 'Display help information'

        has_long = False
        has_short = False
        has_help = False
        for name in self._args_map:
            if self._args_map[name].long == 'help':
                has_long = True
                has_help = True
            if self._args_map[name].short == 'h':
                has_short = True
        if has_help:
            return
        if not has_short:
            help.short = '-h'
        if not has_long:
            help.long = '--help'

        self.add_arg(help)

    def _add_version(self):
        version = Arg('version')
        version.action = self._display_version()
        version.help = 'Display version information'

        has_long = False
        has_short = False
        has_version = False
        for name in self._args_map:
            if self._args_map[name].long == 'version':
                has_long = True
                has_version = True
            if self._args_map[name].short == 'v':
                has_short = True
        if has_version:
            return
        if not has_short:
            help.short = '-v'
        if not has_long:
            help.long = '--version'

        self.add_arg(version)

    # Properties
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    # @property
    # def args(self):
    #     return list(set(self._valid_args_map.values()))
    #
    # @args.setter
    # def args(self, value):
    #     self._args_parsed = False
    #     if value:
    #         self._build_args_map(value)

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

