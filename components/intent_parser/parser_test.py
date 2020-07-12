import unittest
from components.intent_parser import parser


class ParserTest(unittest.TestCase):
    """Test class for the intent parser."""

    def test_query_property(self):
        """Verifies the query propery is properly set."""
        sut = parser.Parser('foo')
        self.assertEqual(sut.query, 'foo')


if __name__ == '__main__':
    unittest.main()
