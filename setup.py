from setuptools import setup, find_packages

with open("requirements.txt") as f:
    reqs = f.read()

setup(
    name="pikautil",
    version="0.1",
    packages=find_packages(include=["pikautil"]),
    license="LICENSE.txt",
    long_description=open("README.md").read(),
    install_requires=reqs.strip().split("\n"),
)
