from ..celeryapp import app
from ..graphProcessing import GraphProcessing
from ..api.logic.product import ProductLogic
from ..api.logic.assortment import AssortmentLogic
from ..api.logic.vendor import VendorLogic
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta

logger = get_task_logger(__name__)


@app.task(name="task_integration_store")
def task_integration_store():
    try:
        integrationProcessing = GraphProcessing()
        integrationProcessing.create_graph()
        logger.info("Create graph")
    except Exception as ex:
        logger.info("Error: " + ex.args[0])
        pass

@app.task(name='task_product')
def task_product():
    try:
        product_logic = ProductLogic()
        product_logic.process_product()
        logger.info("The products was loaded")
    except Exception as e:
        logger.info("Error: ", e.args[0])
        pass

@app.task(name='task_assort')
def task_assort():
    try:
        assort_logic = AssortmentLogic()
        assort_logic.process_assortment()
        logger.info("The products was loaded")
    except Exception as e:
        logger.info("Error: ", e.args[0])
        pass

@app.task(name='task_vendor')
def task_vendor():
    try:
        vendor_logic = VendorLogic()
        vendor_logic.process_vendor()
        logger.info("The products was loaded")
    except Exception as e:
        logger.info("Error: ", e.args[0])
        pass