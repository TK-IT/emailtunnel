# License:
#   "THE BEER-WARE LICENSE" (Revision 42):
# <TKIT@TAAGEKAMMERET.dk> wrote these files. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us some beer in return. TÅGEKAMMERET

import os
import ast
from setuptools import setup, find_packages


# Get the docstring out without importing the file
init_filename = os.path.join(
    os.path.dirname(__file__), 'emailtunnel/__init__.py')
with open(init_filename) as fp:
    tree = ast.parse(fp.read())
    long_description = tree.body[0].value.s


headline = long_description.split('\n', 1)[0].rstrip('.')


setup(
    name='emailtunnel',
    version='0.1',
    packages=find_packages(include=['emailtunnel', 'emailtunnel.*']),
    description=headline,
    long_description=long_description,
    author='https://github.com/Mortal',
    url='https://github.com/Mortal/emailtunnel',
    include_package_data=True,
    license='THE BEER-WARE LICENSE',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'aiosmtpd',
    ],
)
