import unittest
import boto3

from moto import mock_iot, mock_iotdata

from pisysmonitor.pisys_monitor import PisysMonitor


@mock_iot
@mock_iotdata
class PisysMonitorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pisysmonitor(self):
        client = boto3.client("iot-data")
        pisys_monitor = PisysMonitor(client)
        pisys_monitor.monitor()
