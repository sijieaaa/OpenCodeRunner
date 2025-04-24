from setuptools import setup, find_packages


with open("requirements.txt", encoding="utf-8") as f:
    install_requires = [
        line.strip()
        for line in f.readlines()
        if line.strip() and not line.startswith("#")
    ]

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
    install_requires=install_requires,
    license="Apache-2.0",
    classifiers=[
        "License :: OSI Approved :: Apache-2.0",
    ]
)
