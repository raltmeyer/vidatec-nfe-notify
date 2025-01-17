#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

import logging

class LoggerConfig:
    @staticmethod
    def configure_logging():
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging has started.")
