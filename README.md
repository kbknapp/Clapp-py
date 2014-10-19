# Clapp-py

A library for creating command line applications. `clapp` makes it easy to add command line switches and arguments, as well as create a robust menu system.

## Use

The most basic use of library is as follows
```python
import clapp
app = clapp.clapp()
app.name = 'MyApp'
app.version = '1.0'
app.about = 'A custom command line app'

app.start()
```
This will give you version displaying via the `-v` and `--version` switches as well as help information via the `-h` and `--help` switches.

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
-h,--help		Display help information

```

### Adding Additional Arguments
Additional arguments can be added using the following (note keyword arguments can be used in the constructor instead of properties)
```python
arg1 = clapp.CliArg()
arg1.short_name = '-o'
arg1.long_name = '--output'
arg1.needs_arg = True
arg1.usage = 'out_file'
arg1.help = 'The output file used by MyApp'

arg2 = clapp.CliArg()
arg2.short_name = '-i'
arg2.long_name = '--in'
arg2.required = True
arg2.needs_arg = True
arg2.usage = 'in_file'
arg2.help = 'The input file used by MyApp'

# Add args to app
app.args = [arg1, arg2]

app.start()
```
Adding positional arguments is just as easy (note when using positional arguments, you **MUST** set the `usage` property)
```python
arg3 = clapp.CliArg()
arg3.pos = 1	# pos starts at 1, it is **NOT** 0 based
arg3.usage = 'config_file'
arg3.help = 'The config file used by MyApp'

app.args = [arg3]

app.start()
```
### Custom Handlers
You can add custom handlers (functions) for when certain switches are used. i.e. you could a `perform_action()` function run when an arbitrary switch is used (`-a` in this example)
```python
# Note that custom handlers must take one argument
# as they will be passed a dict() containing config
# information
def some_action(config):
    print('My action!')

arg4 = clapp.CliArg()
arg4.short_name = '-a'
arg4.help = 'Perform some special action'
arg4.action = some_action

app.args = [arg4]

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

### TODO
#### Describe CliArg
#### Describe clapp options
#### Describe Handlers (clapp.action)
#### Describe clapp.config
