# Clapp-py

An argparse like library for creating command line applications. `clapp` makes it easy to add command line switches, arguments, and sub-commands.

## Use

The most basic use of library is as follows
```python
import clapp
app = clapp.App()
app.name = 'MyApp'
app.version = '1.0'
app.about = 'A custom command line app'

app.start()
```
This will give you version displaying via the `-v` and `--version` switches as well as help information via the `-h` and `--help` switches for free.

```bash
$ ./main.py -v

MyApp v1.0
```
Or
```bash
$ ./main.py --help

MyApp v1.0
A custom command line app

USAGE:
MyApp [-vh]

FLAGS:
-v,--version		Display version information
-h,--help		    Display help information
```

### Adding Additional Arguments
Additional arguments can be added using the following (note keyword arguments can be used in the constructor instead of properties)
```python
arg1 = clapp.Arg('out_file')
arg1.short = '-o'
arg1.long = '--output'
arg1.args_taken = 1
arg1.help = 'The output file used by MyApp'

arg2 = clapp.Arg('in_file')
arg2.short = '-i'
arg2.long = '--in'
arg2.required = True
arg2.args_taken = 1
arg2.help = 'The input file used by MyApp'

# Add args to app
app.add_args([arg1, arg2])

app.start()
```
Adding positional arguments is just as easy (note positional arguments start at 1 **not** 0)
```python
arg3 = clapp.Arg('config_file')
arg3.index = 1
arg3.help = 'The config file used by MyApp'

app.add_arg(arg3)

app.start()
```
### Custom Handlers
You can add custom handlers (functions) for when certain switches are used. i.e. you could a `perform_action()` function run when an arbitrary switch is used (`-a` in this example)
```python
# Note that custom handlers must take one argument
# as they will be passed a dict() containing config
# information
def some_action(context):
    print('My action!')

arg4 = clapp.Arg('do_action')
arg4.short = '-a'
arg4.help = 'Perform some special action'
arg4.action = some_action

app.add_arg(arg4)

app.start()
```
At this point with four (4) arguments, using `-h` or `--help` would result in
```bash
$ ./main.py -h

MyApp v1.0
A custom command line app

USAGE:
MyApp [-hva] [-o out_file] <-i in_file> [config_file]

FLAGS:
-h,--help		Display help information
-v,--version	Display version information
-a				Perform some special action

OPTIONS:
-o,--output=out_file	The output file used by MyApp

REQUIRED OPTIONS:
-i,--in=in_file		The input file used by MyApp

OPTIONAL ARGUMENTS:
config_file		The config file used by MyApp
```

Sometimes you may wish to add a sub-command (akin to `git clone` style commands) which have their own switches and options independant of the main application. This is just as simple as adding arguments to an application. For example, if we wanted to add a single sub command to our `MyApp` called `fake` we could use the following:
```python
# The name of the subcommand must be unique and contain no spaces
subcmd = clapp.SubCommand('fake')
subcmd.version = '0.2'
subcmd.about = 'Does really fake things'

# If desired, we could even create a seperate main function
subcmd.main = fake_main

# We can then add additional arguemnts to fake if we wish
fake_arg1 = clapp.Arg('crazy')
fake_arg1.short = '-c'
fake_arg1.help = 'Turns on the crazy'

# You can add arguments to sub commands just like applications
subcmd.add_arg(fake_arg1)

# Once you have all the desired sub-commands you can add them to app
app.add_subcommand(subcmd)

# And start the app like normal
app.start()
```

We could then use our sub command as follows
```bash
$ ./main.py fake -c
```

Note: each sub-command gets it's own `--version` and `--help` for free. I.e.
```bash
$ ./main.py fake --help

fake v0.2
Does really fake things

USAGE:
main.py [-chv]

FLAGS:
-c		    Turns on the crazy
-h,--help	Display help information
-v,--version	Display version information
```


### TODO
#### Describe Arg
#### Describe context
