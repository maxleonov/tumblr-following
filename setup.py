import sys

from setuptools import find_packages, setup

from tower.version import __version__


INSTALL_REQUIRES = [x for x in open('requirements.txt').readlines()]


setup(
    name='tumblr-following',
    description='A tool that helps a Tumblr user to clean up the list of blogs they follow',
    author='Maxim Leonov',
    author_email='maks.leonov@gmail.com',
    url='https://github.com/maxleonov/tumblr-following/',
    version=__version__,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "tower = tower.__main__:main"
        ]
    },
)
