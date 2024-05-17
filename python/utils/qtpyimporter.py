"""Qt Importer using Qt.Py to first convert to PySide2 bindings."""
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
# from builtins import *
# from future.builtins.disabled import *

import logging

from sgtk.log import LogManager
from sgtk.util.pyside2_patcher import PySide2Patcher
from sgtk.util.qt_importer import QtImporter

from .pyqt5patcher import PyQt5Patcher

LOG = logging.getLogger(__name__)

__all__ = ('QtPyImporter',)


class QtPyImporter(QtImporter):
    """Extend QtImporter to use Qt.py.

    Due to our patcher and Qt.py is local to tk_katana, this class is
    defined within this method to utilise modules imported by
    the engine's ``import_module()``.

    Attributes:
        logger (logging.Logger):
            Standard Python logger for this Importer.
        interface_version_requested (int):
            Qt interface version requested during construction.
        base (dict[str]):
            Mapping of Qt module, class and bindings names.
    To Do:
        Refactor and upstream our attributes to
        ``sgtk.util.qt_importer.QtImporter``.
    """

    def __init__(self, qt=None, interface_version_requested=QtImporter.QT4):
        """Extended to add local logger.

        Args:
            qt (module):
                Qt.py module (e.g dynamically imported from vendor)
            interface_version_requested (int):
                Custom version of the Qt API is requested.
        """
        self.Qt = qt
        if self.Qt is None:
            import Qt
            self.Qt = Qt

        self._interface_version_requested = interface_version_requested
        self._logger = LogManager.get_logger(self.__class__.__name__)
        super(QtPyImporter, self).__init__(interface_version_requested)

    def _import_qt_dot_py_as_pyside(self):
        """Imports using Qt.py, re-map for PySide using PyQt5Patcher.

        This method is where the magic happens. See the class docs
        for ``PyQt5Patcher`` for more details on PyQt5 patching.

        Returns:
            tuple(str, str, module, dict[str, module], tuple[int]):
                - Binding name
                - Binding version
                - Qt module
                - QtCore, QtGui, QtNetwork and QtWebKit mapping
                - Version as a tuple of integers
        """
        if self.Qt.__binding__ == 'PyQt5':
            QtCore, QtGui = PyQt5Patcher.patch(
                self.Qt.QtCore,
                self.Qt.QtGui,
                self.Qt.QtWidgets,
            )
        else:
            QtCore, QtGui = PySide2Patcher.patch(
                self.Qt.QtCore,
                self.Qt.QtGui,
                self.Qt.QtWidgets,
                'UNUSED LOL (Shotgun, please fix)'
            )

        QtNetwork = getattr(self.Qt, "QtNetwork", None)

        # Might be ugly mate, see deprecation:
        # https://doc.qt.io/qt-5/qtwebenginewidgets-qtwebkitportingguide.html
        QtWebKit = getattr(self.Qt, "QtWebEngineWidgets", None)

        return (
            "Qt",
            self.Qt.__version__,
            self.Qt,
            {
                "QtCore": QtCore,
                "QtGui": QtGui,
                "QtNetwork": QtNetwork,
                "QtWebKit": QtWebKit,
            },
            self._to_version_tuple(QtCore.qVersion()),
        )

    def _import_modules(self, interface_version):
        """Import Qt bindings for a given interface version.

        Tries to import binding implementations in the following order:

        - Qt.py (Uses PySide2 standards)
        - PySide2
        - PySide
        - PyQt4

        Returns:
            tuple(str, str, module, dict[str, module], tuple[int]):
                - Binding name
                - Binding version
                - Qt module
                - QtCore, QtGui, QtNetwork and QtWebKit mapping
                - Version as a tuple of integers

                Or all are ``None`` if no bindings are available.
        """
        self.logger.debug(
            "Requesting %s-like interface",
            "Qt4" if interface_version == self.QT4 else "Qt5"
        )

        # First try Qt.Py
        if interface_version == self.QT4:
            try:
                qt_dot_py = self._import_qt_dot_py_as_pyside()
                self.logger.debug("Imported Qt.py as PySide.")
                return qt_dot_py
            except ImportError:
                pass

        # Then try parent class's bindings.
        return super(QtPyImporter, self)._import_modules(
            interface_version
        )

    @property
    def interface_version_requested(self):
        """Get the interface version requested during construction.

        Returns:
            int: Qt interface version requested during construction.
        """
        return self._interface_version_requested

    @property
    def logger(self):
        """Get the Python logger

        Returns:
            logging.Logger: Standard Python logger for this importer.
        """
        return self._logger

    @property
    def base(self):
        """Extends the parent property for older, Qt4 based interfaces.

        The parent ``QtImporter.base`` seems to only be used
        exclusively when ``interface_version_requested`` was Qt5.

        To make it useful for older Qt4 interfaces, the following
        common mappings are used instead for Qt4 as inspired by
        ``tank.platform.engine.Engine._define_qt_base`` :

        - "qt_core", QtCore module to use
        - "qt_gui", QtGui module to use
        - "wrapper", Qt wrapper root module, e.g. PySide
        - "dialog_base", base class for Tank's dialog factory.

        Returns:
            dict[str]: Mapping of Qt module, class and bindings names.
        """
        base = {"qt_core": None, "qt_gui": None, "dialog_base": None}

        if self._interface_version_requested == self.QT5:
            base = super(QtPyImporter, self).base

        elif self._interface_version_requested == self.QT4:
            base = {
                "qt_core": self.QtCore,
                "qt_gui": self.QtGui,
                "dialog_base": getattr(self.QtGui, 'QDialog', None),
                "wrapper": self.binding,
            }

        return base
