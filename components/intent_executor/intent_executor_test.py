from datetime import datetime
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock
from dateutil import tz
from components.intent_parser.intent_parser import Parser
from components.intent_executor.intent_executor import Executor
from components.api_fetcher.api_fetcher import Fetcher
from components.img_generator.img_generator import Generator
from components.storage.storage import Storage
from protos.activity_id_pb2 import ActivityID
from protos.activity_pb2 import Activity
from protos.api_bundle_pb2 import APIBundle
from protos.planning_pb2 import Planning
from protos.rated_player_pb2 import RatedPlayer

TIMEZONE = tz.gettz('Europe/Paris')
NOW = datetime(2020, 8, 12, 18, 15, 0, 0, TIMEZONE)
LOCALE = 'fr'
API_KEY = os.environ.get('BUNGIE_API_KEY', '')

def make_planning():
    """Constructs a planning for test cases."""
    p = Planning()
    a = p.activities.add()
    a.state = Activity.State.FINISHED
    a.id.type = ActivityID.Type.LEVIATHAN
    a.id.when.datetime = '2020-08-09T21:15:00+02:00'
    a.id.when.time_specified = True
    (a.squad.players.add()).gamer_tag = "Oby1Chick"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.players.add()).gamer_tag = "dark0l1ght"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.players.add()).gamer_tag = "Cosa58"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "Franstuk"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "Walnut Waffle"
    a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
    (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.substitutes.add()).gamer_tag = "croptus"
    a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.substitutes.add()).gamer_tag = "affectevil"
    a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER

    a = p.activities.add()
    a.state = Activity.State.NOT_STARTED
    a.id.type = ActivityID.Type.SPIRE_OF_STARS_PRESTIGE
    a.id.when.datetime = '2020-08-12'
    a.id.when.time_specified = False
    (a.squad.players.add()).gamer_tag = "snippro34"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "Jezehbell"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.substitutes.add()).gamer_tag = "NaughtySoft"
    a.squad.substitutes[-1].rating = RatedPlayer.Rating.INTERMEDIATE

    a = p.activities.add()
    a.state = Activity.State.MILESTONED
    a.milestone = "Save au boss"
    a.id.type = ActivityID.Type.SCOURGE_OF_THE_PAST
    a.id.when.datetime = '2020-08-16T14:30:00+02:00'
    a.id.when.time_specified = True
    (a.squad.players.add()).gamer_tag = "Duality Cobra"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.players.add()).gamer_tag = "Walnut Waffle"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.players.add()).gamer_tag = "Oby1Chick"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.players.add()).gamer_tag = "Franstuk"
    a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
    (a.squad.players.add()).gamer_tag = "dark0l1ght"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.players.add()).gamer_tag = "croptus"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER

    a = p.activities.add()
    a.state = Activity.State.NOT_STARTED
    a.id.type = ActivityID.Type.GARDEN_OF_SALVATION
    a.id.when.datetime = '2020-08-17T21:15:00+02:00'
    a.id.when.time_specified = True
    (a.squad.players.add()).gamer_tag = "Hartog31"
    a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
    (a.squad.players.add()).gamer_tag = "Oby1Chick"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "Walnut Waffle"
    a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
    (a.squad.players.add()).gamer_tag = "Franstuk"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "dark0l1ght"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "Cosa58"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.substitutes.add()).gamer_tag = "croptus"
    a.squad.substitutes[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.substitutes.add()).gamer_tag = "affectevil"
    a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER

    a = p.activities.add()
    a.state = Activity.State.NOT_STARTED
    a.id.type = ActivityID.Type.GARDEN_OF_SALVATION
    a.id.when.datetime = '2020-08-25'
    a.id.when.time_specified = False
    (a.squad.players.add()).gamer_tag = "Cosa58"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "Walnut Waffle"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    return p


class ExecutorTest(unittest.TestCase):
    """Test class for the intent executor."""

    def setUp(self):
        """Sets up a basic sut."""
        bundle = APIBundle()
        bundle.ParseFromString(
            Path('components/intent_executor/test_assets/api_bundle.dat').read_bytes()
        )
        planning = make_planning()
        self.storage_directory = tempfile.TemporaryDirectory()
        self.storage = Storage(self.storage_directory.name)
        self.storage.clear()
        self.storage.write_planning(planning)
        self.storage.write_api_bundle(bundle)
        self.api_fetcher = Fetcher(API_KEY)
        self.img_generator = Generator(TIMEZONE, LOCALE)
        self.sut = Executor(self.storage, self.api_fetcher, self.img_generator)
        self.parser = Parser(LOCALE)

    def tearDown(self):
        """Performs some cleanups at the end of each test."""
        self.storage_directory.cleanup()

    def test_generate_images(self):
        """Verifies image generation intents are properly executed."""
        mocked_images = [io.BytesIO(), io.BytesIO()]
        self.img_generator.generate_images = MagicMock(return_value=mocked_images)
        (feedback, images) = self.execute("!raid images")
        planning = self.storage.read_planning()

        self.img_generator.generate_images.assert_called_with(planning)
        self.assertEqual(feedback, "Affiches pour les activités en cours :")
        self.assertEqual(images, mocked_images)

    def test_sync(self):
        """Verifies sync intents are properly executed."""
        new_bundle = self.storage.read_api_bundle()
        new_bundle.last_sync_datetime = NOW.isoformat()
        new_bundle.stats_by_player['Walnut Waffle'].activity_stats[0].completions = 9999
        self.api_fetcher.fetch = MagicMock(return_value=new_bundle)
        (feedback, images) = self.execute("!raid sync")

        self.api_fetcher.fetch.assert_called_with()
        self.assertEqual(self.storage.read_api_bundle(), new_bundle)
        self.assertEqual(feedback, "Joueurs et niveaux d'experiences synchronisés.")
        self.assertIsNone(images)

    def test_lastsync(self):
        """Verifies lastsync intents are properly executed."""
        (feedback, images) = self.execute("!raid lastsync")
        self.assertEqual(feedback, "Dernière synchronisation : 2020-07-26T16:05:00+02:00")
        self.assertIsNone(images)

    def test_clearpast(self):
        """Verifies clearpast intents are properly executed."""
        planning_before = self.storage.read_planning()
        (feedback, images) = self.execute("!raid clearpast")
        expected_activities = planning_before.activities
        expected_activities.pop(0)
        expectation = Planning()
        expectation.activities.extend(expected_activities)

        self.assertTrue(
            feedback.startswith("Les activités des semaines précédentes ont été suprimées.")
        )
        self.assertIsNone(images)
        self.assertEqual(self.storage.read_planning(), expectation)

    def test_remove(self):
        """Verifies remove intents are properly executed."""
        planning = self.storage.read_planning()
        self.execute("!raid remove calus")
        self.assertRaises(ValueError, self.execute, "!raid remove jds")
        (feedback, images) = self.execute("!raid remove jds 17/08")
        self.assertRaises(ValueError, self.execute, "!raid remove jds 17/08")
        planning.activities.pop(3)
        planning.activities.pop(0)

        self.assertTrue(feedback.startswith("Activité supprimée"))
        self.assertIsNone(images)
        self.assertEqual(self.storage.read_planning(), planning)

    def test_milestone(self):
        """Verifies milestone intents are properly executed."""
        planning = self.storage.read_planning()
        self.execute("!raid milestone flèche prestige save étape 2")
        (feedback, images) = self.execute(
            "!raid milestone fléau dimanche 14h30 save au deuxième boss"
        )
        self.assertRaises(ValueError, self.execute, "!raid milestone dernier voeu save au boss")
        planning.activities[1].state = Activity.State.MILESTONED
        planning.activities[1].milestone = "Save étape 2"
        planning.activities[2].state = Activity.State.MILESTONED
        planning.activities[2].milestone = "Save au deuxième boss"
        self.assertTrue(feedback.startswith("Milestone mise à jour"))
        self.assertIsNone(images)
        self.assertEqual(self.storage.read_planning(), planning)

    def test_finish(self):
        """Verifies finish intents are properly executed."""
        planning = self.storage.read_planning()
        self.execute("!raid finish jds lundi 21h15")
        (feedback, images) = self.execute("!raid finish jds 25/08")
        self.assertRaises(ValueError, self.execute, "!raid milestone couronne save au boss")
        planning.activities[3].state = Activity.State.FINISHED
        planning.activities[4].state = Activity.State.FINISHED
        self.assertTrue(feedback.startswith("Good job!\nActivité marquée comme terminée :\n"))
        self.assertIsNone(images)
        self.assertEqual(self.storage.read_planning(), planning)

    def test_update_date(self):
        """Verifies update date intents are properly executed."""
        planning = self.storage.read_planning()
        self.execute("!raid date calus 9/8 9/8 23h")
        self.execute("!raid date fleau dimanche 21h30")
        self.execute("!raid date jds 25/08/2020 24/08/2021")
        self.execute("!raid date flèche prestige aujourd'hui demain 13h")
        self.assertRaises(ValueError, self.execute, "!raid date dévoreur prestige lundi")
        (feedback, images) = self.execute("!raid date jds 17/08 21h15 mercredi")
        planning.activities[0].id.when.datetime = '2020-08-09T23:00:00+02:00'
        planning.activities[0].id.when.time_specified = True
        planning.activities[1].id.when.datetime = '2020-08-13T13:00:00+02:00'
        planning.activities[1].id.when.time_specified = True
        planning.activities[2].id.when.datetime = '2020-08-16T21:30:00+02:00'
        planning.activities[2].id.when.time_specified = True
        planning.activities[3].id.when.datetime = '2020-08-19'
        planning.activities[3].id.when.time_specified = False
        planning.activities[4].id.when.datetime = '2021-08-24'
        planning.activities[4].id.when.time_specified = False
        self.assertTrue(feedback.startswith("Date mise à jour :\n"))
        self.assertIsNone(images)
        updated_planning = self.storage.read_planning()
        self.assertEqual(updated_planning, planning)


    def execute(self, message):
        """
        Helper that executes an intent from the given message, BUNDLE and NOW.
        :param message: The message to create and execute an intent from.
        :return: The executor's response.
        :raises: If something failed along the way.
        """
        bundle = self.storage.read_api_bundle()
        intent = self.parser.parse(message, bundle, NOW)
        return self.sut.execute(intent, NOW)


if __name__ == '__main__':
    unittest.main()
