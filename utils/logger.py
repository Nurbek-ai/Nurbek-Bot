# utils/logger.py
import logging
import logging.config
import os

def setup_logging(default_path='logging.conf', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = logging.config.fileConfig(f) # Using fileConfig
        #logging.config.dictConfig(config) # For dictConfig you will need a dict config file
    else:
        logging.basicConfig(level=default_level)
        logging.warning("Logging configuration file not found: %s. Using default basic config.", path)