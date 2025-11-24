# ARCHIVED

This is being integrated into BeeWare upstream.

# system-pyside6

In the Qt ecosystem, platform-specific style plugins are compiled strictly against for use for a specific Qt version, and by virtue of how binding generators work, the PySide6 version must be tied to the Qt runtime and version.  Thus, installing PySide6 in venv, it is impossible to integrate with system themes.  This package solves the problem by allowing the import of PySide6 outside of venv, but the isolation is not broken for other packages; access of metadata is also allowed.
