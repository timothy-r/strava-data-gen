from lib.Container import get_container

import time

"""
* Get all data from the last 2 hours
* Add all activities to data store 

"""

def run(event, context):
    container = get_container()
    
    data_populate_service = container.data_store_service
    
    # get all data from the last 4 hours (testing)
    after = time.time() - (4 * 60 * 60)
    new_activities = data_populate_service.update(after)
    
    if new_activities > 0:
        pass
        # publish an event to indicate new activities
        