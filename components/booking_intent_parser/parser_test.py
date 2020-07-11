import unittest
from components.booking_intent_parser import parser

class ParserTest(unittest.TestCase):

    def test_query_property(self):
        sut = parser.Parser('foo')
        self.assertEqual(sut.query, 'foo')

if __name__ == '__main__':
    unittest.main()
