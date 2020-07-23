import unittest
from components.img import generator
from protos.planning_pb2 import Planning
from protos.activity_id_pb2 import ActivityID
from protos.rated_player_pb2 import RatedPlayer

class GeneratorTester(unittest.TestCase):
    """Test class for the image generator."""

    def test_planning(self):
        """Not a real test, but writes a sample image on disk."""
        p = Planning()
        a = p.activities.add()
        a.id.type = ActivityID.Type.LEVIATHAN
        a.id.timestamp_seconds = 1594763746
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        a = p.activities.add()
        a.id.type = ActivityID.Type.SPIRE_OF_STARS_PRESTIGE
        a.id.timestamp_seconds = 1595493712
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        a = p.activities.add()
        a.id.type = ActivityID.Type.SCOURGE_OF_THE_PAST
        a.id.timestamp_seconds = 1603639859
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.UNKNOWN
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        a = p.activities.add()
        a.id.type = ActivityID.Type.GARDEN_OF_SALVATION
        a.id.timestamp_seconds = 1598387759
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        gen = generator.Generator(p)
        gifs = gen.generate_image()
        print("IMPORTANT - the result of this test can be visualized here: ", gifs)
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
