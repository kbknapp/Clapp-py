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
        self._short = short_name.strip('-')
        if self._short and len(self._short) != 2:
            raise RuntimeError('Arg.short improper format. Must be "-h" style.')
        self._long = long.strip('-')
        self._help = help
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
    def short(self):
        return self._short

    @short.setter
    def short_name(self, value):
        if len(value) != 2:
            raise RuntimeError('Arg.short improper format. Must be "-h" style.')
        if value:
            self._short = value

    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, value):
        if not value.startswith('--'):
            raise RuntimeError('Arg.long improper format. Must be in "--help" style.')
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

    # @property
    # def usage(self):
    #     return self._usage
    #
    # @usage.setter
    # def usage(self, value):
    #     self._usage = value

    @property
    def args_taken(self):
        return self._args_taken

    @args_taken.setter
    def args_taken(self, value):
        self._args_taken = value