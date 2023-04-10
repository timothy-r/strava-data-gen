import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import sentinel

from functions.lib.app_exceptions import RequestError
from functions.lib.access_token_service import AccessTokenService

class AccessTokenServiceTest(unittest.TestCase):
    
    def setUp(self) -> None:
        
        logger_mock = Mock()
        logger_mock.info = MagicMock()
        logger_mock.error = MagicMock()
        
        self._sm_service = Mock()
        
        self._requests = Mock()
        
        client_id = '1234'
        self._secret_name = 'secret_sauce'
        authz_url = 'https://authz.service.com/auth'
        self._access_token_name = 'access_token'
        
        
        self._access_token_service = AccessTokenService(
            logger=logger_mock,
            sm=self._sm_service,
            requests=self._requests,
            client_id=client_id,
            secret_name=self._secret_name,
            authz_url=authz_url,
            access_token_name=self._access_token_name
        )
        
        return super().setUp()

    """
        if there's an access token cached locally then return it
    """
    def test_get_access_token_from_cache_hit(self):
        
        # for test purposes this can be any string
        access_token = {"token": "access_token"}
        
        # request for the access token
        self._sm_service.get_by_id = MagicMock(return_value=access_token)

        result = self._access_token_service.get_access_token(use_local=True)
        
        self.assertEqual(access_token["token"], result)
        self._sm_service.get_by_id.assert_called_once_with(self._access_token_name)
        self._sm_service.put_by_id.assert_not_called()
        self._requests.post.assert_not_called()
        
    def test_get_access_token_without_cache(self):
        
        # for test purposes this can be any string
        expected_token = {"access_token": "access_token"}
        
        # request for the secrets
        secrets = {'client_secret': 'secret_value', 'refresh_token': 'refresh_token'}
        
        self._sm_service.get_by_id = MagicMock(return_value=secrets)
        self._sm_service.put_by_id = MagicMock(return_value=True)
        
        response = sentinel
        response.status_code = 200
        response.json = Mock(return_value=expected_token)
        
        self._requests.post = Mock(return_value=response)
        
        result = self._access_token_service.get_access_token(use_local=False)
        
        self.assertEqual(expected_token["access_token"], result)
        self._requests.post.assert_called_once()
        self._sm_service.get_by_id.assert_called_once_with(self._secret_name)
        
        # assert sm servive method was called to store the access token
        self._sm_service.put_by_id.assert_called_once_with(
            self._access_token_name,
            {'token': result}
        )
        
    def test_get_access_token_request_fails(self):
        
        # request for the secrets
        secrets = {'client_secret': 'secret_value', 'refresh_token': 'refresh_token'}
        
        self._sm_service.get_by_id = MagicMock(return_value=secrets)

        response = sentinel
        response.status_code = 500
        
        self._requests.post = Mock(return_value=response)
        
        self.assertRaises(
            RequestError, 
            self._access_token_service.get_access_token,
            False
        )
        
        self._requests.post.assert_called_once()
        self._sm_service.get_by_id.assert_called_once_with(self._secret_name)
        self._sm_service.put_by_id.assert_not_called()
    
    def test_get_access_token_fails_without_secrets(self):
        
        # request for the secrets
        secrets = None
        
        self._sm_service.get_by_id = MagicMock(return_value=secrets)

        result = self._access_token_service.get_access_token(use_local=False)
        
        self.assertIsNone(result)
        
        self._requests.post.assert_not_called()
        self._sm_service.get_by_id.assert_called_once_with(self._secret_name)
        self._sm_service.put_by_id.assert_not_called()