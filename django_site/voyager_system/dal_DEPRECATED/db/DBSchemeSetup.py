from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from voyager_system.domain.medical_center.Consumer import Consumer
from voyager_system.domain.medical_center.Dispenser import Dispenser
from voyager_system.domain.medical_center.Pod import *
from voyager_system.domain.medical_center.Dosing import *

import logging

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


Base = declarative_base()


# define schemes for DTOs - each DTO class describes the sql DB table of the Domain Layer object:
# attributes = columns, instances = rows
class ConsumerDTO(Base):
    __tablename__ = 'consumer'

    # Dto attributes
    id = Column(Integer, primary_key=True)
    pods = relationship("PodDTO")                   # 1-to-many relation: CONSUMER --holds references of--> PODs
    dosing_history = relationship("DosingDTO")      # 1-to-many relation: CONSUMER --holds references of--> DOSINGs
    dispensers = relationship("DispenserDTO")       # 1-to-many relation: CONSUMER --holds references of--> DISPENSERs
    # temp fields - @TODO: to be moved to UserDTO when exists -
    first_name = Column(String(50))
    last_name = Column(String(50))

    # static method. receives a (Domain layer) Consumer object and returns an instance of its DTO counterpart
    @staticmethod
    def from_consumer(consumer: Consumer):
        consumer_dto = ConsumerDTO()
        consumer_dto.id = consumer.id
        consumer_dto.pods = [PodDTO.from_pod(pod) for pod in consumer.pods]
        consumer_dto.dosing_history = [DosingDTO.from_dosing(dosing) for dosing in consumer.dosing_history]
        consumer_dto.dispensers = [DispenserDTO.from_dispenser(dispenser) for dispenser in consumer.dispensers]
        return consumer_dto

    # returns a Domain layer Consumer object for the referenced DTO instance
    def to_consumer(self):
        pods = [dto.to_pod() for dto in self.pods]
        dosing_history = [dto.to_dosing() for dto in self.dosing_history]
        dispensers = [dto.to_dispenser() for dto in self.dispensers]
        consumer = Consumer()
        consumer.pods = pods
        consumer.dosing_history = dosing_history
        consumer.dispensers = dispensers
        return consumer


class DispenserDTO(Base):
    __tablename__ = 'dispenser'

    # Dto attributes
    serial_number = Column(String(50), primary_key=True)
    registration_time = Column(DateTime(timezone=True), server_default=func.now())  # if Datetime not specified - sets it to the time of the SQL insert operation (based on the sql server's clock)
    consumer_id = Column(Integer, ForeignKey('consumer.id'))                        # many-to-1 relation: CONSUMER --holds references of--> DISPENSERs

    # static method. receives a (Domain layer) Dispenser object and returns an instance of its DTO counterpart
    @staticmethod
    def from_dispenser(dispenser: Dispenser):
        dispenser_dto = DispenserDTO()
        dispenser_dto.serial_number = dispenser.serial_number
        dispenser_dto.registration_time = dispenser.registration_time
        return dispenser_dto

    # returns a Domain layer Dispenser object for the referenced DTO instance
    def to_dispenser(self):
        dispenser = Dispenser(serial_number=self.serial_number, registration_time=self.registration_time)
        return dispenser


class PodDTO(Base):
    __tablename__ = 'pod'

    # Dto attributes
    id = Column(Integer, primary_key=True)
    remainder = Column(Float)
    type = relationship("PodTypeDTO")                           # 1-to-1 relation: POD --holds references of--> PODTYPEs
    type_id = Column(Integer, ForeignKey('podType.id'))         #   Domian Layer Pods only hold a 'type' reference field; 'type_id' only shows in the DB table
    consumer_id = Column(Integer, ForeignKey('consumer.id'))    # many-to-1 relation: CONSUMER --holds references of--> DISPENSERs

    # static method. receives a (Domain layer) Pod object and returns an instance of its DTO counterpart
    @staticmethod
    def from_pod(pod: Pod):
        pod_dto = PodDTO()
        pod_dto.id = pod.id
        pod_dto.remainder = pod.remainder
        pod_dto.type = PodTypeDTO.from_podType(pod.type)
        # pod_dto.type.from_podType(pod.type)
        return pod_dto

    # returns a Domain layer Pod object for the referenced DTO instance
    def to_pod(self):
        pod = Pod(pod_id=self.id, pod_type=self.type.to_podType())
        return pod


class PodTypeDTO(Base):
    __tablename__ = 'podType'

    # Dto attributes
    id = Column(Integer, primary_key=True)
    capacity = Column(Float)
    description = Column(String(500))

    # static method. receives a (Domain layer) PodType object and returns an instance of its DTO counterpart
    @staticmethod
    def from_podType(pod_type: PodType):
        pod_type_dto = PodTypeDTO()
        pod_type_dto.id = pod_type.type_id
        pod_type_dto.capacity = pod_type.capacity
        pod_type_dto.description = pod_type.description
        return pod_type_dto

    # returns a Domain layer PodType object for the referenced DTO instance
    def to_podType(self):
        podType = PodType(type_id=self.id,capacity=self.capacity, description=self.description)
        return podType


class DosingDTO(Base):
    __tablename__ = 'dosing'

    # Dto attributes
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    location = Column(String(50))
    time = Column(DateTime(timezone=True), server_default=func.now())   # if Datetime not specified - sets it to the time of the SQL insert operation (based on the sql server's clock)
    pod_id = Column(Integer, ForeignKey('pod.id'))                      # holds the pod_id of the Pod used in dose
    feedback = relationship("FeedbackDTO")                              # 1-to-1 relation: POD --holds references of--> PODTYPEs
    feedback_id = Column(Integer, ForeignKey('feedback.id'))            #   Domian Layer Dosings only hold a 'feedback' reference field; 'feedback_id' only shows in the DB table
    consumer_id = Column(Integer, ForeignKey('consumer.id'))            # many-to-1 relation: CONSUMER --holds references of--> DOSINGs

    # static method. receives a (Domain layer) Dosing object and returns an instance of its DTO counterpart
    @staticmethod
    def from_dosing(dosing: Dosing):
        dosing_dto = DosingDTO()
        dosing_dto.id = dosing.id
        dosing_dto.amount = dosing.amount
        dosing_dto.feedback = FeedbackDTO.from_feedback(dosing.feedback)
        return dosing_dto

    # returns a Domain layer Dosing object for the referenced DTO instance
    def to_dosing(self):
        feedback = self.feedback.to_feedback()
        dosing = Dosing(dosing_id=self.id, pod_id=self.pod_id,amount=self.amount,
                        time= self.time,location=self.location)
        dosing.feedback = feedback
        return dosing


class FeedbackDTO(Base):
    __tablename__ = 'feedback'

    # Dto attributes
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    description = Column(String(500))
    time = Column(DateTime(timezone=True), server_default=func.now())   # if Datetime not specified - sets it to the time of the SQL insert operation (based on the sql server's clock)

    # static method. receives a (Domain layer) Feedback object and returns an instance of its DTO counterpart
    @staticmethod
    def from_feedback(feedback: Feedback):
        feedback_dto = FeedbackDTO()
        feedback_dto.id = feedback.id
        feedback_dto.rating = feedback.rating
        feedback_dto.description = feedback.description
        feedback_dto.time = feedback.time
        return feedback_dto

    # returns a Domain layer Feedback object for the referenced DTO instance
    def to_feedback(self):
        feedback = Feedback(id=self.id, rating=self.rating, description=self.description, time=self.time)
        return feedback




def test_db(engine):
    # preping data for tests
    pod_type_1 = PodTypeDTO()
    pod_type_1.id = 111
    pod_type_1.capacity = 100
    pod_type_1.description = "makes you feel ok"

    pod1 = PodDTO()
    pod1.pod_id = 10
    pod1.type = pod_type_1

    feedback1 = FeedbackDTO()
    feedback1.description = "ok, i guess"
    feedback1.rating = 6.3
    dosing1 = DosingDTO()
    dosing1.amount = 40.5
    dosing1.pod_id = 1
    dosing1.feedback = feedback1

    dispenser1 = DispenserDTO()
    dispenser1.serial_number = "AAAAAA_1"

    consumer1 = ConsumerDTO()
    consumer1.pods.append(pod1)
    consumer1.dispensers.append(dispenser1)
    consumer1.dosing_history.append(dosing1)

    # adding data to db
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.add(consumer1)
    # session.add(feedback1)
    session.commit()

    # dispenser2 = session.query(DispenserDTO).filter(DispenserDTO.serial_number == "AAAAAA_1").one()
    # real_dispenser1 = dispenser2.to_dispenser()
    # dispenser3 = DispenserDTO()
    # dispenser3.from_dispenser(real_dispenser1)
    # dispenser3.serial_number = "AAAAAA_2"
    # session.add(dispenser3)
    # session.commit()

    dto_consumer2 = session.query(ConsumerDTO).filter(ConsumerDTO.id == consumer1.id).one()
    real_consumer3 = dto_consumer2.to_consumer()
    dto_consumer4 = ConsumerDTO.from_consumer(real_consumer3)
    dto_consumer4.id = 5
    for pod in dto_consumer4.pods:
        pod.id += 100
        pod.type.id += 100
    for dosing in dto_consumer4.dosing_history:
        dosing.id += 100
        dosing.feedback.id += 100

    for disp in dto_consumer4.dispensers:
        disp.serial_number += '100'
    session.add(dto_consumer4)
    session.commit()
    print(dto_consumer4)


def setup_DB(engine):
    Base.metadata.drop_all(engine)      # drop all schemes in current DB
    Base.metadata.create_all(engine)    # create all schemes described above in current DB
    test_db(engine)

if __name__ == "__main__":
    engine = create_engine('sqlite:///medicalCenter.db')    # creates the specified db, if it does not exist
    setup_DB(engine)



