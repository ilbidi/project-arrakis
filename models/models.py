# Modelli per gestione tabelle
#
# Alcune note:
# Per db quali mysql e' necessario definire un lunghezza sui campi stringa
# Per db quali oracle il campo primary key deve essere gestito quale sequence

import sqlalchemy
import json

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence

Base = declarative_base()

# Classe User per gestione utenti
class User(Base):
    # Table name
    __tablename__ = 'user'
    # Fields
    id = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    name = Column(String(100))
    fullname = Column(String(100))
    password = Column(String(100))

    # Show content
    def __repr__(self):
        return '<User(''name''=%s, ''fullname''=%s, ''password''=%s)>' % (self.name, self.fullname, self.password)


    # Check equals
    def __eq__(self, other):
        return isinstance(other, User) and other.id == self.id

# Classe device type
#     tipo di dispositivo che esegue la comunicazione, ad esempio
#     arduino
class DeviceType(Base):
    # Table name
    __tablename__ = 'device_type'
    # Fields
    id = Column(Integer, Sequence('device_type_id_seq'), primary_key = True)
    code = Column(String(100))
    description = Column(String(100))

    # Show content
    def __repr__(self):
        return '<DeviceType(''code''=%s, ''description''=%s)>' % \
            (self.code, self.description)

    # Check equals
    def __eq__(self, other):
        return isinstance(other, DeviceType) and other.id == self.id

# Classe sensor type
#     Tipo di sensore che trasmette i dati
#     ad esempio HumiditySensor
class SensorType(Base):
    # Table name
    __tablename__ = 'sensor_type'
    # Fields
    id = Column(Integer, Sequence('sensor_type_id_seq'), primary_key = True)
    code = Column(String(100))
    description = Column(String(100))

    # Show content
    def __repr__(self):
        return '<SensorType(''code''=%s, ''description''=%s)>' % \
            (self.code, self.description)

    # Check equals
    def __eq__(self, other):
        return isinstance(other, SensorType) and other.id == self.id


# Classe device
#     Nome univoco di un dispositivo
class Device(Base):
    # Table name
    __tablename__ = 'device'
    # Fields
    id = Column(Integer, Sequence('device_id_seq'), primary_key = True)
    code = Column(String(100))
    description = Column(String(100))
    # Device type (many to one)
    device_type_id = Column(Integer, ForeignKey('device_type.id'))
    deviceType = relationship("DeviceType")

    # Sensors
    sensors = relationship("Sensor")

    # Show content
    def __repr__(self):
        return '<Device(''code''=%s, ''description''=%s, ''device type''=%s, ''sensors''=%s)>' % \
            (self.code, self.description, self.deviceType, self.sensors)

    # Check equals
    def __eq__(self, other):
        return isinstance(other, Device) and other.id == self.id

# Classe sensor
#     Sensore
class Sensor(Base):
    # Table name
    __tablename__ = 'sensor'
    # Fields
    id = Column(Integer, Sequence('sensor_id_seq'), primary_key = True)
    code = Column(String(100))
    description = Column(String(100))

    # Sensor type (many to one)
    sensor_type_id = Column(Integer, ForeignKey('sensor_type.id'))
    sensorType = relationship("SensorType")

    # Relation with device
    device_id = Column(Integer, ForeignKey('device.id'))

    # Show content
    def __repr__(self):
        return '<Sensor(''code''=%s, ''description''=%s, ''sensor type''=%s)>' % \
            (self.code, self.description, self.sensorType)

    # Check equals
    def __eq__(self, other):
        return isinstance(other, Sensor) and other.id == self.id

# Classe data
#    Dati ricevuti dai sensori dei dispositivi
class DeviceData(Base):
    # Table name
    __tablename__ = 'device_data'
    # Fields
    id = Column(Integer, Sequence('device_data_id_seq'), primary_key = True)

    # timestamp
    datetimeRead = Column(DateTime)

    # Device (many to one)
    device_id = Column(Integer, ForeignKey('device.id'))
    device = relationship("Device")
    # Sensor (many to one)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship("Sensor")

    # Data read from a device
    value = Column(Float)

    # Show content
    def __repr__(self):
        return '<DeviceData(''device''=%s, ''Sensor''=%s, ''value''=%f ''DateTimeRead''=%s' % \
            (self.device,\
             self.sensor,\
             self.value, \
             self.datetimeRead.strftime('%Y-%m-%d %H:%M:%S' ) \
             if self.datetimeRead is not None else '0000-00-00 00:00:00')

    # Check equals
    def __eq__(self, other):
        return isinstance(other, DeviceData) and other.id == self.id
