import re
from os.path import join, dirname

from setuptools import setup, find_packages


with open(join(dirname(__file__), 'inception', '__init__.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read()).group(1)


dependencies = [
    'restfulpy >= 2.9.0',
]


setup(
    name='inception',
    author='mehdi',
    author_email='mehdinazari@carrene.com',
    version=package_version,
    install_requires=dependencies,
    packages=find_packages(),
    test_suite='inception.tests',
    entry_points={
        'console_scripts': [
            'inception = inception:inception.cli_main'
        ]
    }
)

