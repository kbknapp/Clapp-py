# Clapp-py

`clapp` (which stands for *C*ommand *L*ine *APP*lication) is a very simple and minimal library for building command line applications and parsing command line arguments. `clapp` makes it easy to add command line switches, arguments, and sub-commands.

## Use
`clapp` gives you several things "for free" so to speak. Things such as typical unix-like help and version switches (`-h` / `--help` and`-v` / `--version` respecitivly). To get these features all you need to do is:

```python
import clapp

app = clapp.App()
app.name = 'MyApp'
app.version = '1.0'
app.about = 'A custom command line app'

app.start()

# Your code goes here
```
From this point on, you can use the typical unix-like switches. This helps users instantly identify version numbers and help information without ever having to look at a single line of code or documentation.

```bash
$ ./myapp.py -v

MyApp v1.0
```
Or

```bash
$ ./myapp.py --help

MyApp v1.0
A custom command line app

USAGE:
MyApp [-vh]

FLAGS:
-v,--version		Display version information
-h,--help		    Display help information
```

### Adding Additional Arguments
Most command line applications will want to add their own command line arguments in addition to the "for free" options that `clapp` provides. Adding those arguments is is as simple as creating a few objects and giving them to your application.

Let's say you want to allow users to pass an optional output file to use using either a `-o` or `--output` switch and the file name (Note: You do not need to use both a long and shorthand version of a switch). And you also want to  accept a mandatory positional argument, which is some input file your program needs to function. 

In order to get the information back out of the those switches and arguemnts, start will return a dictionary filled with the parsed data.
```python
# When creating an instance of clapp.Arg() the name 
# should be unique with no spaces
outfile_arg = clapp.Arg('out_file')
outfile_arg.short = '-o'
outfile_arg.long = '--output'
outfile_arg.args_taken = 1
outfile_arg.help = 'The output file used by MyApp'

# When making an argument positional, simply 
# set the index it is expected at
# Note: the index starts at 1. 1 means first 
#       *POSITIONAL* argument, not agument in general
infile_arg = clapp.Arg('in_file')
infile_arg.index = 1
infile_arg.required = True
infile_arg.args_taken = 1
infile_arg.help = 'The input file used by MyApp'

# Then you make your application aware of the arguments
# Note: when adding multiple args, you can use the App.add_args method which 
#       accepts a list of clapp.Arg objects
app.add_args([infile_arg, outfile_arg])

# Once all arguments have been added, simply start your application
context = app.start()

# Your code goes here
#
# if we ran: myapp.py -o outfile.txt infile.txt
# context looks like:
# { '-o': 'outfile.txt',
#   '--output': 'outfile.txt',
#   'out_file': 'outfile.txt',
#   'in_file': 'infile.txt',
#   'index1': 'infile.txt',
#   'raw_args': ['myapp.py', '-o', 'outfile.txt', 'infile.txt']
# }
# Note: the multiple keys each arg is stored under to give you options on
#       how you wish to call for them
```

### Custom Handlers
So far we've only seen how to check what users input. But what if we want to perform a specific action when a user passes a particular option? For this, we could define a custom handler or `action`. Let's say we want to parse a config file when the user passes a `-c` option and a config file. 

```python
# Note: Custom handlers must take one argument as they will be 
#       passed a dict() containing context values
#
# Note2: The file or parameter passed to '-c' can be looked in the
#        context dict by eitehr '-c' or the name you chose (in this
#        case we use 'config')
def parse_config(context):
    print('The config file being parsed is {}'.format(context['config']))

config_arg = clapp.Arg('config')
config_arg.short = '-c'
config_arg.help = 'The config file to parse'
config_arg.args_take = 1
config_arg.action = parse_config

app.add_arg(config_arg)

app.start()
```
It is important to note that if you define custom handlers they will be executed **BEFORE** `start()` returns.

At this point with four (3) arguments, using `-h` or `--help` would result in
```bash
$ ./myapp.py -h

MyApp v1.0
A custom command line app

USAGE:
MyApp [-hv] [-o out_file -c config_file] <in_file>

FLAGS:
-h,--help		Display help information
-v,--version	Display version information

OPTIONS:
-o,--output=out_file	The output file used by MyApp
-c                      The config file to parse

REQUIRED OPTIONS:
in_file         		The input file used by MyApp
```
#### Overriding `-v` or `-h`
You may freely override the `-v` or `-h` switches just as you would a normal argument (those options are only given to our program for free if `clapp` determines that you have not provided your own implementations). You may also provide your own `--help` or `--verison` switches as well.

### Adding a `main()`
In the event that you do not wish to simply start your code directly after calling `start()` you may add your own `main()` function, just like you would add other properties of your application. For instance, using the `if __name__` idiom.

```python
# Note: your main needs to accept a dict containing
#       the context information described earlier
def app_main(context):
    # Your code goes here

if __name__ == '__main__':
    #
    # clapp.App initialization from previous examples goes here
    #
    
    app.main = app_main
    
    app.start()
```

Note: When using custom handlers and a main, all custom handlers are called and executed **BEFORE** your `main()` is called.

### Sub-Commands
Sometimes you may wish to add a sub-command (akin to `git clone` style commands) which have their own switches and options independant of the main application. This is just as simple as adding arguments to an application. For example, if we wanted to add a single sub command to our `MyApp` called `fake` we could use the following:
```python
# The name of the subcommand must be unique and contain no spaces
fake_cmd = clapp.SubCommand('fake')
fake_cmd.version = '0.2'
fake_cmd.about = 'Does really fake things'

# If desired, we could even create a seperate main function
fake_cmd.main = fake_main

# We can then add additional arguemnts to fake if we wish
fake_crazy_arg = clapp.Arg('crazy')
fake_crazy_arg.short = '-z'
fake_crazy_arg.help = 'Turns on the crazy'

# You can add arguments to sub commands just like applications
fake_cmd.add_arg(fake_crazy_arg)

# Once you have all the desired sub-commands you can add them to app
app.add_subcommand(fake_cmd)

# And start the app like normal
app.start()
```

We could then use our sub command as follows
```bash
$ ./myapp.py fake -z
```

Note: each sub-command gets it's own `--version` and `--help` for free. I.e.
```bash
$ ./myapp.py fake --help

fake v0.2
Does really fake things

USAGE:
main.py fake [-zhv]

FLAGS:
-z		    Turns on the crazy
-h,--help	Display help information
-v,--version	Display version information
```
### `clapp.Arg`
The `clapp.Arg` object defines the following possible properties with descriptions of their use
```python
# As discussed the name must be unique with no spaces
myarg = clapp.Arg('name')

# `short` and `long` define switches to denote the argument
# both are optional
# Note: when defining a short, it must start with a leading '-'
#       and contain only one letter
myarg.short = '-d'
# Note: when defining a long, it must start with a leading '--'
#       and contain no spaces
myarg.long = '--debug'

# When defining an action, your function should accept a dict
myarg.action = some_func

# The help string that will be displayed when the user uses the -h or --help
myarg.help = 'Describe your argument or option here'

# If defining a positional argument (i.e. no -f or --fake)
# you must not define a `short` or `long`
# Note: the index starts at 1 **NOT** 0
# Note 2: The index specifies the relationship to other **POSITIONAL** arguments
#         not arguments in general
myarg.index = 1

# Defines if an argument is mandatory for your application to function
# if you specify that an argument is mandatory, and the parser determines
# that it was not found, your application will display the usage message
# and exit (**WITHOUT** calling your main() if it is defined)
#
# Note: If you define a `short` or `long` and set this property to true
#       you **MUST** also set the `args_taken` property to something
#       greater than 0 (i.e. there is no such thing as mandatory flag
myarg.required = False

# If your arguments needs additional positional arguments you can define
# how many to expect here.
# i.e. if you define a -c <some_file> you can set the `args_taken` to 1
# When you choose a number greater than 0, all valid positional arguments
# directly following your switch (i.e. -c or whatever) will be stored
# in a list inside the context dict
#
# Note: if your argument does not need additional arguments (i.e. it is a flag)
#       and the user **DOES NOT** use the flag, it will still exist in your
#       context dict, but the valid associated with it will be `False`
myarg.args_taken = 2
```

### TODO
#### Describe context
