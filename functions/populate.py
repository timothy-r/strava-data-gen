from lib.Container import Container

"""
* Get all activities
* Add all activities to DDB table

"""
def run(event, context):
    
    strava_service = Container.strava_service
    
    # use 0 to indicate all activities
    activities = strava_service.getActivities(0)
    