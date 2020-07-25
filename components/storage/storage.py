from pathlib import Path
import shutil
from protos.api_bundle_pb2 import APIBundle
from protos.planning_pb2 import Planning

STORAGE_DIRECTORY = Path('destiny-bot')
API_BUNDLE_FILE = Path('api_bundle.dat')
PLANNING_FILE = Path('planning.dat')

class Storage:
    """Parser for user input (intents)."""

    def __init__(self, root_directory):
        try:
            self.__root_path = Path(root_directory).joinpath(STORAGE_DIRECTORY)
            self.__root_path.mkdir(parents=True, exist_ok=True)
        except:
            raise IOError("Impossible d'initialiser le stockage.")

    def clear(self):
        """Clears all the contents inside self.__path."""
        try:
            shutil.rmtree(self.__root_path)
            self.__root_path.mkdir(parents=True, exist_ok=True)
        except:
            raise IOError("Impossible d'effacer le stockage.")

    def read_api_bundle(self):
        """
        Reads the API Bundle that is saved to the storage.
        :return: The read API Bundle.
        """
        try:
            filepath = self.__root_path.joinpath(API_BUNDLE_FILE)
            data = filepath.read_bytes()
            bundle = APIBundle()
            bundle.ParseFromString(data)
        except:
            raise IOError("Impossible de lire l'API Bundle du stockage.")
        return bundle

    def write_api_bundle(self, api_bundle):
        """
        Writes the given API Bundle to the storage.
        :param api_bundle: The bundle to write.
        """
        if not isinstance(api_bundle, APIBundle):
            raise ValueError("L'API Bundle à écrire est invalide.")
        try:
            filepath = self.__root_path.joinpath(API_BUNDLE_FILE)
            data = api_bundle.SerializeToString()
            filepath.write_bytes(data)
        except:
            raise IOError("Impossible d'écrire l'API Bundle dans le stockage.")

    def read_planning(self):
        """
        Reads the planning that is saved to the storage.
        :return: The read planning.
        """
        try:
            filepath = self.__root_path.joinpath(PLANNING_FILE)
            data = filepath.read_bytes()
            bundle = Planning()
            bundle.ParseFromString(data)
        except:
            raise IOError("Impossible de lire le planning du stockage.")
        return bundle

    def write_planning(self, planning):
        """
        Writes the given planning to the storage.
        :param planning: The planning to write.
        """
        if not isinstance(planning, Planning):
            raise ValueError("Le planning à écrire est invalide.")
        try:
            filepath = self.__root_path.joinpath(PLANNING_FILE)
            data = planning.SerializeToString()
            filepath.write_bytes(data)
        except:
            raise IOError("Impossible d'écrire le planning dans le stockage.")
