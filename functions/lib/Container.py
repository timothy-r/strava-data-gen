from dependency_injector import containers, providers

import boto3
import logging
import requests

from functions.lib.data_populate_service import DataPopulateService

from functions.lib.access_token_service import AccessTokenService
from functions.lib.strava_service import StravaService
from functions.lib.data_store_service import DataStoreService
from functions.lib.secret_manager_service import SecretManagerService

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
    
    logger_service = providers.Callable(
        logging.getLogger,
        __name__
    )
    
    sm_service = providers.Factory(
        SecretManagerService,
        sm_client,
        logger_service
    )
    
    s3_client = providers.Singleton(
        boto3.client,
        service_name='s3'
    )
    
    # provide the requests object to clients
    # requests_service = providers.Object(
    #     requests
    # )
    
    data_store_service = providers.Factory(
        DataStoreService,
        logger=logger_service,
        s3_client=s3_client,
        bucket=config.data_store_bucket,
        region=config.app_region
    )
    
    access_token_service = providers.Singleton()(
        AccessTokenService,
        logger=logger_service,
        sm=sm_client,
        client_id=config.strava_client_id,
        secret_name=config.sm_secret_name,
        authz_url=config.strava_authz_url,
        access_token_name=config.sm_access_token_name
    )
    
    strava_service = providers.Singleton()(
        StravaService,
        logger=logger_service,
        access_token_service=access_token_service,
        activities_url=config.strava_activities_url
    )
    
    data_populate_service = providers.Factory(
        DataPopulateService,
        logger=logger_service,
        strava_service=strava_service,
        data_store_service=data_store_service
    )
    
def get_container():
    
    container = Container()

    container.config.sm_secret_name.from_env("SM_SECRET_NAME", required=True)
    container.config.sm_access_token_name.from_env("SM_ACCESS_TOKEN_NAME", required=True)

    container.config.strava_client_id.from_env("STRAVA_CLIENT_ID", required=True)
    container.config.strava_authz_url.from_env("STRAVA_AUTHZ_URL", required=True)
    container.config.strava_activities_url.from_env("STRAVA_ACTIVITIES_URL", required=True)

    container.config.app_region.from_env("APP_REGION", required=True)

    container.config.data_store_bucket.from_env("DATA_STORE_BUCKET", required=True)
    
    container.init_resources()
    
    container.logger_service().setLevel(logging.DEBUG)
    
    container.access_token_service().set_requests(requests=requests)
    
    container.strava_service().set_requests(requests=requests)
    
    return container