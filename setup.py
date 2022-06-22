# standard imports
import logging
import subprocess
import time
from setuptools import setup

# local imports

logg = logging.getLogger()

requirements = []
with open('requirements.txt', 'r') as requirements_file:
    while True:
        requirement = requirements_file.readline()
        if requirement == '':
            break
        requirements.append(requirement.rstrip())
test_requirements = []
with open('test_requirements.txt', 'r') as test_requirements_file:
    while True:
        test_requirement = test_requirements_file.readline()
        if test_requirement == '':
            break
        test_requirements.append(test_requirement.rstrip())
setup(install_requires=requirements, tests_require=test_requirements)
