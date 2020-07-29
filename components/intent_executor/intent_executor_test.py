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
from protos.schedule_pb2 import Schedule
from protos.rated_player_pb2 import RatedPlayer

TIMEZONE = tz.gettz('Europe/Paris')
NOW = datetime(2020, 8, 12, 18, 15, 0, 0, TIMEZONE)
LOCALE = 'fr'
API_KEY = os.environ.get('CORTANA_BUNGIE_API_KEY', '')

def make_schedule():
    """Constructs a schedule for test cases."""
    s = Schedule()
    a = s.activities.add()
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

    a = s.activities.add()
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

    a = s.activities.add()
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
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "dark0l1ght"
    a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
    (a.squad.players.add()).gamer_tag = "croptus"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER

    a = s.activities.add()
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

    a = s.activities.add()
    a.state = Activity.State.NOT_STARTED
    a.id.type = ActivityID.Type.GARDEN_OF_SALVATION
    a.id.when.datetime = '2020-08-25'
    a.id.when.time_specified = False
    (a.squad.players.add()).gamer_tag = "Cosa58"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    (a.squad.players.add()).gamer_tag = "Walnut Waffle"
    a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
    return s


class ExecutorTest(unittest.TestCase):
    """Test class for the intent executor."""

    def setUp(self):
        """Sets up a basic sut."""
        bundle = APIBundle()
        bundle.ParseFromString(
            Path('components/intent_executor/test_assets/api_bundle.dat').read_bytes()
        )
        schedule = make_schedule()
        self.storage_directory = tempfile.TemporaryDirectory()
        self.storage = Storage(self.storage_directory.name)
        self.storage.clear()
        self.storage.write_schedule(schedule)
        self.storage.write_api_bundle(bundle)
        self.api_fetcher = Fetcher(API_KEY)
        self.img_generator = Generator(TIMEZONE, LOCALE)
        self.sut = Executor(self.storage, self.api_fetcher, self.img_generator)
        self.parser = Parser(LOCALE)

    def tearDown(self):
        """Performs some cleanups at the end of each test."""
        self.storage_directory.cleanup()

    def test_credits(self):
        """Verifies help intents are properly executed."""
        (feedback, images) = self.execute("!cortana credits")
        self.assertTrue(feedback.startswith("Mes créateurs sont"))
        self.assertIsNone(images)

    def test_help(self):
        """Verifies help intents are properly executed."""
        (feedback, images) = self.execute("!cortana help")
        self.assertTrue(feedback.startswith("Guide d'utilisation:"))
        self.assertIsNone(images)

    def test_generate_images(self):
        """Verifies image generation intents are properly executed."""
        mocked_images = [io.BytesIO(), io.BytesIO()]
        self.img_generator.generate_images = MagicMock(return_value=mocked_images)
        (feedback, images) = self.execute("!cortana images")
        schedule = self.storage.read_schedule()
        self.img_generator.generate_images.assert_called_with(schedule)
        self.assertEqual(feedback, "Affiches pour les activités en cours:")
        self.assertEqual(images, mocked_images)

        mocked_images = []
        self.img_generator.generate_images = MagicMock(return_value=mocked_images)
        (feedback, images) = self.execute("!cortana images")
        schedule = self.storage.read_schedule()
        self.img_generator.generate_images.assert_called_with(schedule)
        self.assertEqual(feedback, "Il n'y a aucune activité dans le planning pour le moment.")
        self.assertEqual(images, mocked_images)

    def test_sync(self):
        """Verifies sync intents are properly executed."""
        new_bundle = self.storage.read_api_bundle()
        new_bundle.last_sync_datetime = NOW.isoformat()
        new_bundle.stats_by_player['Walnut Waffle'].activity_stats[0].completions = 9999
        self.api_fetcher.fetch = MagicMock(return_value=new_bundle)
        (feedback, images) = self.execute("!cortana sync")

        self.api_fetcher.fetch.assert_called_with(NOW)
        self.assertEqual(self.storage.read_api_bundle(), new_bundle)
        self.assertEqual(feedback, "Joueurs et niveaux d'experiences synchronisés.")
        self.assertIsNone(images)

    def test_lastsync(self):
        """Verifies lastsync intents are properly executed."""
        (feedback, images) = self.execute("!cortana lastsync")
        self.assertEqual(feedback, "Dernière synchronisation: 2020-07-26T16:05:00+02:00")
        self.assertIsNone(images)

    def test_clearall(self):
        """Verifies clearall intents are properly executed."""
        (feedback, images) = self.execute("!cortana clearall")
        expectation = Schedule()
        self.assertEqual(self.storage.read_schedule(), expectation)
        self.assertEqual(feedback, "Toutes les activités du planning sont désormais supprimées.")
        self.assertIsNone(images)

    def test_clearpast(self):
        """Verifies clearpast intents are properly executed."""
        schedule_before = self.storage.read_schedule()
        (feedback, images) = self.execute("!cortana clearpast")
        expected_activities = schedule_before.activities
        expected_activities.pop(0)
        expectation = Schedule()
        expectation.activities.extend(expected_activities)

        self.assertTrue(
            feedback.startswith("Les activités des semaines précédentes ont été suprimées.")
        )
        self.assertIsNone(images)
        self.assertEqual(self.storage.read_schedule(), expectation)

    def test_infoall(self):
        """Verifies infoall intents are properly executed."""
        schedule = self.storage.read_schedule()
        (feedback, images) = self.execute("!cortana infoall")
        self.assertIsNone(images)
        self.assertEqual(feedback, str(schedule))

        self.execute("!cortana clearall")
        (feedback, images) = self.execute("!cortana infoall")
        self.assertIsNone(images)
        self.assertEqual(feedback, "Le planning est vide.")

    def test_info(self):
        """Verifies info intents are properly executed."""
        schedule = self.storage.read_schedule()
        (feedback, images) = self.execute("!cortana info calus")
        self.assertIsNone(images)
        self.assertEqual(feedback, str(schedule.activities[0]))

    def test_clear(self):
        """Verifies clear intents are properly executed."""
        schedule = self.storage.read_schedule()
        self.execute("!cortana clear calus")
        self.assertRaises(ValueError, self.execute, "!cortana clear jds")
        (feedback, images) = self.execute("!cortana clear jds 17/08")
        self.assertRaises(ValueError, self.execute, "!cortana clear jds 17/08")
        schedule.activities.pop(3)
        schedule.activities.pop(0)

        self.assertTrue(feedback.startswith("Activité supprimée"))
        self.assertIsNone(images)
        self.assertEqual(self.storage.read_schedule(), schedule)

    def test_milestone(self):
        """Verifies milestone intents are properly executed."""
        schedule = self.storage.read_schedule()
        self.execute("!cortana milestone flèche prestige save étape 2")
        (feedback, images) = self.execute(
            "!cortana milestone fléau dimanche 14h30 save au deuxième boss"
        )
        self.assertRaises(ValueError, self.execute, "!cortana milestone dernier voeu save au boss")
        schedule.activities[1].state = Activity.State.MILESTONED
        schedule.activities[1].milestone = "Save étape 2"
        schedule.activities[2].state = Activity.State.MILESTONED
        schedule.activities[2].milestone = "Save au deuxième boss"
        self.assertTrue(feedback.startswith("Étape mise à jour"))
        self.assertIsNone(images)
        self.assertEqual(self.storage.read_schedule(), schedule)

    def test_finish(self):
        """Verifies finish intents are properly executed."""
        schedule = self.storage.read_schedule()
        self.execute("!cortana finish jds lundi 21h15")
        (feedback, images) = self.execute("!cortana finish jds 25/08")
        self.assertRaises(ValueError, self.execute, "!cortana milestone couronne save au boss")
        schedule.activities[3].state = Activity.State.FINISHED
        schedule.activities[4].state = Activity.State.FINISHED
        self.assertTrue(feedback.startswith("Good job!\nActivité marquée comme terminée:\n"))
        self.assertIsNone(images)
        self.assertEqual(self.storage.read_schedule(), schedule)

    def test_update_date(self):
        """Verifies update date intents are properly executed."""
        schedule = self.storage.read_schedule()
        self.execute("!cortana date calus 9/8 9/8 23h")
        self.execute("!cortana date fleau dimanche 21h30")
        self.execute("!cortana date jds 25/08/2020 24/08/2021")
        self.execute("!cortana date flèche prestige aujourd'hui demain 13h")
        self.assertRaises(ValueError, self.execute, "!cortana date dévoreur prestige lundi")
        (feedback, images) = self.execute("!cortana date jds 17/08 21h15 mercredi")
        schedule.activities[0].id.when.datetime = '2020-08-09T23:00:00+02:00'
        schedule.activities[0].id.when.time_specified = True
        schedule.activities[1].id.when.datetime = '2020-08-13T13:00:00+02:00'
        schedule.activities[1].id.when.time_specified = True
        schedule.activities[2].id.when.datetime = '2020-08-16T21:30:00+02:00'
        schedule.activities[2].id.when.time_specified = True
        schedule.activities[3].id.when.datetime = '2020-08-19'
        schedule.activities[3].id.when.time_specified = False
        schedule.activities[4].id.when.datetime = '2021-08-24'
        schedule.activities[4].id.when.time_specified = False
        self.assertTrue(feedback.startswith("Date mise à jour:\n"))
        self.assertIsNone(images)
        updated_schedule = self.storage.read_schedule()
        self.assertEqual(updated_schedule, schedule)

    def test_update_players(self):
        """Verifies update players intents are properly executed."""
        # Test 1 addition.
        schedule0 = self.storage.read_schedule()
        self.execute("!cortana fleche prestige +Walnut Waffle")
        self.execute("!cortana fleche prestige +Walnut Waffle")
        schedule1 = self.storage.read_schedule()
        self.assertEqual(len(schedule1.activities[1].squad.players), 3)
        fleche1 = schedule1.activities[1]
        self.assertEqual(fleche1.squad.players[2].gamer_tag, "Walnut Waffle")
        self.assertEqual(fleche1.squad.players[2].rating, RatedPlayer.Rating.BEGINNER)
        self.execute("!cortana fleche prestige -Walnut Waffle")
        schedule2 = self.storage.read_schedule()
        self.assertEqual(schedule2, schedule0)

        # Test additions and deletions.
        fleau0 = schedule0.activities[2]
        self.execute("!cortana fleau xxMarie -Walnut Waffle")
        self.execute("!cortana fleau du passé -Franstuk +kyzerjo -klaexy")
        schedule3 = self.storage.read_schedule()
        fleau1 = schedule3.activities[2]
        self.assertEqual(fleau1.squad.players[1].gamer_tag, "Oby1Chick")
        self.assertEqual(fleau1.squad.players[3].gamer_tag, "croptus")
        self.assertEqual(fleau1.squad.players[4].gamer_tag, "xXmarie91Xx")
        self.assertEqual(fleau1.squad.players[4].rating, RatedPlayer.Rating.BEGINNER)
        self.assertEqual(fleau1.squad.players[5].gamer_tag, "kyzerjo88")
        self.assertEqual(fleau1.squad.players[5].rating, RatedPlayer.Rating.EXPERIENCED)
        self.execute("!cortana fleau -Mariexx +Walnut Waffle -kyzerjo +Franstuck")
        schedule4 = self.storage.read_schedule()
        fleau2 = schedule4.activities[2]
        fleau0_gamer_tags = list(map(lambda p: p.gamer_tag, fleau0.squad.players))
        fleau2_gamer_tags = list(map(lambda p: p.gamer_tag, fleau2.squad.players))
        self.assertEqual(set(fleau0_gamer_tags), set(fleau2_gamer_tags))

        # Test surbooking.
        self.assertRaises(ValueError, self.execute, "!cortana jardin 17/08 +SUperFayaChon")
        self.execute("!cortana jardin 17/08 -klaexy")
        schedule5 = self.storage.read_schedule()
        jds1 = schedule0.activities[3]
        jds2 = schedule5.activities[3]
        self.assertEqual(jds1, jds2)
        self.assertRaises(ValueError, self.execute, "!cortana jardin 17/08 +SUperFayaChon")
        self.execute("!cortana jardin 17/08 -Cosa58")
        self.execute("!cortana jardin 17/08 +SUperFayaChon")
        schedule6 = self.storage.read_schedule()
        jds3 = schedule6.activities[3]
        self.assertEqual(jds3.squad.players[5].gamer_tag, "SuperFayaChonch")

        # Test underbooking.
        self.execute("!cortana flèche d'étoiles prestige 12 août -snippro34")
        self.assertRaises(
            ValueError,
            self.execute,
            "!cortana flèche d'étoiles prestige 12 août -Jezebell"
        )
        (feedback, images) = self.execute("!cortana fleche prestige +Striikers -Jezebell")
        schedule7 = self.storage.read_schedule()
        fleche2 = schedule7.activities[1]
        self.assertEqual(len(fleche2.squad.players), 1)
        self.assertEqual(fleche2.squad.players[0].gamer_tag, "Striikers")
        self.assertTrue(feedback.startswith("Escouade mise à jour"))
        self.assertIsNone(images)

    def test_update_substitutes(self):
        """Verifies update substitutes intents are properly executed."""
        # Test 1 addition.
        schedule0 = self.storage.read_schedule()
        self.execute("!cortana backup fleche prestige +Walnut Waffle")
        self.execute("!cortana backup fleche prestige +Walnut Waffle")
        schedule1 = self.storage.read_schedule()
        self.assertEqual(len(schedule1.activities[1].squad.substitutes), 2)
        fleche1 = schedule1.activities[1]
        self.assertEqual(fleche1.squad.substitutes[1].gamer_tag, "Walnut Waffle")
        self.assertEqual(fleche1.squad.substitutes[1].rating, RatedPlayer.Rating.BEGINNER)
        self.execute("!cortana backup fleche prestige -Walnut Waffle")
        self.execute("!cortana backup fleche prestige -Walnut Waffle")
        schedule2 = self.storage.read_schedule()
        self.assertEqual(schedule2, schedule0)

        # Test additions and deletions.
        calus0 = schedule0.activities[0]
        self.execute("!cortana backup calus xxMarie -affectevil")
        self.execute("!cortana backup calus -croptus +Neofighter")
        schedule3 = self.storage.read_schedule()
        calus1 = schedule3.activities[0]
        self.assertEqual(calus1.squad.substitutes[0].gamer_tag, "xXmarie91Xx")
        self.assertEqual(calus1.squad.substitutes[0].rating, RatedPlayer.Rating.BEGINNER)
        self.assertEqual(calus1.squad.substitutes[1].gamer_tag, "Neofighter")
        self.assertEqual(calus1.squad.substitutes[1].rating, RatedPlayer.Rating.BEGINNER)
        self.execute("!cortana backup calus croptus affectevil -xxmarie -Neofighter")
        schedule4 = self.storage.read_schedule()
        calus2 = schedule4.activities[0]
        calus0_gamer_tags = list(map(lambda p: p.gamer_tag, calus0.squad.substitutes))
        calus2_gamer_tags = list(map(lambda p: p.gamer_tag, calus2.squad.substitutes))
        self.assertEqual(set(calus0_gamer_tags), set(calus2_gamer_tags))

        # Test surbooking
        self.assertRaises(
            ValueError,
            self.execute,
            "!cortana backup jds 25/08 +cosa +hartog +kyzerjo"
        )
        self.execute("!cortana backup jardin 25/08 -klaexy")
        schedule5 = self.storage.read_schedule()
        jds1 = schedule0.activities[3]
        jds2 = schedule5.activities[3]
        self.assertEqual(jds1, jds2)
        self.assertRaises(
            ValueError,
            self.execute,
            "!cortana backup jardin 17/08 +cosa +hartog +kyzerjo"
        )
        self.execute("!cortana backup jardin 25/08 +live x gaming")
        (feedback, images) = self.execute("!cortana backup jardin 25/08 +babwazza")
        schedule6 = self.storage.read_schedule()
        jds3 = schedule6.activities[4]
        self.assertEqual(jds3.squad.substitutes[0].gamer_tag, "LiVe x GamIing")
        self.assertEqual(jds3.squad.substitutes[1].gamer_tag, "BAB x WaZZa")
        self.assertTrue(feedback.startswith("Escouade mise à jour"))
        self.assertIsNone(images)

        # Test underbooking not possible
        self.assertEqual(len(schedule6.activities[1].squad.substitutes), 1)
        self.execute("!cortana backup fleche prestige -NaughtySoft")
        schedule7 = self.storage.read_schedule()
        self.assertEqual(len(schedule7.activities[1].squad.substitutes), 0)
        self.execute("!cortana backup fleche prestige -SuperFayaChonch -NaughtySoft -Cosa -Hartog")
        schedule8 = self.storage.read_schedule()
        self.assertEqual(schedule8, schedule7)

    def test_insert(self):
        """Verifies insert intents are properly executed."""
        self.execute("!cortana dévoreur karibnkilla")
        (feedback, images) = self.execute(
            "!cortana couronne jeudi 19h cosa58 Walnut Waffle omegagip"
        )
        schedule = self.storage.read_schedule()
        self.assertEqual(len(schedule.activities), 7)
        devoreur = schedule.activities[-2]
        self.assertEqual(devoreur.id.type, ActivityID.Type.EATER_OF_WORLDS)
        self.assertEqual(devoreur.state, Activity.State.NOT_STARTED)
        self.assertEqual(devoreur.squad.players[0].gamer_tag, "karibNkilla")
        self.assertEqual(devoreur.squad.players[0].rating, RatedPlayer.Rating.BEGINNER)
        couronne = schedule.activities[-1]
        self.assertEqual(couronne.id.type, ActivityID.Type.CROWN_OF_SORROW)
        self.assertEqual(couronne.id.when.datetime, '2020-08-13T19:00:00+02:00')
        self.assertTrue(couronne.id.when.time_specified)
        self.assertEqual(couronne.state, Activity.State.NOT_STARTED)
        self.assertEqual(len(couronne.squad.players), 3)
        self.assertEqual(couronne.squad.players[2].gamer_tag, "Omega Gips")
        self.assertEqual(couronne.squad.players[2].rating, RatedPlayer.Rating.BEGINNER)
        self.assertTrue(feedback.startswith("Activité créée"))
        self.assertIsNone(images)

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
