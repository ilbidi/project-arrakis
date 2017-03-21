# Funzioni di utilita' per project-arrakis
import sqlalchemy
import models
import datetime

from sqlalchemy.orm import sessionmaker
from models.models import Base, SensorType, Sensor, DeviceType, Device, DeviceData

# Base dati
Session = sessionmaker()
session = None

# Funzioni
def parseInput(input, delimiter='|'):
    """Parsing dell'input dalla lettura sensori"""
    return input.split(delimiter)

def dictInput(input, delimiter='|'):
    if( not input ):
        return None
    tokens = parseInput(input, delimiter)
    if( not tokens ):
        return None
    if( len(tokens) != 5):
        return None
    dataRead = dict()
    dataRead['device']=tokens[0]
    dataRead['deviceType']=tokens[1]
    dataRead['sensor']=tokens[2]
    dataRead['sensorType']=tokens[3]
    dataRead['value']=tokens[4]
    return dataRead

def insDataRead(dataRead):
    """Inserimento dei dati a Database
    vengono anche insiriti sensori e dispositivi
    nel caso non esistessero"""
    sensorType = session.query(SensorType).filter_by(code=dataRead['sensorType']).first()
    if( sensorType is None ):
        sensorType = SensorType(code=dataRead['sensorType'])
        session.add(sensorType)
    deviceType = session.query(DeviceType).filter_by(code=dataRead['deviceType']).first()
    if( deviceType is None ):
        deviceType = DeviceType(code=dataRead['deviceType'])
        session.add(deviceType)
    sensor = session.query(Sensor).filter_by(code=dataRead['sensor']).first()
    if( sensor is None ):
        sensor = Sensor(code=dataRead['sensor'], sensorType=sensorType)
        session.add(sensor)
    device = session.query(Device).filter_by(code=dataRead['device']).first()
    if( device is None ):
        device = Device(code=dataRead['device'], deviceType=deviceType)
        device.sensors.append(sensor)
    else:
        if( not sensor in device.sensors ):
            device.sensors.append(sensor)
    session.add(device)
    deviceData = DeviceData(device=device,\
                            sensor=sensor,\
                            value=dataRead['value'],\
                            datetimeRead=datetime.datetime.utcnow()\
                            )
    session.add(deviceData)
    # Commit data
    session.commit()
