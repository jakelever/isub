#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION='0.0.1'

setup(name='isub',
	version=VERSION,
	description='A tool for running scripts on an OpenShift cluster',
	url='http://github.com/jakelever/isub',
	author='Jake Lever',
	author_email='jake.lever@gmail.com',
	license='MIT',
	packages=['isub'],
	install_requires=[],
	include_package_data=True,
	entry_points = {
		'console_scripts': ['isub=isub.main:main'],
	})

