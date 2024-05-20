# import json
# from uuid import uuid4
# from confluent_kafka import Producer, KafkaException
# from ..settings import Base

# def delivery_report(err, msg):
#     """ Called once for each message produced to indicate delivery result.
#         Triggered by poll() or flush(). """
#     if err is not None:
#         print('Message delivery failed: {}'.format(err))
#     else:
#         print('Message delivered to topic {}, partition {}'.format(msg.topic(), msg.partition()))


# class Sender:
#     def __init__(self):
#         self.producer = Producer({'bootstrap.servers': Base.KAFKA_CONFIG.get('bootstrap.servers')})
#         self.topic = Base.KAFKA_SERVICE_TOPIC
#         self.partition = int(Base.KAFKA_SERVICE_PARTITION)

#     def send(self, data):
#         # Trigger any available delivery report callbacks from previous produce() calls
#         # self.producer.poll(5.0)
#         # Asynchronously produce a message. The delivery report callback will
#         # be triggered from the call to poll() above, or flush() below, when the
#         # message has been successfully delivered or failed permanently.
#         try:
#             self.producer.produce(topic=self.topic, key=str(uuid4()),
#                                   value=json.dumps(data, ensure_ascii=False).encode(),
#                                   callback=delivery_report, partition=self.partition)
#         except KafkaException as e:
#             print('KafkaException: {}'.format(e))
#         except BaseException as e:
#             print('BaseException: {}'.format(e))
#         except NotImplementedError as e:
#             print('NotImplementedError: {}'.format(e))
#         # Wait for any outstanding messages to be delivered and delivery report
#         # callbacks to be triggered.
#         self.producer.flush()