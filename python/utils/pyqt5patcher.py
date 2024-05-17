"""PyQt5 to PySide 1 patcher, extending ``PySide2Patcher`` in ``sgtk.util``."""
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from sgtk.util.pyside2_patcher import PySide2Patcher

__all__ = ('PyQt5Patcher', 'PatchedBoundSignal')


class PatchedBoundSignal(object):
    """Wrap original PyQt BoundSignal signal instances.

    Attributes:
        original_signal (PyQt5.BoundSignal): Original, wrapped signal.
    """

    def __init__(self, original_signal):
        """Wrap the original signal like a burrito.

        Args:
            original_signal (PyQt5.BoundSignal): Signal to wrap.
        """
        self.original_signal = original_signal

    def __getitem__(self, item):
        """Get original signal if requesting empty tuple.

        Args:
            item (type or tuple): Specific signal type to fetch.

        Returns:
            PyQt5.BoundSignal: Signal for required signal type.
        """
        if item is tuple():
            return self.original_signal
        else:
            return self.original_signal[item]

    def __getattr__(self, attr):
        """Get attributes from original signal.

        Args:
            attr (str): Name of attribute to fetch.

        Returns:
            object: Attribute from original signal.
        """
        return getattr(self.original_signal, attr)


class PyQt5Patcher(PySide2Patcher):
    """Patch remaining PyQt5 binding after Qt.py for PySide 1.

    So yes, this patcher is used **specifically** after Qt.py patched
    most of PyQt5 bindings for PySide2.

    It patches any remaining (Py)Qt5 bindings for PySide 1 since that's what
    Shotgun still seems to mainly target as of May 2019.

    Originally developed for Katana 3.1 for use in ``tk-katana``:

    .. code-block:: text

        Katana 3.1 (PyQt5)
                |
                V
              Qt.py
              ^^^^^
                |
                | Converts PyQt5 for PySide2 compatibility
                V
         PySide2Patcher (parent class from sgtk.util)
         ^^^^^^^^^^^^^^
                |
                |  Converts PySide2 for PySide 1 compatibility
                V
           PyQt5Patcher (that's me!)
           ^^^^^^^^^^^^
                |
                |  Converts any remaining PyQt5 for PySide 1 compatibility
                V
           KatanaEngine._define_qt_base
           ^^^^^^^^^^^^
                |
                |  Engine then exposes Qt bindings publicly through...
                V
         sgtk.platform.qt
    """

    @classmethod
    def _patch_QAction(cls, QtGui):
        """PyQt5 doesn't take ``triggered[()]``, re-map to ``triggered``."""
        original_QAction = QtGui.QAction

        class QAction(original_QAction):
            """QAction with patched ``triggered`` (bound) signal."""

            def __init__(self, *args, **kwargs):
                """Extend original constructor to override triggered signal."""
                super(QAction, self).__init__(*args, **kwargs)
                self._original_triggered = self.triggered
                self.triggered = PatchedBoundSignal(self._original_triggered)

        QtGui.QAction = QAction

    @classmethod
    def _patch_QPyTextObject(cls, QtCore, QtGui):
        class QPyTextObject(QtCore.QObject, QtGui.QTextObjectInterface):
            """PyQt5 specific, create a backport QPyTextObject.

            See https://doc.bccnsoft.com/docs/PyQt5/pyqt4_differences.html?highlight=qpytextobject#qpytextobject.
            """
        QtGui.QPyTextObject = QPyTextObject

    @classmethod
    def _patch_QHeaderView(cls, QtGui):
        """
        Back port old method calls on the QHeaderView object.
        """
        original_QHeaderView = QtGui.QHeaderView

        class QHeaderView(original_QHeaderView):

            def setResizeMode(self, *args, **kwargs):
                return super(QHeaderView, self).setSectionResizeMode(*args, **kwargs)

            def resizeMode(self, *args, **kwargs):
                return super(QHeaderView, self).sectionResizeMode(*args, **kwargs)

            def isClickable(self, *args, **kwargs):
                return super(QHeaderView, self).sectionsClickable(*args, **kwargs)

            def isMovable(self, *args, **kwargs):
                return super(QHeaderView, self).sectionsMovable(*args, **kwargs)

            def setClickable(self, *args, **kwargs):
                return super(QHeaderView, self).setSectionsClickable(*args, **kwargs)

            def setMovable(self, *args, **kwargs):
                return super(QHeaderView, self).setSectionsMovable(*args, **kwargs)

        QtGui.QHeaderView = QHeaderView

    @classmethod
    def _patch_QTreeView(cls, QtCore, QtGui):
        """
        Use the patched `QHeaderView` as the header object otherwise it will use an
        unpatched version, which we don't want.
        """
        original_QTreeView = QtGui.QTreeView

        class QTreeView(original_QTreeView):

            def __init__(self, *args, **kwargs):
                super(QTreeView, self).__init__(*args, **kwargs)
                header = QtGui.QHeaderView(QtCore.Qt.Horizontal, parent=self)
                header.setSectionResizeMode(QtGui.QHeaderView.Stretch)
                self.setHeader(header)

        QtGui.QTreeView = QTreeView

    @classmethod
    def _patch_QTreeWidget(cls, QtCore, QtGui):
        """
        Use the patched `QHeaderView` as the header object otherwise it will use an
        unpatched version, which we don't want.
        """
        original_QTreeWidget = QtGui.QTreeWidget

        class QTreeWidget(original_QTreeWidget):

            def __init__(self, *args, **kwargs):
                super(QTreeWidget, self).__init__(*args, **kwargs)
                header = QtGui.QHeaderView(QtCore.Qt.Horizontal, parent=self)
                header.setSectionResizeMode(QtGui.QHeaderView.Stretch)
                self.setHeader(header)

        QtGui.QTreeWidget = QTreeWidget

    @classmethod
    def _patch_QTreeWidgetItemIterator(cls, QtGui):
        """
        Add the '__iter__' method to the `QTreeWidgetItemIterator`.
        """
        original_QTreeWidgetItemIterator = QtGui.QTreeWidgetItemIterator
        class QTreeWidgetItemIterator(original_QTreeWidgetItemIterator):

            def __iter__(self):
                value = self.value()
                while value:
                    yield self
                    self += 1
                    value = self.value()

        QtGui.QTreeWidgetItemIterator = QTreeWidgetItemIterator

    @classmethod
    def _patch_QtCore__version__(cls, QtCore):
        """PyQt does not have ``__version__``, get it from ``qVersion()``."""
        QtCore.__version__ = QtCore.qVersion()

    @classmethod
    def patch(cls, QtCore, QtGui, QtWidgets):
        """Patches QtCore, QtGui and QtWidgets

        Args:
            QtCore (module): The QtCore module to patch.
            QtGui (module): The QtGui module to patch.
            QtWidgets (module): The QtWidgets module to patch.
        """
        qt_core_shim, qt_gui_shim = PySide2Patcher.patch(
            QtCore, QtGui, QtWidgets, None,
        )

        cls._patch_QtCore__version__(qt_core_shim)
        cls._patch_QPyTextObject(qt_core_shim, qt_gui_shim)
        cls._patch_QAction(qt_gui_shim)
        cls._patch_QHeaderView(qt_gui_shim)
        cls._patch_QTreeView(qt_core_shim, qt_gui_shim)
        cls._patch_QTreeWidget(qt_core_shim, qt_gui_shim)
        cls._patch_QTreeWidgetItemIterator(qt_gui_shim)
        return qt_core_shim, qt_gui_shim
