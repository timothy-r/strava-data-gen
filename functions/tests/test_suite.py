import unittest

from tests.data_store_service_test import DataStoreServiceTest

suite = unittest.TestSuite()

suite.addTest((DataStoreServiceTest()))

if __name__ == '__main__':
    unittest.main()