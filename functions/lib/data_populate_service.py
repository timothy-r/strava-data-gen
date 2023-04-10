from functions.lib.strava_service import StravaService
from functions.lib.data_store_service import DataStoreService

"""
    Get data from Strava & update the local data set
"""
class DataPopulateService:
    
    """
    
    """
    def __init__(
        self, 
        logger, 
        strava_service: StravaService, 
        data_store_service: DataStoreService
    ) -> None:
        
        self._logger = logger
        self._strava_service = strava_service
        self._data_store_service = data_store_service
        
    """
        add a single new activity
    """
    def add_activity(self, id):
        
        activity = self._strava_service.get_activity(id)
        
        self._logger.info("Number of retrieved activities: {}".format(len(activity)))
        
        new_activities = self._data_store_service.add_new_activities(activities=activity)
        
        self._logger.info("Number of new activities: {}".format(new_activities))
        
        return new_activities
    
    """
        use 0 to indicate all activities
        get activities
        store the new activities in data store
    """
    def update(self, after:int):
        
        activities = self._strava_service.get_activities(after=after)
        
        self._logger.info("Number of retrieved activities: {}".format(len(activities)))
        
        new_activities = self._data_store_service.add_new_activities(activities=activities)
        
        self._logger.info("Number of new activities: {}".format(new_activities))
        
        return new_activities