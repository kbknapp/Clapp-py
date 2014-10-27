import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('clapp/clapp.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))
setup(
    name='clapp',
    author='Kevin Knapp',
    author_email='kbknapp@gmail.com',
    version=version,
    url='http://github.com/kbknapp/Clapp-py',
    packages=['clapp'],
    description='A small package for easily creating'
                ' command line applications',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Pyhthon :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
