from pathlib import Path
import tempfile
import unittest
from components.storage import storage
from protos.activity_pb2 import Activity
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle
from protos.schedule_pb2 import Schedule
from protos.rated_player_pb2 import RatedPlayer


class StorageTest(unittest.TestCase):
    """Test class for the Destiny API service."""

    def setUp(self):
        """Set up method."""
        self.directory = tempfile.TemporaryDirectory()
        self.sut = storage.Storage(self.directory.name)
        self.sut.clear()

    def tearDown(self):
        """Performs some cleanups at the end of each test."""
        self.directory.cleanup()

    def test_no_permission(self):
        """Verifies the storage raises an IOError when encountering permission errors."""
        s = storage.Storage(Path('/'))
        self.assertRaises(IOError, s.write_schedule, Schedule())
        self.assertRaises(IOError, s.write_api_bundle, APIBundle())

    def test_api_bundle_write_then_read(self):
        """Writes then reads an APIBundle to/from the storage."""
        gamer_tags = ['Walnut Waffle', 'SuperFayaChonch', 'foobar', 'Batman']
        stats = [
            APIBundle.Stats.ActivityStat(),
            APIBundle.Stats.ActivityStat(),
            APIBundle.Stats.ActivityStat(),
            APIBundle.Stats.ActivityStat()
        ]
        stats[0].activity_type = ActivityID.Type.LEVIATHAN
        stats[0].completions = 1337
        stats[1].activity_type = ActivityID.Type.GARDEN_OF_SALVATION
        stats[1].completions = 5
        stats[2].activity_type = ActivityID.Type.SPIRE_OF_STARS_PRESTIGE
        stats[2].completions = 0
        stats[3].activity_type = ActivityID.Type.VAULT_OF_GLASS
        stats[3].completions = 10
        bundle = APIBundle()
        bundle.last_sync_datetime = '2021-3-28'
        for gamer_tag in gamer_tags:
            for stat in stats:
                bundle.stats_by_player[gamer_tag].activity_stats.append(stat)
        self.assertEqual(len(bundle.stats_by_player), len(gamer_tags))
        self.assertEqual(len(bundle.stats_by_player[gamer_tags[0]].activity_stats), len(stats))
        self.sut.write_api_bundle(bundle)
        bundle2 = self.sut.read_api_bundle()
        self.assertEqual(bundle, bundle2)
        bundle3 = storage.Storage(self.directory.name).read_api_bundle()
        self.assertEqual(bundle, bundle3)
        self.assertRaises(IOError, self.sut.read_schedule)

    def test_schedule_write_then_read(self):
        """Writes then reads a schedule to/from the storage."""
        schedule = Schedule()
        player1 = RatedPlayer()
        player1.gamer_tag = "Walnut Waffle"
        player1.rating = RatedPlayer.Rating.EXPERIENCED
        player2 = RatedPlayer()
        player2.gamer_tag = "Oby1Chick"
        player2.rating = RatedPlayer.Rating.INTERMEDIATE

        activity1 = Activity()
        activity1.id.type = ActivityID.Type.GARDEN_OF_SALVATION
        activity1.id.when.datetime = '2020-9-1'
        activity1.state = Activity.State.NOT_STARTED
        activity1.squad.players.append(player1)
        schedule.activities.append(activity1)

        activity2 = Activity()
        activity2.id.type = ActivityID.Type.LEVIATHAN_PRESTIGE
        activity2.state = Activity.State.FINISHED
        activity2.squad.substitutes.append(player2)
        schedule.activities.append(activity2)
        self.sut.write_schedule(schedule)
        schedule2 = self.sut.read_schedule()
        self.assertEqual(schedule, schedule2)
        self.assertRaises(IOError, self.sut.read_api_bundle)


if __name__ == '__main__':
    unittest.main()
