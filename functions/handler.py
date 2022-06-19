import datetime
import logging
import numpy as np

from lib.AccessToken import AccessToken

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Your cron function " + name + " ran at " + str(current_time))
    token = AccessToken()
    logger.info("Access token {}".format(token))
    
    a = np.arange(15).reshape(3, 5)
 
    logger.info("Your numpy array:")
    logger.info(a)