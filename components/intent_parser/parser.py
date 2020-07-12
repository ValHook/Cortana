class Parser:
    """Parser for user input (intents)."""

    def __init__(self, query):
        self.__query = query

    @property
    def query(self):
        """Returns the query this parser will process."""
        return self.__query
