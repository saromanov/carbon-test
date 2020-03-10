import io
import re

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="Flask",
    version='1.0',
    url="https://github.com/saromanov/serload",
    license="MIT",
    author="Sergey Romanov",
    author_email="xxsmotur@gmail.com",
    description="Test task for Carbonsoft",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=[
       "flask",
       "sqlalchemy",
       "flask_sqlalchemy"
    ],  
)