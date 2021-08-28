import logging
import os

from colorlog import ColoredFormatter

def init_log():
    # Initializing the logger
    logPath = os.path.dirname(os.path.abspath(__file__)) + "/../log/run.log"
    logFormat = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    
    formatter = ColoredFormatter("%(log_color)s" + logFormat)
    
    # Terminal
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)

    logging.basicConfig(
        level=logging.DEBUG,
        format=logFormat,
        handlers=[
            logging.FileHandler(logPath),
            stream
        ]
    )

    