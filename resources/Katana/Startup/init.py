__author__ = "Juno Park"
__github__ = "https://github.com/junopark00/tk-katana"


"""
Setup the environment and menu to run Shotgun tools.
"""


def bootstrap():
    import logging
    import os
    import traceback

    # Check environment for engine and serialized context
    logger = logging.getLogger(__name__)
    error_msg = "Shotgun: Missing required environment variable: '%s'."

    engine_name = os.environ.get("SGTK_ENGINE")
    if engine_name is None:
        logger.error(error_msg, "SGTK_ENGINE")
        return
    
    serialized_context = os.environ.get("SGTK_CONTEXT")
    if serialized_context is None:
        logger.error(error_msg, "SGTK_CONTEXT")
        return

    # Import sgtk to deserialize and start engine
    try:
        import sgtk
    except ImportError:
        logger.error("Shotgun: Could not import sgtk! See sys.path below")
        list(map(logger.error, os.sys.path))
        logger.error("----end of sys.path ----")
        return

    logger = sgtk.platform.get_logger(__name__)
    try:
        context = sgtk.context.deserialize(serialized_context)
    except Exception:
        error_msg = "Shotgun: Could not create context from: '%s'\n%s"
        logger.error(error_msg, serialized_context, traceback.format_exc())
        return

    try:
        sgtk.platform.start_engine(engine_name, context.sgtk, context)
    except Exception:
        error_msg = "Shotgun: Could not start engine: '%s'\n%s"
        logger.error(error_msg, engine_name, traceback.format_exc())
        return

    # clean up temp env vars
    for var in ["SGTK_ENGINE", "SGTK_CONTEXT", "SGTK_FILE_TO_OPEN"]:
        if var in os.environ:
            logger.debug("Shotgun: Removing env var '%s'", var)
            del os.environ[var]


bootstrap()
del bootstrap
