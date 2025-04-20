import os
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

def write_opencoderunner_home_to_bashrc():
    bashrc_path = os.path.expanduser("~/.bashrc")
    install_path = os.getcwd()
    export_line = f'export OEPNCODERUNNER_HOME={repr(install_path)}'
    alias_line = 'alias opencoderunner-start-server="bash $OEPNCODERUNNER_HOME/start_server.sh"'

    try:
        with open(bashrc_path, "r") as f:
            bashrc_content = f.read()

        updated = False

        # Add OEPNCODERUNNER_HOME if not already present
        if "OEPNCODERUNNER_HOME" not in bashrc_content:
            with open(bashrc_path, "a") as f2:
                f2.write(f"\n# Added by OpenCodeRunner setup\n{export_line}\n")
            print(f"✅ OEPNCODERUNNER_HOME has been added to ~/.bashrc")
            updated = True
        else:
            print("ℹ️ OEPNCODERUNNER_HOME already exists in ~/.bashrc")

        # Add alias for start-opencoderunner
        if "start-opencoderunner" not in bashrc_content:
            with open(bashrc_path, "a") as f2:
                f2.write(f"{alias_line}\n")
            print("✅ Alias start-opencoderunner has been added to ~/.bashrc")
            updated = True
        else:
            print("ℹ️ Alias start-opencoderunner already exists in ~/.bashrc")

        if updated:
            print("👉 Please run `source ~/.bashrc` to activate the changes")

    except Exception as e:
        print(f"⚠️ Failed to write to ~/.bashrc: {e}")

class CustomInstallCommand(install):
    def run(self):
        super().run()
        write_opencoderunner_home_to_bashrc()

class CustomDevelopCommand(develop):
    def run(self):
        super().run()
        write_opencoderunner_home_to_bashrc()

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
    ],
    cmdclass={
        "install": CustomInstallCommand,
        "develop": CustomDevelopCommand,
    }
)
