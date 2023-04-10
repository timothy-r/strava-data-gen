import json

from botocore.exceptions import ClientError

"""
    wrap access to SM 
"""
class SecretManagerService():

    SECRET_STRING = 'SecretString'
    
    """
    """
    def __init__(self, sm, logger) -> None:
        self._sm = sm
        self._logger = logger

    """
        return the data stored in SM for this id
    """
    def get_by_id(self, id:str) -> dict:
            # should be in JSON format, convert here
        try:
            secrets_data = self._sm.get_secret_value(SecretId = id)
            
            # print(secrets_data)
            
            if self.SECRET_STRING in secrets_data:
                return json.loads(secrets_data[self.SECRET_STRING])
            else:
                self._logger.error(
                    "{} not set for id: {}".format(self.SECRET_STRING, id)
                )
                return None
            
        except ClientError as err:
            self._logger.error("Failed to get secrets for id: {} from SM - error: {}".format(id, err))
            return None 
    
    """
        set a new secret with id
    """
    def put_by_id(self, id:str, token_data:dict) -> bool:
        
        data = json.dumps(token_data)
        
        try:
            return self._sm.put_secret_value(SecretId=id, SecretString=data)
        
        except ClientError as err:
            
            self._logger.error("Failed to set access token in SM {}".format(err))
            # create a new secret
            return self._sm.create_secret(Name=id, SecretString=data)