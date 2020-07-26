from datetime import datetime
import os
import unittest
from dateutil import tz
from components.api_fetcher import api_fetcher
from protos.activity_id_pb2 import ActivityID

SUT_NOW = datetime(2020, 8, 12, 18, 15, 0, 0, tz.gettz('Europe/Paris'))


class FetcherTest(unittest.TestCase):
    """Test class for the Destiny API service."""

    def setUp(self):
        """Set up method."""
        api_key = os.environ.get('BUNGIE_API_KEY', '')
        self.sut = api_fetcher.Fetcher(api_key)

    def test_fetch(self):
        """Makes a fetch call and asserts its contents against some known stuff."""
        bundle = self.sut.fetch(SUT_NOW)
        self.assertEqual(bundle.last_sync_datetime, SUT_NOW.isoformat())
        minimum_expectations = {
            'Walnut Waffle':
            {
                ActivityID.Type.LEVIATHAN: 4,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 1,
                ActivityID.Type.EATER_OF_WORLDS: 3,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 0,
                ActivityID.Type.SPIRE_OF_STARS: 2,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 0,
                ActivityID.Type.CROWN_OF_SORROW: 8,
                ActivityID.Type.LAST_WISH: 5,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 17,
                ActivityID.Type.GARDEN_OF_SALVATION: 10,
            },
            'Oby1Chick':
            {
                ActivityID.Type.LEVIATHAN: 0,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 0,
                ActivityID.Type.EATER_OF_WORLDS: 1,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 0,
                ActivityID.Type.SPIRE_OF_STARS: 1,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 0,
                ActivityID.Type.CROWN_OF_SORROW: 0,
                ActivityID.Type.LAST_WISH: 2,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 3,
                ActivityID.Type.GARDEN_OF_SALVATION: 0,
            },
            'pistache espita':
            {
                ActivityID.Type.LEVIATHAN: 27,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 11,
                ActivityID.Type.EATER_OF_WORLDS: 10,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 20,
                ActivityID.Type.SPIRE_OF_STARS: 6,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 8,
                ActivityID.Type.CROWN_OF_SORROW: 29,
                ActivityID.Type.LAST_WISH: 44,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 65,
                ActivityID.Type.GARDEN_OF_SALVATION: 69,
            },
            'dark0l1ght':
            {
                ActivityID.Type.LEVIATHAN: 9,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 3,
                ActivityID.Type.EATER_OF_WORLDS: 3,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 1,
                ActivityID.Type.SPIRE_OF_STARS: 3,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 0,
                ActivityID.Type.CROWN_OF_SORROW: 15,
                ActivityID.Type.LAST_WISH: 7,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 32,
                ActivityID.Type.GARDEN_OF_SALVATION: 22,
            },
            'croptus':
            {
                ActivityID.Type.LEVIATHAN: 7,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 0,
                ActivityID.Type.EATER_OF_WORLDS: 5,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 0,
                ActivityID.Type.SPIRE_OF_STARS: 2,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 0,
                ActivityID.Type.CROWN_OF_SORROW: 6,
                ActivityID.Type.LAST_WISH: 3,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 12,
                ActivityID.Type.GARDEN_OF_SALVATION: 11,
            },
            'snippro34':
            {
                ActivityID.Type.LEVIATHAN: 13,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 9,
                ActivityID.Type.EATER_OF_WORLDS: 1,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 1,
                ActivityID.Type.SPIRE_OF_STARS: 3,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 0,
                ActivityID.Type.CROWN_OF_SORROW: 12,
                ActivityID.Type.LAST_WISH: 22,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 14,
                ActivityID.Type.GARDEN_OF_SALVATION: 17,
            },
            'Jezehbell':
            {
                ActivityID.Type.LEVIATHAN: 11,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 7,
                ActivityID.Type.EATER_OF_WORLDS: 4,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 7,
                ActivityID.Type.SPIRE_OF_STARS: 4,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 3,
                ActivityID.Type.CROWN_OF_SORROW: 26,
                ActivityID.Type.LAST_WISH: 26,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 83,
                ActivityID.Type.GARDEN_OF_SALVATION: 30,
            },
            'Seven2011':
            {
                ActivityID.Type.LEVIATHAN: 28,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 7,
                ActivityID.Type.EATER_OF_WORLDS: 22,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 3,
                ActivityID.Type.SPIRE_OF_STARS: 2,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 0,
                ActivityID.Type.CROWN_OF_SORROW: 2,
                ActivityID.Type.LAST_WISH: 11,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 25,
                ActivityID.Type.GARDEN_OF_SALVATION: 37,
            },
            'NaughtySoft':
            {
                ActivityID.Type.LEVIATHAN: 6,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 2,
                ActivityID.Type.EATER_OF_WORLDS: 2,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 1,
                ActivityID.Type.SPIRE_OF_STARS: 3,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 0,
                ActivityID.Type.CROWN_OF_SORROW: 1,
                ActivityID.Type.LAST_WISH: 3,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 1,
                ActivityID.Type.GARDEN_OF_SALVATION: 1,
            },
            'FranckRabbit':
            {
                ActivityID.Type.LEVIATHAN: 58,
                ActivityID.Type.LEVIATHAN_PRESTIGE: 76,
                ActivityID.Type.EATER_OF_WORLDS: 87,
                ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: 19,
                ActivityID.Type.SPIRE_OF_STARS: 23,
                ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: 6,
                ActivityID.Type.CROWN_OF_SORROW: 25,
                ActivityID.Type.LAST_WISH: 54,
                ActivityID.Type.SCOURGE_OF_THE_PAST: 65,
                ActivityID.Type.GARDEN_OF_SALVATION: 36,
            },
        }
        for gamer_tag, stats in minimum_expectations.items():
            for activity_type, completions in stats.items():
                activity_type_str = ActivityID.Type.Name(activity_type)
                times_str = "time" if completions == 1 else "times"
                debug_str = gamer_tag + " must have at least completed " + \
                    activity_type_str + " " + str(completions) + " " + times_str
                bundle_stats = bundle.stats_by_player[gamer_tag].activity_stats
                bundle_stat = next(
                    stat for stat in bundle_stats if stat.activity_type == activity_type)
                self.assertGreaterEqual(
                    bundle_stat.completions, completions, debug_str)


if __name__ == '__main__':
    unittest.main()
