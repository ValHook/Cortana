from components.api_fetcher import api_fetcher
import os
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle
import unittest

class FetcherTest(unittest.TestCase):
    """Test class for the Destiny API service."""

    def setUp(self):
        api_key = os.environ.get('BUNGIE_API_KEY', '')
        self.sut = api_fetcher.Fetcher(api_key)

    def test_fetch(self):
        bundle = self.sut.fetch()
        minimum_expectations = {
        	'Walnut Waffle': 
        		{
        			ActivityID.Type.CALUS: 4,
        			ActivityID.Type.CALUS_PRESTIGE: 1,
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
        			ActivityID.Type.CALUS: 0,
        			ActivityID.Type.CALUS_PRESTIGE: 0,
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
        			ActivityID.Type.CALUS: 27,
        			ActivityID.Type.CALUS_PRESTIGE: 11,
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
        			ActivityID.Type.CALUS: 9,
        			ActivityID.Type.CALUS_PRESTIGE: 3,
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
        			ActivityID.Type.CALUS: 7,
        			ActivityID.Type.CALUS_PRESTIGE: 0,
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
        			ActivityID.Type.CALUS: 13,
        			ActivityID.Type.CALUS_PRESTIGE: 9,
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
        			ActivityID.Type.CALUS: 11,
        			ActivityID.Type.CALUS_PRESTIGE: 7,
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
        			ActivityID.Type.CALUS: 28,
        			ActivityID.Type.CALUS_PRESTIGE: 7,
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
        			ActivityID.Type.CALUS: 6,
        			ActivityID.Type.CALUS_PRESTIGE: 2,
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
        			ActivityID.Type.CALUS: 58,
        			ActivityID.Type.CALUS_PRESTIGE: 76,
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
        		debug_str = gamer_tag + " must have at least completed " + activity_type_str + " " + str(completions) + " " + times_str
        		bundle_stats = bundle.stats_by_player[gamer_tag].activity_stats
        		bundle_stat = next(bundle_stat for bundle_stat in bundle_stats if bundle_stat.activity_type == activity_type)
        		self.assertGreaterEqual(bundle_stat.completions, completions, debug_str)




if __name__ == '__main__':
    unittest.main()
