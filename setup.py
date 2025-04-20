import os
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

setup(
    name="opencoderunner",
    version="0.1",
    description="OpenCodeRunner: A FastAPI-based code execution server",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Sijie Wang",
    author_email="wang1679@e.ntu.edu.sg",
    python_requires=">=3.8",
    packages=find_packages(include=["opencoderunner", "opencoderunner.*"]),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic>=2.0.0",
        "requests",
        "matplotlib",
        "msgpack",
        "numpy",
        "Pillow",
        "python-dotenv",
        "tqdm"
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ]
)
