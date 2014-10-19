__author__ = 'Kevin K. <kbknapp@gmail.com>'

class Arg(object):
    def __init__(self,
                 name,
                 short='',
                 long='',
                 help='',
                 args_taken=0,
                 action=_null_func,
                 index=0,
                 required=False):
        if not id:
            raise RuntimeError('Arg(s) must have a unique id string.')
        self._id = id
        self._short_name = short_name.strip('-')
        if self._short_name and len(self._short_name) > 1:
            raise RuntimeError('Arg.short_name improper format. Must be "-h" or "h" style.')
        self._long_name = long_name.strip('-')
        self._help = help
        self._required = required
        self._has_action = False
        if action != _null_func:
            self._has_action = True
        self._action = action
        self._index = index
        self._usage = usage
        self._needs_arg = needs_arg

    @property
    def id(self):
        return self._id

    @property
    def short_name(self):
        return self._short_name

    @short_name.setter
    def short_name(self, value):
        if len(value) > 2:
            raise RuntimeError('Arg.short_name improper format. Must be "-h" or "h" style.')
        if value:
            self._short_name = value.strip('-')

    @property
    def long_name(self):
        return self._long_name

    @long_name.setter
    def long_name(self, value):
        self._long_name = value.strip('-')

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
        # if not self._usage:
        #    raise RuntimeError('Positional arguments MUST have an Arg.usage set.')
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def usage(self):
        return self._usage

    @usage.setter
    def usage(self, value):
        self._usage = value

    @property
    def needs_arg(self):
        return self._needs_arg

    @needs_arg.setter
    def needs_arg(self, value):
        self._needs_arg = value