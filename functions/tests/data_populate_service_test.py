import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock

from lib.DataPopulateService import DataPopulateService

class DataPopulateServiceTest(unittest.TestCase):
    
    def setUp(self) -> None:
            
        logger_mock = Mock()
        logger_mock.info = MagicMock()
        logger_mock.error = MagicMock()
        
        self._strava_service_mock = MagicMock()
        self._data_store_service_mock = MagicMock()
        
        self._data_populate_service = DataPopulateService(
            logger=logger_mock,
            strava_service=self._strava_service_mock,
            data_store_service=self._data_store_service_mock
            )
        
        return super().setUp()
    
    def test_update(self):
        
        self._strava_service_mock.get_activities = MagicMock()
        
        expected = 10
        mock_return = MagicMock()
        mock_return.return_value = expected
        self._data_store_service_mock.add_new_activities = mock_return
        
        after = 0
        actual = self._data_populate_service.update(after)
        
        assert(actual == expected)
        