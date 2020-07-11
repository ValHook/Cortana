from protos import rated_player_pb2

class Parser:

    def __init__(self, query):
        self.__query = query

    @property
    def query(self):
        return self.__query
