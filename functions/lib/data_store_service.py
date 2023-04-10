import json
from datetime import datetime
from time import strftime
import botocore.exceptions

from lib.DateTimeEncoder import DateTimeEncoder

"""
    Encapsulates reading & writing & updating activity data
"""
class DataStoreService:
    
    def __init__(self, logger, s3_client, bucket:str, region:str) -> None:
        """
        """
        self._logger = logger
        self._s3_client = s3_client
        self._bucket = bucket
        self._region = region
        
        return None 
        
    def add_new_activities(self, activities:list)-> int:
        """
            add any new activities from the parameter to the current data set (ignore dupes)
            return number of added activities
        """
        # convert list to a dict with unique keys for each activity
        new_activities = {
            'activity:{}:athlete:{}'.format(a['id'], a['athlete']['id']) : a for a in activities
        }
        # get current data set
        stored_activities = self.get_all_activities()
        self._logger.info("Number of stored activities: {}".format(len(stored_activities)))
        
        added = 0
        # test if parameter activities exist in current set
        for k in new_activities.keys():
            if not k in stored_activities:
                stored_activities[k] = new_activities[k]
                added += 1
                self._logger.info("Adding new activity: {}".format(k))
        
        if added > 0:
            now = datetime.now()
            key = now.strftime("%Y/%m/%d-%H:%M:%S.json")
            self._logger.info("Adding new activities data set: {}".format(key))
            # store new activity data set in S3
            self._s3_client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=json.dumps(stored_activities, cls=DateTimeEncoder),
                ContentType='application/json'
            )
            
        # return number of additions
        return added 
    
    def get_all_activities(self) -> dict:
        """
            return the current activities data set
            using a date & time format for S3 objects, find the most recent object & return its contents
            object naming format is 'YYYY/MM/DD-HH:MM:SS.json'
        """
        
        object_key = self._get_current_object_key()
        if object_key == '':
            return {}
        
        self._logger.info("Current activities object: {}".format(object_key))
        
        # return the object's contents
        object_data = self._s3_client.get_object(
            Bucket = self._bucket,
            Key = object_key
        )
        
        return json.loads(object_data["Body"].read())
    
    def ensure_bucket_exists(self):
        try:
            response = self._s3_client.head_bucket(
                Bucket=self._bucket
            )
        except botocore.exceptions.ClientError as err:
            # create the bucket
            response = self._s3_client.create_bucket(
                Bucket=self._bucket,
                CreateBucketConfiguration={
                    'LocationConstraint': self._region
                }
            )
        
    
    def _get_current_object_key(self) -> str:
        """
        """
        top_level = self._get_object_list(prefix='')
        self._logger.info(top_level)
        
        if len(top_level) == 0:
            return ''
        
        if not 'CommonPrefixes' in top_level:
            return ''
        
        # extract the newest year
        years = [y['Prefix'] for y in top_level['CommonPrefixes']]
        years.sort(reverse=True)
        
        if len(years) == 0:
            return ''
        
        next_level = self._get_object_list(prefix=years[0])
        years_months = [ym['Prefix'] for ym in next_level['CommonPrefixes']]
        years_months.sort(reverse=True)
        
        lowest_level = self._get_object_list(prefix=years_months[0])
        
        objects = [ll['Key'] for ll in lowest_level['Contents']]
        objects.sort(reverse=True)
        
        return objects[0]
    
        
    def _get_object_list(self, prefix='') -> dict:
        """
        """
        return self._s3_client.list_objects_v2(
            Bucket=self._bucket,
            Prefix=prefix,
            Delimiter='/'
        )
        
