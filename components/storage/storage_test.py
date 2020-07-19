from components.storage import storage
from pathlib import Path
import unittest
from protos.api_bundle_pb2 import APIBundle
from protos.activity_id_pb2 import ActivityID


class FetcherTest(unittest.TestCase):
    """Test class for the Destiny API service."""

    def setUp(self):
        """Set up method."""
        sut = storage.Storage(Path('/tmp'))
        sut.clear()
        self.sut = sut

    def test_no_permission(self):
        """Verifies the storage raises an IOError when encountering permission errors."""
        self.assertRaises(IOError, storage.Storage, Path('/'))

    def test_api_bundle_read_non_existing(self):
        """
        Verifies the storage raises an IOError,
        when asked to read an APIBundle and there is not any.
        """
        self.assertRaises(IOError, self.sut.read_api_bundle)

    def test_api_bundle_write_then_read(self):
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
        for gamer_tag in gamer_tags:
            for stat in stats:
                bundle.stats_by_player[gamer_tag].activity_stats.append(stat)
        self.assertEquals(len(bundle.stats_by_player), len(gamer_tags))
        self.assertEquals(len(bundle.stats_by_player[gamer_tags[0]].activity_stats), len(stats))
        self.sut.write_api_bundle(bundle)
        bundle2 = self.sut.read_api_bundle()
        self.assertEqual(bundle, bundle2)
        bundle3 = storage.Storage(Path('/tmp')).read_api_bundle()
        self.assertEqual(bundle, bundle3)




if __name__ == '__main__':
    unittest.main()
