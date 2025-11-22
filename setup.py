from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py

# Referenced answer
# https://stackoverflow.com/questions/2145779/setup-py-installing-just-a-pth-file
# "Copy pth during build_by without preserving mode" is probably not copyrightable


class add_pyside6(build_py):
    def run(self):
        super().run()
        self.copy_file(
            "system_pyside6.pth",
            str(Path(self.build_lib) / "system_pyside6.pth"),
            preserve_mode=0,
        )


setup(
    cmdclass={"build_py": add_pyside6},
)
