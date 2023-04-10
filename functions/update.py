from lib.container import get_container


"""
Example request to confirm subscription

GET https://mycallbackurl.com?hub.verify_token=STRAVA&hub.challenge=15f7d1a91c1f40f8a748fd134752feb3&hub.mode=subscribe


Example request for a new activity
{
    "aspect_type": "update",
    "event_time": 1516126040,
    "object_id": 1360128428,
    "object_type": "activity",
    "owner_id": 134815,
    "subscription_id": 120475,
    "updates": {
        "title": "Messy"
    }
}

* 

* new activity
    * get the new activity id from the request
    * get the full activity from Strava APIs
    * update the local data store
    * publish event to Event Bridge to the reporter tasks
"""
def run(event, context):
    
    # determine type of request
    
    pass