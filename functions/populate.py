'use strict';

from lib.Container import get_container

"""
* Get all activities from Strava
* Add all activities to data store 

"""
def run(event, context):
    
    container = get_container()
    
    data_store_service = container.data_store_service
    
    # as part of set up ensure the bucket has been created
    data_store_service.ensure_bucket_exists()
    
    data_populate_service = container.data_store_service
    
    # get all data from 0 epoch time
    new_activities = data_populate_service.update(0)
    
    if new_activities > 0:
        pass
        # publish an event to indicate new activities