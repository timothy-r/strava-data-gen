'use strict';

"""
    Get data from Strava & update the local data set
"""
class DataPopulateService:
    
    def __init__(self, logger, strava_service, data_store_service) -> None:
        self._logger = logger
        self._strava_service = strava_service
        self.data_store_service = data_store_service

    def update(self, after):
        """
            after: epoch time to get activities after 
        """
        # use 0 to indicate all activities
        activities = self._strava_service.get_activities(after=after)
        
        self._logger.info("Number of retrieved activities: {}".format(len(activities)))
        
        # store the new activities in data store
        new_activities = self._data_store_service.add_new_activities(activities=activities)
        
        self._logger.info("Number of new activities: {}".format(new_activities))
        
        return new_activities