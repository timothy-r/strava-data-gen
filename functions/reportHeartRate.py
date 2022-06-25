'use strict';

from lib.Container import get_container

"""
* Get all activities from data store
* Generate a heart rate report graph image
"""
def run(event, context):
    
    container = get_container()
    
    logger = container.logger_service()
    
    # get the current activities data 
    data_store_service = container.data_store_service()
    all_activities = data_store_service.get_all_activities()
    
    reporter = container.heart_rate_reporter()
    # generate report graph image from activities
    image_file_path = reporter.generate(all_activities)
    
    # upload image to S3 bucket
    
    logger.info("Created new heart rate report: {}".format(image_file_path))
    