import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import json

from functions.lib.secret_manager_service import SecretManagerService

class SecretManagerServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        
        logger_mock = Mock()
        logger_mock.info = MagicMock()
        logger_mock.error = MagicMock()
        
        self._mock_sm = Mock()
        
        self._secret_manager_service = SecretManagerService(
            self._mock_sm,
            logger_mock
        )
        
        return super().setUp()
    
    def test_get_by_id(self):
        id = 'secret_key'
        data = {'key':'value'}
        
        secret_data = {'SecretString': json.dumps(data)}
        
        self._mock_sm.get_secret_value = MagicMock(return_value=secret_data)
        
        result = self._secret_manager_service.get_by_id(id)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['key'], 'value')
    
    def test_get_by_id_invalid(self):
        id = 'secret_key'
        data = {'key':'value'}
        
        secret_data = {'Invalid': json.dumps(data)}
        
        self._mock_sm.get_secret_value = MagicMock(return_value=secret_data)
        
        result = self._secret_manager_service.get_by_id(id)
        
        self.assertIsNone(result)        

    def test_get_by_id_error(self):
        
        id = 'secret_key'
        data = {'key':'value'}
        
        secret_data = {'SecretString': json.dumps(data)}
        
        self._mock_sm.get_secret_value = Mock(side_effect=ClientError({}, {}))
        
        result = self._secret_manager_service.get_by_id(id)
        
        self.assertIsNone(result) 
    
    def test_put_by_id(self):
        id = 'secret_key'
        data = {'key':'value'}
        
        self._mock_sm.put_secret_value = Mock(return_value=True)
        
        result = self._secret_manager_service.put_by_id(id, data)
        
        self.assertTrue(result)
    
    def test_put_by_id_creates_entry(self):
        id = 'secret_key'
        data = {'key':'value'}
        self._mock_sm.put_secret_value = Mock(side_effect=ClientError({}, {}))
        self._mock_sm.create_secret = Mock(return_value=True)
        
        result = self._secret_manager_service.put_by_id(id, data)
        
        self.assertTrue(result)