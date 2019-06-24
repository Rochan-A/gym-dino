from setuptools import setup
import os

setup(name='gym_dino',
	version='0.0.1',
	install_requires=['gym', 'pygame'],

	package_data={ 'gym_dino': ['gym_dino/envs/sprites/*'] },
	include_package_data=True
)
