'use strict';

from dependency_injector.wiring import Provide, inject
import logging
import os 

from lib.Container import getContainer


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


"""
* Get all activities
* Add all activities to DDB table

"""
def run(event, context):
    
    container = getContainer()
    
    strava_service = container.strava_service()
    
    # use 0 to indicate all activities
    activities = strava_service.getActivities(0)
    logger.info("Number of activities: {}".format(len(activities)))