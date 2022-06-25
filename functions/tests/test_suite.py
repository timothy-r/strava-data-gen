import unittest

from tests.data_store_service_test import DataStoreServiceTest
from tests.data_populate_service_test import DataPopulateServiceTest

suite = unittest.TestSuite()

suite.addTest((DataStoreServiceTest()))
suite.addTest(DataPopulateServiceTest())

if __name__ == '__main__':
    unittest.main()