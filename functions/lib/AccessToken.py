# use requests? 
# aws lib to access SM

#import boto3
#import base64
#from botocore.exceptions import ClientError


class AccessToken:
    
    def __init__(self) -> None:
        pass
    
    def get_access_token(self, useLocal=True) -> str:
        # get secrets: client_secret, refresh_token, access_token
        # get config: client_id, authz url, secret_name, region
        None
    
    def _get_stored_access_token(self) -> str:
        None
    
    def _set_stored_access_token(self, token) -> bool:
        None 
        
    def _get_secrets(self) -> dict:
        None
    
    """ 
        Get an access token from Strava API
    """
    def _request_access_token(self) -> str:
        None