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
import Katana
from Katana import QtGui, QtCore, QtWidgets, UI4

class ActionFactory(object):
    """
    Factory class that handles creation of Katana actions that wrap Toolkit command
    callbacks.
    """

    def __init__(self):
        """
        Construction
        """
        self.__action_id = 0
        self.__callbacks = {}

    ACTION_COMMANDS_ATTR = "_shotgun_menu_callbacks"

    def create_action(self, name, callback, menu=None):
        """
        Create a Katana action for the specified callback

        :param name:        The name of the action/Toolkit command
        :param callback:    The callback that should be run when the action is executed
        :param menu:        The menu that the action should be added to.  If None, the action will be added to the main menu.

        :returns:           A Katana Action that will execute the Toolkit callback
        """
        if not hasattr(Katana, ActionFactory.ACTION_COMMANDS_ATTR):
            setattr(Katana, ActionFactory.ACTION_COMMANDS_ATTR, {})

        action_id = self.__action_id
        self.__action_id += 1

        self.__callbacks[action_id] = callback
        if menu is None:
            menu = UI4.App.MainWindow.GetMainWindow().getMenuBar()
        action = menu.addAction(name)
        action.triggered.connect(lambda: self._execute_callback(action_id))
        return action

    def _execute_callback(self, action_id):
        """
        Execute the callback associated with the triggered action

        :param action_id:   The id of the action that was triggered
        """
        callback = self.__callbacks.get(action_id)
        if callback:
            callback()

    def clear(self):
        """
        Clear the list of Toolkit actions stored on the mari module
        """
        if hasattr(Katana, ActionFactory.ACTION_COMMANDS_ATTR):
            delattr(Katana, ActionFactory.ACTION_COMMANDS_ATTR)

class MenuGenerator(object):
    """
    A Katana specific menu generator.
    """

    def __init__(self, engine, menu_name):
        """
        Initializes a new menu generator.

        :param engine: The currently-running engine.
        :type engine: :class:`sgtk.platform.Engine`
        :param menu_name: The name of the menu to be created.
        """
        self._engine = engine
        self.menu_name = menu_name
        self.__action_factory = ActionFactory()
        self.root_menu = self.setup_root_menu()

    def create_menu(self):
        """
        Create the Shotgun menu
        """
        shotgun_menu = self.__build_shotgun_menu()
        context_menu = self.__build_context_menu(shotgun_menu)
        self.root_menu.addSeparator()

        menu_items = []
        for cmd_name, cmd_details in self._engine.commands.items():
            menu_items.append(AppCommand(cmd_name, cmd_details, self.__action_factory, self.root_menu))

        commands_by_app = {}
        for cmd in menu_items:
            if cmd.get_type() == "context_menu":
                cmd.add_to_menu(context_menu)
            else:
                app_name = cmd.get_app_name()
                if app_name is None:
                    app_name = "Other Items"
                if not app_name in commands_by_app:
                    commands_by_app[app_name] = []
                commands_by_app[app_name].append(cmd)

        self.__build_app_menu(commands_by_app, shotgun_menu)

    def destroy_menu(self):
        """
        Destroys the Shotgun menu.
        """
        if self.root_menu is not None:
            self.__action_factory.clear()

    def setup_root_menu(self):
        """
        Attempts to find an existing menu of the specified title.

        If it can't be found, it creates one.
        """
        main_menu = UI4.App.MainWindow.GetMainWindow().getMenuBar()

        # Attempt to find existing menu
        for menu in main_menu.children():
            is_menu = isinstance(menu, QtWidgets.QMenu)
            if is_menu and menu.title() == self.menu_name:
                return menu

        # Otherwise, create a new menu
        menu = QtWidgets.QMenu(self.menu_name, main_menu)
        return main_menu

    def __build_shotgun_menu(self):
        """
        Build and return the Shotgun menu in Katana
        """
        return self.root_menu.addMenu(self.menu_name)

    def __build_context_menu(self, shotgun_menu):
        """
        Adds a context menu which displays the current context.
        """
        ctx_menu = shotgun_menu.addMenu("Current Context")
        
        ctx = self._engine.context
        action = ctx_menu.addAction(str(ctx))
        ctx_menu.addAction(action)
        ctx_menu.addSeparator()

        action = ctx_menu.addAction("Jump to File System")
        action.triggered.connect(self._jump_to_fs)

        action = ctx_menu.addAction("Jump to Flow Production Tracking")
        action.triggered.connect(self._jump_to_sg)
        ctx_menu.addAction(action)
        return ctx_menu

    def _jump_to_sg(self):
        """
        Opens current context's Shotgun URL.
        """
        url = self._engine.context.shotgun_url
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def _jump_to_fs(self):
        """
        Opens current context's folders on the file system.
        """
        paths = self._engine.context.filesystem_locations
        for disk_location in paths:
            if os.sys.platform.startswith("linux"):
                os.system("xdg-open '%s'" % disk_location)
            elif os.sys.platform.startswith("win"):
                os.startfile(disk_location)
            elif os.sys.platform.startswith("darwin"):
                os.system("open '%s'" % disk_location)

    def __build_app_menu(self, commands_by_app, shotgun_menu):
        """
        Build the main app menu for all app commands

        :param shotgun_menu: The full path to the shotgun menu
        """
        for app_name, commands in sorted(commands_by_app.items()):
            if len(commands_by_app[app_name]) > 1:
                app_menu = shotgun_menu.addMenu(app_name)
                for cmd in commands:
                    cmd.add_to_menu(app_menu)
            else:
                cmd = commands_by_app[app_name][0]
                cmd.add_to_menu(shotgun_menu)


class AppCommand(object):
    """
    Wrapper for a command registered by an app
    """

    def __init__(self, name, command_dict, action_factory, menu):
        """
        Construction

        :param name:            The name of the command
        :param command_dict:    A dictionary of parameters specified for the command
        :param action_factory:  An instance of the ActionFactory class used to create
                                Mari actions for command callbacks
        """
        self.name = name
        self.properties = command_dict["properties"]
        self.callback = command_dict["callback"]
        self.favourite = False
        self.__action_factory = action_factory
        self.__action = None
        self.menu = menu

    def get_app_name(self):
        """
        Find the display name for the app this command was loaded from

        :returns:    The app display name if known
        """
        if "app" not in self.properties:
            return None
        return self.properties["app"].display_name

    def get_app_instance_name(self):
        """
        Find the instance name for the app this command was loaded from

        :returns:    The app instance name if known
        """
        if "app" not in self.properties:
            return None

        app_instance = self.properties["app"]
        engine = app_instance.engine

        for app_instance_name, app_instance_obj in engine.apps.items():
            if app_instance_obj == app_instance:
                # found our app!
                return app_instance_name

        return None

    def get_type(self):
        """
        Find the type of this command

        :returns:    The type of the command or 'default' if not found
        """
        return self.properties.get("type", "default")

    def add_to_menu(self, menu):
        """
        Add this command to the menu

        :param menu:    The menu this command should be added to.
        """
        # create a new action for the command if needed:
        if not self.__action:
            self.__action = self.__action_factory.create_action(
                self.name, self.callback, menu
            )

        if self.__action:
            # add the action to the menu:
            menu.addAction(self.__action)