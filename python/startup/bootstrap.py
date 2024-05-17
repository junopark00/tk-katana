# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os


def _get_resource_paths(context):
    """
    Retrieve any resource paths for any installed apps. 

    Resources live in the "resources/Katana" directory relative the the app's
    root directory.

    :returns: List of paths.
    """
    from sgtk.platform import constants
    
    paths = []
    env_name = context.sgtk.execute_core_hook(
        constants.PICK_ENVIRONMENT_CORE_HOOK_NAME,
        context=context
    )
    env = context.sgtk.pipeline_configuration.get_environment(env_name, context)
    apps = env.get_apps("tk-katana")
    for app in apps:
        app_descriptor = env.get_app_descriptor("tk-katana", app)
        path = app_descriptor.get_path()
        resource_path = os.path.join(path, "resources", "Katana")
        if os.path.isdir(resource_path):
            paths.append(resource_path)
    return paths


def bootstrap(engine_name, context, app_path, app_args, extra_args):
    """
    Setup the environment for Katana
    """
    import sgtk

    # pull the path to "{engine}/resources/Katana"
    engine_path = sgtk.platform.get_engine_path(engine_name, context.sgtk, context)
    startup_paths = [os.path.join(engine_path, "resources", "Katana")]
    startup_paths.extend(_get_resource_paths(context))
    startup_path = os.pathsep.join(startup_paths)

    # add to the katana startup env
    sgtk.util.append_path_to_env_var("KATANA_RESOURCES", startup_path)
    return (app_path, app_args)
