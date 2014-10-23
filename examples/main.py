#!/usr/bin/env python

# Simply import the lib
import clapp

# This is used as the action when -o <file>
# is passed to the app.
# When options take additional arguments they
# are given a list (in this case we only expect)
# a single value so [0] is used
def do_output(context):
    print('-o was passed the file: ', context['-o'][0])

def my_main(context):
    """ The starting point for your app."""
    print('starting MyApp...')
    if context['debug']:
        print('Context:')
        for k in context:
            print('Key: {}\nValue: {}'.format(k, context[k]))
        print('Done!')
    return 0

def super_crazy(context):
    print('super crazy actions happen here!')

def super_main(context):
    print('My super sub command was called!')

if __name__ == '__main__':
    # Create an var of type clapp.App and set the properties
    # Could also use App(name='MyApp', version='1.0', about='Example CLI application')
    # etc. etc.
    #
    # Your main() should accept a dict() with which is the context
    # It will be executed AFTER all actions have returned
    app = clapp.App('My Super App')
    app.version = '1.0'
    app.about = 'Testing a command line app'
    app.author = 'Kevin K. <kbknapp@gmail.com>'
    app.main = my_main


    # Create a command line argument (can also use keyword arguments)
    # All actions should take one dict() as it will be passed a dict()
    # with context and will be executed PRIOR to your main()
    arg1 = clapp.Arg('out_file')
    arg1.short = '-o'
    arg1.long ='--output'
    arg1.args_taken = 1
    arg1.help = 'The output file'
    arg1.action = do_output

    # index starts at 1 **NOT** 0 based. Positional
    # args **MUST** have 'usage' property set
    # usage is for displaying help info and should
    # contain no whitespace or '-'s. Used in help
    # information
    # Bind the args to the 'args' property
    # (**must be a list of Arg's**)
    arg2 = clapp.Arg('in_file')
    arg2.index = 1
    arg2.help = 'The input file'
    # arg2.required = True

    # Creating a true/false flag is easy too
    arg3 = clapp.Arg('debug')
    arg3.short = '-d'
    arg3.long = '--debug'
    arg3.help = 'Print debugging info'

    arg4 = clapp.Arg('flag')
    arg4.short = '-f'
    arg4.long = '--flag'
    arg4.help = 'Use some special flag'

    subcmd = clapp.SubCommand('super')
    subcmd.version = '0.2'
    subcmd.about = 'Does super things'
    subcmd.main = super_main

    subarg = clapp.Arg('crazy')
    subarg.short = '-c'
    subarg.help = 'Does something super crazy'
    subarg.action = super_crazy

    subcmd.add_arg(subarg)

    app.add_args([arg1, arg2, arg3, arg4])
    app.add_subcommand(subcmd)

    app.start()
