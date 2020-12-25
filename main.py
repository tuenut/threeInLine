from app.utils.logger import configure_logger
from app.utils.appmode import main_mode
from app.utils.arguments import parse_arguments
from config import BASE_DIR

if __name__ == "__main__":
    logger = configure_logger()
    start_opts = parse_arguments()

    logger.debug(f"Start with args <{start_opts}>.")
    logger.debug(f"Base dir: <{BASE_DIR}>.")

    main_mode()
