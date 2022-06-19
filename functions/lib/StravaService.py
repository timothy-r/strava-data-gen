"""
* Encapsulates all interactions with Strava APIs
* Handles authorisation internally
"""
class StravaService:
    
    def __init__(self) -> None:
        pass
    
    def getAllActivities(self) -> list:
        return []
    
    def getActivities(self, since) -> list:
        
        # get access token (use local one if possible)
        # get activities from Strava - if authZ fails then get a new access token & try again
        
        return []