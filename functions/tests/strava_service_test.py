import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import sentinel

from functions.lib.strava_service import StravaService

class StravaServiceTest(unittest.TestCase):
    
    def setUp(self) -> None:
        
        logger_mock = Mock()
        logger_mock.info = MagicMock()
        logger_mock.error = MagicMock()
        
        # container = get_container()
        
        self._access_token_service = Mock()
        self._access_token_service.get_access_token = MagicMock(return_value='token')
        
        self._requests = Mock()
        
        self._strava_service = StravaService(
            logger=logger_mock,
            access_token_service=self._access_token_service,
            activities_url="https://strava.com/activities"
        )
        
        self._strava_service.set_requests(self._requests)
        
        return super().setUp()

    def test_get_activities_failed_request(self):
        after = 0
        
        response = sentinel
        sentinel.status_code = 500
        self._requests.get = MagicMock(return_value = response)
        
        activities = self._strava_service.get_activities(after=after)
        self.assertIsNone(activities)
    
    def test_get_activities(self):
        after = 0
        returned_activities = [self._get_mock_activity(111)]
        expected_activities = returned_activities
        
        response_a = Mock()
        response_a.status_code = 200
        response_a.json = Mock(return_value=returned_activities)
        
        response_b = Mock()
        response_b.status_code = 200
        response_b.json = Mock(return_value=[])

        self._requests.get = MagicMock(side_effect = [response_a, response_b])
        
        result = self._strava_service.get_activities(after=after)
        
        self.assertEqual(expected_activities, result)
    
    def test_get_multi_page_activities(self):
        after = 0
        returned_activities_a = [self._get_mock_activity(123)]
        returned_activities_b = [self._get_mock_activity(456)]
        expected_activities = returned_activities_a + returned_activities_b
        
        
        response_a = Mock()
        response_a.status_code = 200
        response_a.json = Mock(return_value=returned_activities_a)
        
        response_b = Mock()
        response_b.status_code = 200
        response_b.json = Mock(return_value=returned_activities_b)

        response_c = Mock()
        response_c.status_code = 200
        response_c.json = Mock(return_value=[])
        
        self._requests.get = MagicMock(side_effect = [response_a, response_b, response_c])
        
        result = self._strava_service.get_activities(after=after)
        
        self.assertEqual(expected_activities, result)
    
    def test_get_single_activity(self):
        id = 0
        returned_activity = self._get_mock_activity(123)
        
        response_a = Mock()
        response_a.status_code = 200
        response_a.json = Mock(return_value=returned_activity)
        
        self._requests.get = MagicMock(side_effect = [response_a])
        
        result = self._strava_service.get_activity(id=id)
        
        self.assertEqual(returned_activity, result)
    
    def test_get_activity_failed_request(self):
        id = 999
        
        response = sentinel
        sentinel.status_code = 500
        self._requests.get = MagicMock(return_value = response)
        
        result = self._strava_service.get_activity(id=id)
        self.assertIsNone(result)
        
    def _get_mock_activity(self, id=101):
        
        return {
            "resource_state": 2, 
            "athlete": {"id": 123, "resource_state": 1}, 
            "name": "Lunch Run", 
            "distance": 9736.0, 
            "moving_time": 3666, 
            "elapsed_time": 3756, 
            "total_elevation_gain": 47.5, 
            "type": "Run", 
            "sport_type": "Run", 
            "id": id, 
            "timezone": "(GMT+00:00) Europe/London", 
            "utc_offset": 3600.0, 
            "location_country": "United Kingdom"
        }
    