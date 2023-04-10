import requests

from functions.lib.secret_manager_service import SecretManagerService
from functions.lib.app_exceptions import RequestError


"""
    Provides OAuth access tokens
    Uses AWS SM to store secrets
        * Client secret - depends on this being set
        * Refresh token - depends on this being set
        * Access token - caches tokens in SM for reuse
"""

class AccessTokenService:
    
    """
    """
    def __init__(self, 
        logger,
        sm: SecretManagerService,
        requests: requests,
        client_id:str,
        secret_name:str,
        authz_url:str,
        access_token_name:str
    ) -> None:
        
        self._logger = logger
        self._sm = sm
        self._requests = requests
        
        # pass in a dict?
        self._client_id = client_id
        self._secret_name = secret_name
        self._authz_url = authz_url
        self._access_token_name = access_token_name
        
        return None
    
    def get_access_token(self, use_local=True) -> str:
        
        if use_local:
            token_data = self._sm.get_by_id(self._access_token_name)
            if token_data:
                self._logger.info("Using local token")
                return token_data['token']
        
        # get a new access token
        token = self._request_access_token()

        # only store the token if it exists, on failure store nothing
        if token:
            self._logger.info("Got new token")
            self._sm.put_by_id(self._access_token_name, {'token': token})
            return token 
        else:
            return None
        
    """ 
        Get an access token from Strava API
    """
    def _request_access_token(self) -> str:
        
        secrets = self._sm.get_by_id(self._secret_name)
        
        # test if secrets is set 
        if not secrets:
            # log error here or in above function?
            return None 
        
        payload = {
            'client_id': self._client_id,
            'client_secret': secrets['client_secret'],
            'refresh_token': secrets['refresh_token'],
            'grant_type': 'refresh_token',
            'f': 'json'
        }
        
        response = self._requests.post(
            self._authz_url,
            data=payload, 
            verify=True
        )
        
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise RequestError("Request failed: {}".format(response.status_code))