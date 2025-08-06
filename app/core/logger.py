import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("VitalSync")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)

# File handler with rotation
file_handler = RotatingFileHandler("vitalsync.log", maxBytes=10485760, backupCount=5)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)