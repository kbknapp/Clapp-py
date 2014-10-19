#!/usr/bin/env python

# Simply import the lib
import clapp


# is used as the action when -o <file> is passed to the app
def do_output(context):
    print('-o was passed the file: ', context['out'])


def my_main(context):
	""" The starting point for your app."""
	print('starting MyApp...')
	print('Context:')
	for k in context:
		print('Key: {}\nValue: {}'.format(k, context[k]))
	print('Done!')
	return 0


# Create a command line argument, can also used keyword arguments
# All actions should take one dict() as it will be passed a dict() with config info
# and will be executed PRIOR to your main()
# your main() should accept a dict() with config
# It will be executed AFTER all actions have returned
arg1 = clapp.Arg('out_file')
arg1.short = 'o'
arg1.long ='output'
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
arg2.required = True


# Create an var of type Clapp and set the properties
#
# Could also use Clapp(name='MyApp', version='1.0', about='Example CLI application') etc. etc.
# You can call the atributes in any order, but start() MUST be called last
app = clapp.App()
app.name = 'MyApp'
app.version = '1.0'
app.about = 'Testing a command line app'
app.main = my_main
app.add_args([arg1, arg2])

app.start()
