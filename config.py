import logging

# Create and configure logger
logging.basicConfig(filename="apparate.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)