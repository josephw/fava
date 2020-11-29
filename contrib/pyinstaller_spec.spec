# vim: set ft=python:
"""Pyinstaller spec file for building a binary from fava's cli.py"""
import importlib
import os

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import copy_metadata

hidden_imports = collect_submodules(
    "beancount", filter=lambda name: "test" not in name
)

data_files = [
    ("../src/fava/help", "fava/help"),
    ("../src/fava/static", "fava/static"),
    ("../src/fava/templates", "fava/templates"),
    ("../src/fava/translations", "fava/translations"),
]

# add fava version information:
data_files += copy_metadata("fava")

# add beancount version file:
beancount_dir = os.path.dirname(importlib.import_module("beancount").__file__)
beancount_version_file = os.path.join(beancount_dir, "VERSION")
data_files += [(beancount_version_file, "beancount")]

a = Analysis(
    ["../src/fava/cli.py"],
    pathex=["."],
    datas=data_files,
    hiddenimports=hidden_imports,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='fava',
          upx=True,
)