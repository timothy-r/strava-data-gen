import random
import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
import json

from lib.DataStoreService import DataStoreService

class DataStoreServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        
        logger_mock = Mock()
        logger_mock.info = MagicMock()
        logger_mock.error = MagicMock()
        
        self._test_bucket_name = 'TestBucket'
        self._s3_client_mock = Mock()
           
        self._data_store = DataStoreService(
            logger=logger_mock, 
            s3_client=self._s3_client_mock,
            bucket=self._test_bucket_name
            )
        
        return super().setUp()
    
    def test_get_all_activities_when_none_stored(self):
        
        # set up mocked data
        activity_data = get_list_objects_v2_empty_response(self._test_bucket_name)
        
        self._s3_client_mock.list_objects_v2 = MagicMock(activity_data)
        
        # exec code
        all_activities = self._data_store.get_all_activities()
        
        # assert expected results
        assert(len(all_activities) == 0)

    def test_get_all_activities(self):
        self._s3_client_mock.list_objects_v2 = MagicMock(side_effect=get_all_activities_mock)
        
        existing_activity_data = get_activity_data([99887, 333112])
        mock_get_object = MagicMock()
        mock_get_object.return_value = json.dumps(existing_activity_data)
        self._s3_client_mock.get_object = mock_get_object
        
        all_activities = self._data_store.get_all_activities()
        assert(len(all_activities) == 2)

    def test_add_new_activities_no_new(self):
        """
            test that the data store ignores activities that it already contains
        """
        ids = [23456, 12778]
        self._s3_client_mock.list_objects_v2 = MagicMock(side_effect=get_all_activities_mock)
        
        existing_activity_data = get_activity_data(ids)
        mock_get_object = MagicMock()
        mock_get_object.return_value = json.dumps(existing_activity_data)
        self._s3_client_mock.get_object = mock_get_object
        
        # data format returned by Strava APIs is a list of dicts
        # data store service generates unique ids for each activity
        new_activities = get_activity_data(ids).values()
        
        added_activities = self._data_store.add_new_activities(new_activities)
        assert (0 == added_activities)
        
    def test_add_new_activities(self):
        ids = [23456, 12778]
        self._s3_client_mock.list_objects_v2 = MagicMock(side_effect=get_all_activities_mock)
        
        existing_activity_data = get_activity_data(ids)
        mock_get_object = MagicMock()
        mock_get_object.return_value = json.dumps(existing_activity_data)
        self._s3_client_mock.get_object = mock_get_object
        
        mock_put_object = MagicMock()
        self._s3_client_mock.put_object = mock_put_object
        
        # data format returned by Strava APIs is a list of dicts
        # data store service generates unique ids for each activity
        
        # only 2 ids are new
        new_activities = get_activity_data([333, 777, ids[1]]).values()
        
        added_activities = self._data_store.add_new_activities(new_activities)
        assert (2 == added_activities)
        
        # print(mock_put_object.mock_calls)
        calls = mock_put_object.mock_calls
        assert (1 == len(calls))
        # assert (self._test_bucket_name == calls[0]['Bucket'])
    
    
def get_list_objects_v2_empty_response(bucket_name):
        """
            an empty bucket response
        """
        return {
            'IsTruncated': False,
            'Contents': [],
            'Name': bucket_name,
            'Prefix': '',
            'Delimiter': '',
            'MaxKeys': 0,
            'CommonPrefixes': [
            ],
            'EncodingType': 'url',
            'KeyCount': 0,
            'ContinuationToken': '',
            'NextContinuationToken': '',
            'StartAfter': ''
        }
        
def get_s3_contents_object(key, size=1024):
    return  {
            'Key': key,
            'LastModified': None,
            'ETag': '',
            'ChecksumAlgorithm': [
                'SHA256',
            ],
            'Size': size,
            'StorageClass': 'STANDARD',
            'Owner': {
                'DisplayName': '',
                'ID': ''
            }
        }

def get_all_activities_mock(Bucket, Prefix, Delimiter):
    """
        return a function that contains 
        3 years '2021', '2022', '2020'
        3 months in the latest year '2022/01', '2022/03', '2022/06'
        3 objects in the latest month '2022/06/10-08:34:23.json' '2022/06/16-09:21:03.json' '2022/06/26-11:48:29.json'
    """
    if Prefix == '':
        data = get_list_objects_v2_empty_response('bucket_name')
        data['CommonPrefixes'] = [
            {'Prefix': '2022'},
            {'Prefix': '2020'},
            {'Prefix': '2021'}
        ]
        return data 
    
    elif Prefix == '2022':
        data = get_list_objects_v2_empty_response('bucket_name')
        data['CommonPrefixes'] = [
            {'Prefix': '2022/03'},
            {'Prefix': '2022/01'},
            {'Prefix': '2022/06'}
        ]
        return data  
    
    elif Prefix == '2022/06':
        data = get_list_objects_v2_empty_response('bucket_name')
        data['Contents'].append(get_s3_contents_object('2022/06/10-08:34:23.json'))
        data['Contents'].append(get_s3_contents_object('2022/06/26-11:48:29.json'))
        data['Contents'].append(get_s3_contents_object('2022/06/16-09:21:03.json'))
        data['KeyCount'] = 3
        return data
    
def get_activity_data(ids:list) -> str:
    """
        return canned data for store activities
    """
    data = {}
    for id in ids:
        activity = get_single_activity(id)
        key = 'activity:{}:athlete:{}'.format(id, activity['athlete']['id'])
        data[key] = activity
        
    return data

def get_single_activity(id) -> dict:
    """
    """
    return {
        "resource_state": 2,
        "athlete": {"id": 98765, "resource_state": 1},
        "name": "Afternoon Ride",
        "distance": 3598.9,
        "moving_time": 819,
        "elapsed_time": 2360,
        "total_elevation_gain": 6.3,
        "type": "Ride",
        "workout_type": "",
        "id": id,
        "external_id": "garmin_push_123456",
        "upload_id": 6580892880,
        "start_date": "2021-10-31T13:49:46Z",
        "start_date_local": "2021-10-31T13:49:46Z",
        "timezone": "(GMT+00:00) Europe/London",
        "utc_offset": 0.0,
        "start_latlng": [51.0, -0.01],
        "end_latlng": [51.5, -0.09],
        "location_city": "",
        "location_state": "",
        "location_country": "United Kingdom",
        "start_latitude": 51.1,
        "start_longitude": -0.01,
        "achievement_count": 0,
        "kudos_count": 0,
        "comment_count": 0,
        "athlete_count": 1,
        "photo_count": 0,
        "map":
            {
                "id": "a123456",
                "summary_polyline": "",
                "resource_state": 2
            },
        "trainer": False,
        "commute": False,
        "manual": False,
        "private": False,
        "visibility": "everyone",
        "flagged": False,
        "gear_id": "",
        "from_accepted_tag": False,
        "upload_id_str": "123456",
        "average_speed": 4.394,
        "max_speed": 7.468,
        "average_watts": 37.9,
        "kilojoules": 31.0,
        "device_watts": False,
        "has_heartrate": True,
        "average_heartrate": 100.0,
        "max_heartrate": 140.0,
        "heartrate_opt_out": False,
        "display_hide_heartrate_option": True,
        "elev_high": 21.0,
        "elev_low": 14.4,
        "pr_count": 0,
        "total_photo_count": 0,
        "has_kudoed": False,
        "suffer_score": 2.0
    }
