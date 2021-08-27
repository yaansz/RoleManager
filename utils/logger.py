import logging
import os

def init_log():
    # Initializing the logger
    logPath = os.path.dirname(os.path.abspath(__file__)) + "/../log/run.log"
    
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        handlers=[
            logging.FileHandler(logPath),
            logging.StreamHandler()
        ]
    )

    