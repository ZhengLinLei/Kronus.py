from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.exceptions import InstallationError

try:
    requirements = parse_requirements("./src/requirements.txt") # THE FILE IS INSIDE THE SRC FOLDER
    install_requires = [str(r.req) for r in requirements]
except InstallationError:
    requirements = parse_requirements("./requirements.env.txt") # SETUP ALL ENV
    install_requires = [str(r.req) for r in requirements]

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = "Kronus virtual assistant"

setup(
    name="Kronus.py",
    version="1.0.0",
    description="Kronus bot",
    license="Apache-2.0",
    author="ZLL",
    packages=find_packages(),
    install_requires=install_requires,
    long_description=long_description
)
