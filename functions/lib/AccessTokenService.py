import re
import requests
import json
import logging
# import boto3


from botocore.exceptions import ClientError

# from boto3 import ResourceNotFoundException

"""
    Provides OAuth access tokens
    Uses AWS SM to store secrets
        * Client secret - depends on this being set
        * Refresh token - depends on this being set
        * Access token - caches tokens in SM for reuse
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AccessTokenService:
    
    """
    """
    def __init__(self, sm, client_id:str, secret_name:str, authz_url:str, access_token_name:str) -> None:
        
        self._sm = sm
        self._client_id = client_id
        self._secret_name = secret_name
        self._authz_url = authz_url
        self._access_token_name = access_token_name
        return None
    
    def get_access_token(self, useLocal=True) -> str:
        # get secrets: client_secret, refresh_token, access_token
        if useLocal:
            token_data = self._get_secrets(self._access_token_name)()
            if token_data:
                logger.info("Using local token")
                return token_data['token']
        
        # otherwise get a new access token
        token = self._request_access_token()

        logger.info("Got new token")
        
        # only store the token if it exists, on failure store nothing
        if token:
            self._set_stored_access_token({'token': token})
            
        return token 
    
    # def _get_stored_access_token(self) -> str:
    #     # wrap in try catch block
    #     try:
    #         secret_data = self._sm.get_secret_value(SecretId=self._access_token_name)
    #         if 'SecretString' in secret_data:
    #             return json.loads(secret_data['SecretString'])
    #         else:
    #             return None
            
    #     except ClientError as err:
    #         # if the secret does't exist an exception is thrown
    #         logger.info("Failed to get access token from SM {}".format(err))
    #         return None
        
    def _set_stored_access_token(self, token_data:dict) -> bool:
        data = json.dumps(token_data)
        try:
            return self._sm.put_secret_value(SecretId=self._access_token_name, SecretString=data)
        except ClientError as err:
            logger.info("Failed to set access token in SM {}".format(err))
            # create a new secret
            return self._sm.create_secret(Name=self._access_token_name, SecretString=data)
        
    def _get_secrets(self, name:str) -> dict:
        # should be in JSON format, convert here
        try:
            secrets_data = self._sm.get_secret_value(SecretId=name)
            if 'SecretString' in secrets_data:
                return json.loads(secrets_data['SecretString'])
            else:
                return None
            
        except ClientError as err:
            logger.info("Failed to get secrets '{}' from SM - error: {}".format(name, err))
            return None 
    
    """ 
        Get an access token from Strava API
    """
    def _request_access_token(self) -> str:
        secrets = self._get_secrets(self._secret_name)
        
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
        
        return requests.post(
            self._authz_url,
            data=payload, 
            verify=False
        ).json()['access_token']
        