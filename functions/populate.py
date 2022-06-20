'use strict';

# from dependency_injector.wiring import Provide, inject

from lib.Container import getContainer


"""
* Get all activities
* Add all activities to DDB table

"""
def run(event, context):
    
    container = getContainer()
    
    strava_service = container.strava_service()
    
    logger = container.logger_service()
    
    # use 0 to indicate all activities
    activities = strava_service.getActivities(0)
    
    logger.info("Number of activities: {}".format(len(activities)))
    
    # store the activities in DDB
    
    # publish an event to indicate new activities