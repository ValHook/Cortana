from datetime import datetime
import unittest
from dateutil import tz
from components.converters.when import to_when, to_datetime
from protos.when_pb2 import When

TIMEZONE = tz.gettz('Europe/Paris')
DATETIME1 = datetime(2020, 8, 12, 18, 15, 0, 0, TIMEZONE)
DATETIME1_STR = '2020-08-12T18:15:00+02:00'
DATETIME2 = datetime(2021, 1, 10, tzinfo=TIMEZONE)
DATETIME2_STR = '2021-01-10'


class WhenConverterTest(unittest.TestCase):
    """Test class for the intent parser."""

    def test_to_when(self):
        """Verifies the datetime to when converter works as expected."""
        when = to_when(DATETIME1)
        expectation = When()
        expectation.datetime = DATETIME1_STR
        expectation.time_specified = True
        self.assertEqual(when, expectation)

        when = to_when(DATETIME2)
        expectation = When()
        expectation.datetime = DATETIME2_STR
        expectation.time_specified = False
        self.assertEqual(when, expectation)

        when = to_when(None)
        expectation = None
        self.assertEqual(when, expectation)

    def test_to_datetime(self):
        """Verifies the when to datetime converter works as expected."""
        when = When()
        when.datetime = DATETIME1_STR
        when.time_specified = True
        self.assertEqual(to_datetime(when, TIMEZONE), DATETIME1)

        when = When()
        when.datetime = DATETIME2_STR
        when.time_specified = False
        self.assertEqual(to_datetime(when, TIMEZONE), DATETIME2)

        self.assertEqual(to_datetime(None, TIMEZONE), None)


if __name__ == '__main__':
    unittest.main()
