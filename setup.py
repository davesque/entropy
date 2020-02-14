from setuptools import setup, find_packages

setup(
    name="entropy", packages=find_packages(), install_requires=["pytest", "hypothesis"],
)
