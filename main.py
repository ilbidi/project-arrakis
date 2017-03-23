# Main program. Per ora non fa nulla se non caricare il sistema di logging
import sys
import logconfig
import arrakis.arrakis
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, SensorType, Sensor, DeviceType, Device, DeviceData
from arrakis import arrakis

# Get logger
logger = logconfig.logging.getLogger(__name__)

# Configure nrf
from arrakis.nrf24 import NRF24
import time
from time import gmtime, strftime

# other configuration
from arrakis import arrakis

pipes = [[0xf0, 0xf0, 0xf0, 0xf0, 0xe1], [0xf0, 0xf0, 0xf0, 0xf0, 0xd2]]

radio = NRF24()
radio.begin(0, 0,25,18) #set gpio 25 as CE pin
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x4c)
radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(1)
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])

radio.startListening()
radio.stopListening()

radio.printDetails()
radio.startListening()


def main():
    # Configure database
    engine = create_engine('mysql://root:root@localhost/testsqlalchemy')
    arrakis.Session.configure(bind=engine)
    arrakis.session = arrakis.Session()
    Base.metadata.create_all(engine)    

    logger.info('Main started. Enter listening sycle')
    while True:
        logger.debug('Listening cycle')
        time.sleep(2)
        pipe = [0]
        while not radio.available(pipe, True):
            time.sleep(1000/1000000.0)
            #print 'radio not available'

        recv_buffer = []
        radio.read(recv_buffer)
        out = ''.join(chr(i) for i in recv_buffer)
        logger.debug(out)
        # write data to db
        arrakis.insDataRead(arrakis.dictInput(input=out))

    arrakis.session.rollback()
    arrakis.session.close()
    logger.info('Main ended')

if __name__=='__main__':
    main()
