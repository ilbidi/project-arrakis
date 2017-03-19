# Logging configuration
import sys
import logging

# A basic configuration that sends log to stout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, \
                    format='%(asctime)s %(name)-12s - %(levelname)-8s - %(message)s')

logger = logging.getLogger(__name__)

logger.debug('Log configuration loaded')
