from setuptools import setup, find_packages

setup(
    name='golf_society',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy'
    ],
)
