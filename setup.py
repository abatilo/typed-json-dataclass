import os
import sys

from setuptools import setup
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.2.2'
about = {'version': VERSION}

with open(
    os.path.join(here, 'typed_json_dataclass', '__init__.py'), 'r',
    encoding='utf-8'
) as f:
    for line in f:
        if line.startswith('__version__'):
            about['version'] = line.strip().split('=')[1].strip(' \'"')

with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    README = f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = ('Git tag: {0} does not match '
                    'the version of this app: {1}').format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name='typed_json_dataclass',
    version=about['version'],
    url='http://github.com/abatilo/typed_json_dataclass/',
    license='MIT',
    author='Aaron Batilo',
    author_email='aaronbatilo@gmail.com',
    maintainer='Aaron Batilo',
    maintainer_email='aaronbatilo@gmail.com',
    description='Make your dataclasses automatically validate their types',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=['typed_json_dataclass'],
    package_data={'typed_json_dataclass': ['typed_json_dataclass/*']},
    platforms='any',
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='dataclasses dataclass json mypy pyre marshmallow attrs cattrs',
    python_requires='==3.7.*',
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
