import requests
import json

class AccessTokenService:
    
    def __init__(self, sm, client_id:str, secret_name:str, authz_url:str, access_token_name:str) -> None:
        
        # secrets manager instance
        self._sm = sm
        
        # strava client id
        self._client_id = client_id
        
        # secret name for all other secrets (r/o)
        self._secret_name = secret_name
        
        # strava endpoint to get access tokens
        self._authz_url = authz_url
        
        # secret name for access token
        self._access_token_name = access_token_name
    
    def get_access_token(self, useLocal=True) -> str:
        # get secrets: client_secret, refresh_token, access_token
        if useLocal:
            token = self._get_stored_access_token()
            if token:
                return token
        
        # otherwise get a new access token
        token = self._request_access_token()

        # only store the token if it exists, on failure store nothing
        if token:
            self._set_stored_access_token(token)
            
        return token 
    
    def _get_stored_access_token(self) -> str:
        return self._sm.get_secret_value(SecretId=self._access_token_name)
        
    def _set_stored_access_token(self, token) -> bool:
        return self._sm.put_secret_value(SecretId=self._access_token_name, SecretString=token)
        
    def _get_secrets(self) -> dict:
        # should be in JSON format, convert here
        secrets = self._sm.get_secret_value(SecretId=self._secret_name)
        return json.loads(secrets)
    
    """ 
        Get an access token from Strava API
    """
    def _request_access_token(self) -> str:
        secrets = self._get_secrets()
        
        payload = {
            'client_id': self._client_id,
            'client_secret': secrets['client_secret'],
            'refresh_token': secrets['refresh_token'],
            'grant_type': 'refresh_token',
            'f': 'json'
        }
        
        return requests.post(
            self._authz_url,
            data=payload, 
            verify=False
        ).json()['access_token']
        