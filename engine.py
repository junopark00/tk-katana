# Copyright (c) 2024 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.


__author__ = "Juno Park"
__github__ = "https://github.com/junopark00/tk-katana"


import os
import traceback

import PySide2

from distutils.version import StrictVersion
import sgtk
from sgtk import TankError
from sgtk.util.pyside2_patcher import PySide2Patcher
import Katana


class KatanaEngine(sgtk.platform.Engine):
    """
    The engine class
    """
    def __init__(self, *args, **kwargs):
        # Detect if Katana is running in UI mode or not
        self._ui_enabled = bool(Katana.Configuration.get('KATANA_UI_MODE'))
        super(KatanaEngine, self).__init__(*args, **kwargs)

    @property
    def has_ui(self):
        """
        Detect and return if Katana is running with UI
        """
        return self._ui_enabled
        
    @property
    def host_info(self):
        """
        :returns: A dictionary with information about the application hosting this engine.
        """
        host_info = {"name": "Katana", "version": "unknown"}

        try:
            # Get Katana version information here
            host_info["version"] = Katana.version
        except:
            pass

        return host_info

    def pre_app_init(self):
        """
        Engine construction/setup done before any apps are initialized
        """
        self.log_debug("%s: Initializing..." % self)

        # Check Katana version compatibility
        MIN_VERSION = (3, 0, 0, 5)  # Minimum supported version
        MAX_VERSION = (6, 0, 1, 4)  # Maximum tested version

        katana_version = self.host_info["version"]

        if katana_version[0] < MIN_VERSION[0]:
            raise TankError(
                "This version of Katana %s.%s.%s is not supported. "
                "Please upgrade to at least Katana %s.%s.%s."
                % (
                    katana_version[0],
                    katana_version[1],
                    katana_version[3],
                    MIN_VERSION[0],
                    MIN_VERSION[1],
                    MIN_VERSION[3],
                )
            )
        elif katana_version[0] > MAX_VERSION[0] or (
            katana_version[0] == MAX_VERSION[0]
            and katana_version[1] > MAX_VERSION[1]
        ):
            msg = (
                "This version of Katana %s.%s.%s has not been tested with "
                "this version of the Toolkit. Please use caution and "
                "report any issues you encounter."
                % (
                    katana_version[0],
                    katana_version[1],
                    katana_version[3],
                )
            )

            if (
                self.has_ui
                and "SGTK_KATANA_VERSION_WARNING_SHOWN" not in os.environ
                and katana_version[0]
                >= self.get_setting("compatibility_dialog_min_version")
            ):
                # show the warning dialog the first time:
                Katana.UI4.Widgets.MsgBox(
                    "Toolkit Warning", msg, Katana.UI4.Widgets.MsgBox.Icon.Warning
                )
                os.environ["SGTK_KATANA_VERSION_WARNING_SHOWN"] = "1"
            self.log_warning(msg)

    def post_app_init(self):
        """
        Do any initialization after apps have been loaded
        """
        if self.has_ui:
            try:
                menu = self.add_katana_menu()
                if menu is None:
                    Katana.Callbacks.addCallback(Katana.Callbacks.Type.onStartupComplete, self.add_katana_menu)
            except AttributeError as e:
                self.log_error("Failed to add menu: %s" % e)
                Katana.Callbacks.addCallback(Katana.Callbacks.Type.onStartupComplete, self.add_katana_menu)
            except:
                traceback.print_exc()

    def add_katana_menu(self, **kwargs):
        """
        Add a menu item to the Katana menu
        """
        self.log_info("Creating Shotgun Menu.")
        menu_name = "Flow Production Tracking"
        tk_katana = self.import_module("tk_katana")
        self._menu_generator = tk_katana.MenuGenerator(self, menu_name)
        self._menu_generator.create_menu()

    def destroy_engine(self):
        """
        Called when the engine is being destroyed
        """
        self.log_debug("%s: Destroying..." % self)

        if self.has_ui:
            try:
                self._menu_generator.destroy_menu()
            except:
                traceback.print_exc()

    def _define_qt_base(self):
        """
        Patch PyQt to PySide
        """
        katana_version = os.environ['KATANA_RELEASE'].replace('v', '.')

        if StrictVersion(katana_version) >= StrictVersion('3.1'):
            qt_core_shim, qt_gui_shim = PySide2Patcher.patch(PySide2.QtCore, PySide2.QtGui, PySide2.QtWidgets, PySide2)
            return {"qt_core": qt_core_shim, "qt_gui": qt_gui_shim, "dialog_base": PySide2.QtWidgets.QDialog}
        
        else:
            #When the Katana's version is below 3.1, it uses PySide1.
            os.environ['QT_SIP_API_HINT'] = '1'
            vendor = self.import_module("vendor")
            utils = self.import_module("utils")
            return utils.QtPyImporter(vendor.Qt).base
        
################### LOG ####################
            
    def log_debug(self, msg):
        """
        Log a debug message
        :param msg:    The debug message to log
        """
        if not hasattr(self, "_debug_logging"):
            self._debug_logging = self.get_setting("debug_logging", False)
        if self._debug_logging:
            print("PTR Debug: %s" % msg)

    def log_info(self, msg):
        """
        Log some info
        :param msg:    The info message to log
        """
        print("SG Info: %s" % msg)

    def log_warning(self, msg):
        """
        Log a warning
        :param msg:    The warning message to log
        """
        msg = "PTR Warning: %s" % msg
        print(msg)

    def log_error(self, msg):
        """
        Log an error
        :param msg:    The error message to log
        """
        msg = "PTR Error: %s" % msg
        print(msg)