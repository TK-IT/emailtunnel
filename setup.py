# License:
#   "THE BEER-WARE LICENSE" (Revision 42):
# <TKIT@TAAGEKAMMERET.dk> wrote these files. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us some beer in return. TÅGEKAMMERET

from setuptools import setup, find_packages
import emailtunnel


headline = emailtunnel.__doc__.split('\n', 1)[0].rstrip('.')


setup(
    name='emailtunnel',
    version='0.1',
    packages=find_packages(include=['emailtunnel', 'emailtunnel.*']),
    description=headline,
    long_description=emailtunnel.__doc__,
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
)
