#!/usr/bin/env python
'''
Python 3.x

app.py

v0.2

A library for building command line applications
'''
import sys
import arg

__version__ = '0.2'
__author__ = 'Kevin K. <kbknapp@gmail.com>'

def _null_func(context):
    pass


class Clapp(object):
    def __init__(self, name='', version='', about='', main=_null_func):
        self._name = name
        self._version = version
        self._args_map = dict()
        self._valid_args = []
        # self._raw_args = ''
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
        self._num_pos_args = 0
        self._num_req_pos_args = 0
        self._num_req_opts = 0

    def start(self):
        if self._needs_help():
            self.add_arg(Arg('help', long_name='--help',
                        help='Display help information', action=self._display_help))
        if self._needs_version():
            self.add_arg(Arg('version', long_name='--version',
                        help='Display version information', action=self._display_version))
        self._build_args_map()
        if len(sys.argv) > 1:
            self._context['raw_args'] = sys.argv[1:]
            self._do_args(sys.argv[1:])

        if self._has_main:
            self._main(self._context)

    def _do_args(self, args):
        if self._args_parsed:
            return

        # valid = False
        ignore_next = False
        todo = []
        num_req_pos = self._num_req_pos_args
        num_pos = self._num_pos_args + num_req_pos
        cur_pos = 1

        # for ak in self._args:
        #    if self._args[ak].pos:
        #        num_pos += 1
        for i, a in enumerate(self._raw_args[1:]):
            next_arg = ''
            if ignore_next:
                ignore_next = False
                continue
            if a[1] == '-':
                # Arg start with --, so probably --times style
                # Check if arg is something like --times=20
                if a.find('=') != -1:
                    s = a.split('=')
                    # Set a to --times and next_arg to 20
                    a = s[0]
                    next_arg = s[1]
                a = a.strip('-')
                if a not in self._valid_arg_strings:
                    print('Supplied argument isn\'t valid')
                    self._display_usage()
                valid_arg = self._valid_args_map[a]
                if valid_arg.needs_arg:
                    if not next_arg:
                        next_arg = self._raw_args[i+1]
                        ignore_next = True
                    if next_arg[0] == '-':
                        self._display_usage()
                    self._context[valid_arg.id] = next_arg
                else: 
                    self._context[valid_arg.id] = True
                if valid_arg.has_action:
                    todo.append(valid_arg.action)
            elif a[0] == '-':
                # Not --times style
                # could be -f<file> style though
                if a[1] in self._valid_arg_strings:
                    valid_arg = self._valid_args_map[a[1]]
                    if self._valid_args_map[a[1]].needs_arg:
                        if len(a) > 2:
                            # It is...
                            #a = a.strip('-')
                            next_arg = a[2:]
                        else:
                            next_arg = self._raw_args[i+1]
                            ignore_next = True
                        if next_arg[0] == '-':
                            self._display_usage()
                        self._context[valid_arg.id] = next_arg
                    self._context[valid_arg.id] = True
                    if valid_arg.has_action:
                        todo.append(valid_arg.action)
                else:
                    print('Supplied argument invalid')
                    self._display_usage()
            else:
                # Maybe positional
                if not num_pos:
                    # There shouldn't be any positional
                    print('Too many positional arguments supplied')
                    self._display_usage()
                valid_arg = self._valid_args_map['posarg{}'.format(cur_pos)]
                self._context[valid_arg.id] = a
                if valid_arg.has_action:
                    todo.append(valid_arg.action)
                num_pos -= 1
                cur_pos += 1
                num_req_pos -= 1

        if num_req_pos > 0:
            print('Required arguments not found...')
            self._display_usage()

        for id in self._req_opts:
            if id not in self._context:
                print('Required arguments not found...')
                self._display_usage()

        # DEBUG
        # self._debug()

        for f in todo:
            f(self._context)
        self._args_parsed = True

    def _display_usage(self, no_exit=False):
        ''' Displays usage of app based of flags and options
        name.py [flags] <req_opts> [opt_opts] <req_bald_args> [bald_args]
        '''
        usage_str = ''
        if self._flags:
            usage_str += '[-{}]'.format(''.join([self._valid_args_map[fid].short_name for fid in self._flags]))
        if self._opts:
            usage_str += ' [{}]'.format(' '.join([self._valid_args_map[oid].short_name for oid in self._opts]))
        if self._req_opts:
            usage_str += ' <{}>'.format(' '.join([self._valid_args_map[roid].short_name for roid in self._req_opts]))
        if self._req_pos_args:
            usage_str += ' <{}>'.format(' '.join([self._valid_args_map[rpid].usage for rpid in self._req_pos_args]))
        if self._pos_args:
            usage_str += ' [{}]'.format(' '.join([self._valid_args_map[poid].usage for poid in self._pos_args]))
        print('\nUSAGE:\n{} {}'.format(self.name, usage_str))
        if not no_exit:
            print('\nFor more information try --help or -h')
            sys.exit(0)

    def _display_help(self, config=None):
        print('\n{} v{}\n{}'.format(self.name, self.version, self.about))
        self._display_usage(no_exit=True)
        if self._flags:
            print('\nFLAGS:')
            for f in self._flags:
                a = self._args[f]
                print(a.short_name, end='')
                if a.short_name and a.long_name:
                    print(',', end='')
                else:
                    print('\t', end='')
                print('{}\t\t{}'.format(a.long_name, a.help))

        if self._opts:
            print('\nOPTIONS:')
            for f in self._opts:
                o = self._args[f[0:f.find(' ')]]
                print(o.short_name, end='')
                if o.short_name and o.long_name:
                    print(',', end='')
                print('{}={}\t{}'.format(o.long_name, o.usage, o.help))
        if self._req_opts:
            print('\nREQUIRED OPTIONS:')
            for f in self._req_opts:
                ro = self._args[f[0:f.find(' ')]]
                print(ro.short_name, end='')
                if ro.short_name and ro.long_name:
                    print(',', end='')
                print('{}={}\t\t{}'.format(ro.long_name, ro.usage, ro.help))
        if self._req_pos_args:
            print('\nREQUIRED ARGUMENTS:')
            for f in self._req_pos_args:
                rpo = self._args[f]
                print('{}\t\t{}'.format(rpo.usage, rpo.help))
        if self._pos_args:
            print('\nOPTIONAL ARGUMENTS:')
            for f in self._pos_args:
                po = self._args[f]
                print('{}\t\t{}'.format(po.usage, po.help))
        sys.exit(0)

    def _display_version(self, config=None):
        print('\n{} v{}'.format(self._name, self._version))
        sys.exit(0)

    def _build_args_map(self, args):
        """Builds a dict of possible valid arguments."""
        for a in args:
            if a.id in self._args_map:
                raise RuntimeError('Arg.id must be unique.')
            self._args_map[a.id] = a
            # Get all the required options, flags, etc
            if a.required:
                # Only positional and options can be required (i.e. no such
                # thing as mandatory flag)
                if a.index:
                    self._num_req_pos_args += 1
                    self._req_pos_args.append(a.id)
                else:
                    self._num_req_opts += 1
                    self._req_opts.append(a.id)
            else:
                if a.index:
                    self._num_pos_args += 1
                    self._pos_args.append(a.id)
                elif a.needs_arg:
                    self._opts.append(a.id)
                else:
                    self._flags.append(a.id)
            if a.short_name:
                self._args_map[a.short_name] = a
                self._valid_args.append(a.short_name)
            if a.long_name:
                self._args_map[a.long_name] = a
                self._valid_args.append(a.long_name)
            if a.index:
                self._valid_args_map['posarg{}'.format(a.index)] = a


    def _debug(self):
        print('Args dict:\n{}'.format(self._args))
        print('Args List:\n{}'.format(self.args))
        print('Flags:\n{}'.format(self._flags))
        print('Options:\n{}'.format(self._opts))
        print('Req Opts:\n{}'.format(self._req_opts))
        print('Pos:\n{}'.format(self._pos_args))
        print('Req Pos:\n{}'.format(self._req_pos_args))

    def add_arg(self, arg):
        return self.args([arg])

    def _needs_help(self):
        for a in self._args_map.values():
            if a.long_name.strip('-') == 'version':
                return False
        return True

    def _needs_version(self):
        for a in self._args_map.values():
            if a.long_name.strip('-') == 'help':
                return False
        return True

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

    @property
    def args(self):
        return list(set(self._valid_args_map.values()))

    @args.setter
    def args(self, value):
        self._args_parsed = False
        if value:
            self._build_args_map(value)

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

