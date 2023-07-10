#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION='0.0.3'

setup(name='isub',
	version=VERSION,
	description='A tool for running scripts on an OpenShift cluster',
	url='http://github.com/jakelever/isub',
	author='Jake Lever',
	author_email='jake.lever@gmail.com',
	license='MIT',
	packages=['isub'],
	install_requires=[],
        package_data={'': ['isub/run_script.sh','isub/run_command.sh','isub/template.yml']},
	include_package_data=True,
	entry_points = {
		'console_scripts': ['isub=isub.main:main'],
	})

