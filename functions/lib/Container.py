from dependency_injector import containers, providers

import boto3
import logging

# import requests

from .AccessTokenService import AccessTokenService
from .StravaService import StravaService
from .DDBService import DDBService

"""
    DI container for the application
"""
class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    
    # inject into AccessToken 
    sm_client = providers.Singleton(
        boto3.client,
        service_name="secretsmanager"
    )
    
    ddb_client = providers.Singleton(
        boto3.client,
        service_name="dynamodb"
    )
    
    logger_service = providers.Callable(
        logging.getLogger,
        __name__
    )
    
    # provide the requests object to clients
    # requests_service = providers.Object(
    #     requests
    # )
    
    ddb_service = providers.Factory(
        DDBService,
        logger=logger_service,
        ddb_client=ddb_client,
        table_name=config.ddb_table_name
    )
    
    access_token_service = providers.Factory(
        AccessTokenService,
        logger=logger_service,
        sm=sm_client,
        client_id=config.strava_client_id,
        secret_name=config.sm_secret_name,
        authz_url=config.strava_authz_url,
        access_token_name=config.sm_access_token_name
    )
    
    strava_service = providers.Factory(
        StravaService,
        logger=logger_service,
        access_token_service=access_token_service,
        activities_url=config.strava_activities_url
    )
    
def getContainer():
    
    container = Container()

    container.config.sm_secret_name.from_env("SM_SECRET_NAME", required=True)
    container.config.sm_access_token_name.from_env("SM_ACCESS_TOKEN_NAME", required=True)

    container.config.strava_client_id.from_env("STRAVA_CLIENT_ID", required=True)
    container.config.strava_authz_url.from_env("STRAVA_AUTHZ_URL", required=True)
    container.config.strava_activities_url.from_env("STRAVA_ACTIVITIES_URL", required=True)

    container.config.app_region.from_env("APP_REGION", required=True)

    container.config.ddb_table_name.from_env("DDB_TABLE_NAME", required=True)
    
    container.init_resources()
    
    return container