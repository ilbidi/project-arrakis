# Main program. Per ora non fa nulla se non caricare il sistema di logging
import sys
import logconfig

# Get logger
logger = logconfig.logging.getLogger(__name__)

def main():
    logger.info('Main started')
    logger.info('Main ended')

if __name__=='__main__':
    main()
    
