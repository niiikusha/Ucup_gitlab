import traceback
from json import JSONDecodeError
from confluent_kafka import Consumer, KafkaException
from confluent_kafka.cimpl import TopicPartition, OFFSET_BEGINNING
from ..settings import Base
import threading
from ..api.logic.vendor import VendorLogic
from ..api.logic.product import ProductLogic
from ..api.logic.assortment import AssortmentLogic
from ..api.logic.category import CategoryLogic
from ..api.logic.invoice import InvoiceLogic
from ..api.logic.invoiceLines import InvoiceLinesLogic
# from ..api.logic.customer import CustomerLogic
import json
from ..settings import Dev
import logging

class TopicNames:
    VENDOR_TOPIC_NAME = Base.VENDOR_TOPIC_NAME
    PRODUCT_TOPIC_NAME = Base.PRODUCT_TOPIC_NAME
    # ASSORTMENT_TOPIC_NAME = Base.ASSORTMENT_TOPIC_NAME
    CATEGORY_TOPIC_NAME = Base.CATEGORY_TOPIC_NAME
    INVOICE_TOPIC_NAME = Base.INVOICE_TOPIC_NAME
    INVOICE_LINES_TOPIC_NAME = Base.INVOICE_LINES_TOPIC_NAME
    CUSTOMER_TOPIC_NAME = Base.CUSTOMER_TOPIC_NAME

class MessageProcessor:
    # customer_logic= CustomerLogic()
    vendor_logic = VendorLogic()
    product_logic = ProductLogic()
    # assortmanet_logic = AssortmentLogic()
    category_logic = CategoryLogic()
    invoice_logic = InvoiceLogic()
    invoice_lines_logic = InvoiceLinesLogic()

    def process_message(self, msg):
        """
            Обрабатывает сообщение
        """
        try:
            message = json.loads(msg.value().decode('utf-8'))
            print('msg', msg)
            print('message', message)
            # message = msg
            #     match msg.topic():
            # match msg.topic():
            #     case TopicNames.PRODUCT_TOPIC_NAME:
            #         self.product_logic.process_product(message)
            #     case TopicNames.ASSORTMENT_TOPIC_NAME:
            #         self.assortmanet_logic.process_assortment(message)
            #     case TopicNames.VENDOR_TOPIC_NAME:
            #         self.vendor_logic.process_vendor(message)
            if msg.topic() == TopicNames.PRODUCT_TOPIC_NAME:
                self.product_logic.process_product(message)
            elif msg.topic() == TopicNames.VENDOR_TOPIC_NAME:
                self.vendor_logic.process_vendor(message)
            elif msg.topic() == TopicNames.CATEGORY_TOPIC_NAME:
                self.category_logic.process_category(message)
            elif msg.topic() == TopicNames.INVOICE_TOPIC_NAME:
                self.invoice_logic.process_invoice(message)
            elif msg.topic() == TopicNames.INVOICE_LINES_TOPIC_NAME:
                self.invoice_lines_logic.process_invoice_lines(message)
            # elif msg.topic() == TopicNames.CUSTOMER_TOPIC_NAME:
            #     self.customer_logic.process_customer(message)
        except JSONDecodeError as e:
            traceback.print_exception(e, limit=0)
            pass

class Listener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.consumer = Consumer(Base.KAFKA_CONFIG)
        self.topics = [
            TopicNames.PRODUCT_TOPIC_NAME,  
            TopicNames.VENDOR_TOPIC_NAME, 
            TopicNames.CATEGORY_TOPIC_NAME,
            TopicNames.INVOICE_TOPIC_NAME,
            TopicNames.INVOICE_LINES_TOPIC_NAME,
            TopicNames.CUSTOMER_TOPIC_NAME
        ]

        self.processor = MessageProcessor()

    def run(self):
        """
            Запускает прослушивание топика и обработку сообщений
        """
        try:
            self.consumer.subscribe(self.topics)
            # for topic in self.topics:
            # слушает с конкретного топика, раздела и отступа
            # self.consumer.assign([TopicPartition(TopicNames.SUPPLIER_TOPIC_NAME, 0, OFFSET_BEGINNING)])
            while True:
                msg = self.consumer.poll(5.0)
                print('msg', msg)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    self.processor.process_message(msg)
        finally:
            self.consumer.close()

print(Dev.KAFKA_CONFIG)