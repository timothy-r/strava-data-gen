import requests

from .AppExceptions import RequestError
from .AccessTokenService import AccessTokenService

"""
    Encapsulates all interactions with Strava APIs
    Handles authorisation internally
"""

class StravaService:
    
    """"
        initialise service with dependencies
    """
    def __init__(self, logger, access_token_service: AccessTokenService, activities_url:str) -> None:
        self._access_token_service = access_token_service
        self._logger = logger
        self._activities_url = activities_url

        return None

    def get_activities(self, after:int) -> list:
        """
            get activities from Strava - if authZ fails then get a new access token & try again
        """
        try:
            # get access token (use local one if possible)
            token = self._access_token_service.get_access_token(True)
            activities = self._get_strava_data(token, after=after)
            # test if request failed
            
        except RequestError as error:
            self._logger.error("Request to get activities failed {}".format(error))
        
        try:
            # get new access token & try again
            token = self._access_token_service.get_access_token(False)
            activities = self._get_strava_data(token, after=after)
            
        except RequestError as error:
            self._logger.error("Second request to get activities failed {}".format(error))
            return None 
        
        return activities

    def _get_strava_data(self, token: str, after=0) -> dict:
        p = 1
        results = []
        while True:
            data = self._get_paged_strava_data(token, items_per_page=200, page=p, after=after)
            
            # self._logger.info("page {} has {} items".format(p, len(data)))
            p += 1
            if len(data) == 0:
                break
            results += data
            
        return results
    
    def _get_paged_strava_data(self, token: str, items_per_page:int=200, page:int=1, after=0) -> dict:
        header = {'Authorization': 'Bearer ' + token}
        param = {'per_page': items_per_page, 'page': page, 'after': after}
        
        response = requests.get(self._activities_url, headers=header, params=param)
        if response.status_code == 200:
            return response.json()
        else:
            raise RequestError("Request failed: {}".format(response.status_code))
    