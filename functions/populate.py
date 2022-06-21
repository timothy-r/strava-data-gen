'use strict';

from lib.Container import get_container

"""
* Get all activities
* Add all activities to DDB table

"""
def run(event, context):
    
    container = get_container()
    
    strava_service = container.strava_service()
    
    logger = container.logger_service()
    
    # use 0 to indicate all activities
    activities = strava_service.get_activities(after=0)
    
    logger.info("Number of retrieved activities: {}".format(len(activities)))
    
    # store the new activities in data store
    data_store = container.data_store_service()
    
    new_activities = data_store.add_new_activities(activities=activities)
    
    logger.info("Number of new activities: {}".format(new_activities))
    
    if new_activities > 0:
        pass
        # publish an event to indicate new activities