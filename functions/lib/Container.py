from dependency_injector import containers, providers
# from dependency_injector.wiring import Provide, inject
import boto3

from .AccessTokenService import AccessTokenService
from .StravaService import StravaService

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()
    
    # inject into AccessToken 
    sm_client = providers.Singleton(
        boto3.client,
        service_name="secretsmanager"
    )
    
    ddb_client = providers.Singleton(
        boto3.client,
        service_name=""
    )
    
    access_token_service = providers.Factory(
        AccessTokenService,
        sm=sm_client,
        client_id=config.sm_client_id,
        secret_name=config.sm_secret_name,
        authz_url=config.strava_authz_url,
        access_token_name=config.sm_access_token_name
    )
    
    strava_service = providers.Factory(
        StravaService,
        access_token_service,
        activities_url=config.strava_activities_url
    )
    

container = Container()
container.config.client_id.from_env("STRAVA_CLIENT_ID", required=True)
container.config.secret_name.from_env("SM_SECRET_NAME", required=True)
container.config.strava_authz_url.from_env("STRAVA_AUTHZ_URL", required=True)
container.config.sm_access_token_name.from_env("SM_ACCESS_TOKEN_NAME", required=True)
container.config.strava_activities_url.from_env("STRAVA_ACTIVITIES_URL", required=True)
container.config.app_region.from_env("APP_REGION", required=True)