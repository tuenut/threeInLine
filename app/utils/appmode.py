import logging

logger = logging.getLogger(__name__)

from app.mainprocess import App


def main_mode():
    logger.debug("Start in main mode.")

    try:
        App().run()
    except Exception as exception:
        logger.exception("Some exception on `App().run()`.")

        exit(1)
