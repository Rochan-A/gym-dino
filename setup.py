from setuptools import setup
import os

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(name='gym_dino',
	version='0.0.4',
	long_description=long_description,
	long_description_content_type='text/markdown',
	install_requires=['gym', 'pygame'],

	package_data={ 'gym_dino': ['gym_dino/envs/sprites/*'] },
	include_package_data=True
)
