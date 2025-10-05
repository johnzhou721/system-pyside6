from setuptools.command.build_py import build_py
from setuptools import setup
from pathlib import Path
import os


# Referenced answer
# https://stackoverflow.com/questions/2145779/setup-py-installing-just-a-pth-file
# "Copy pth during build_by without perserving mode" is probably not copyrightable

class add_pyside6(build_py):
     def run(self):
         super().run()
         self.copy_file("PySide6.pth", str(Path(self.build_lib) / "PySide6.pth"), preserve_mode=0)

setup(
    name="system-pyside6",
    version="0.0.1",
    packages=["system_pyside6"],
    package_dir={'system_pyside6': '.'},
    python_requires=">=3.9",
    author="John Zhou",
    description="Installs PySide6.pth to access system PySide6",
    cmdclass={"build_py": add_pyside6},
)
