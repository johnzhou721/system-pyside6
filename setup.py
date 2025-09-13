# setup.py
import os
import sys
import sysconfig
import pathlib
import csv
from io import StringIO
from setuptools import setup
from setuptools.command.install import install
from wheel.wheelfile import WheelFile
from zipfile import ZipFile

BASE_PREFIX = getattr(sys, "real_prefix", None) or getattr(sys, "base_prefix", None) or sys.prefix

def system_site_packages():
    base = BASE_PREFIX
    paths = {
        "purelib": sysconfig.get_path("purelib", vars={"base": base, "platbase": base}),
        "platlib": sysconfig.get_path("platlib", vars={"base": base, "platbase": base}),
    }
    return [p for p in (paths["purelib"], paths["platlib"]) if p and os.path.exists(p)]

venv_site = sysconfig.get_paths()['purelib']
sites = system_site_packages()

class SystemLinker(install):
    def run(self):
        super().run()
        if BASE_PREFIX == sys.prefix:
            raise SystemExit("Must be installed in venv")

        for pkg in ("PySide6", "shiboken6"):
            src = None
            for sitedir in sites:
                if (pathlib.Path(sitedir) / pkg).exists():
                    src = pathlib.Path(sitedir) / pkg
                    break
            if src is None:
                raise SystemExit(f"Can't find {pkg} in system site packages")
            dst = pathlib.Path(venv_site) / pkg
            if dst.exists():
                raise SystemExit(f"{pkg} already exists in venv. Uninstall it first.")
            print(f"Linking: {src} → {dst}")
            dst.symlink_to(src)

        print("PySide6 and shiboken6 linked")

old_close = WheelFile.close
def __WheelFile_close(self):
    if self.fp is not None and self.mode == "w" and self._file_hashes:
        data = StringIO()
        writer = csv.writer(data, delimiter=",", quotechar='"', lineterminator="\n")
        writer.writerows(
            ((fname, algorithm + "=" + hash_, self._file_sizes[fname])
             for fname, (algorithm, hash_) in self._file_hashes.items())
        )
        writer.writerow((format(self.record_path), "", ""))
        writer.writerow(("shiboken6", "", ""))
        writer.writerow(("PySide6", "", ""))
        self.writestr(self.record_path, data.getvalue())
    ZipFile.close(self)

old_init = WheelFile.__init__
def __WheelFile__init__(self, *args, **kwargs):
    old_init(self, *args, **kwargs)
    try:
        mode = args[1]
    except IndexError:
        mode = kwargs['mode']
    if mode == "r":
        self._file_hashes["PySide6"] = None, None
        self._file_hashes["shiboken6"] = None, None

WheelFile.close = __WheelFile_close
WheelFile.__init__ = __WheelFile__init__

setup(
    name="system-pyside6",
    version=0.0.1,
    description="Hack system PySide6 and shiboken6 into venv",
    py_modules=[],
    install_requires=[],
    cmdclass={"install": SystemLinker},
)
