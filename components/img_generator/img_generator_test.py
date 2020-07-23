import unittest
from components.img_generator import img_generator
from protos.planning_pb2 import Planning
from protos.activity_id_pb2 import ActivityID
from protos.rated_player_pb2 import RatedPlayer
import tempfile
import hashlib


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
        a = p.activities.add()
        a.id.type = ActivityID.Type.WRATH_OF_THE_MACHINE
        a.id.timestamp_seconds = 1548387759
        (a.squad.players.add()).gamer_tag = "Cosa58"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        a.squad.players[-1].rating = RatedPlayer.Rating.EXPERIENCED
        (a.squad.players.add()).gamer_tag = "Franstuck"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        a.squad.players[-1].rating = RatedPlayer.Rating.INTERMEDIATE
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        a.squad.players[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        a.squad.substitutes[-1].rating = RatedPlayer.Rating.BEGINNER
        gen = img_generator.Generator(p)
        gifs = gen.generate_images()

        hash_reference = {
            0: "ad11f5a62c7c7f734aca59e5cd8c473ebcd961e56e482c3cb752ed2ff4c0c723",
            1: "13d9eec94c0479b9a5a129079df8e1749dc42881d2c1d714f07cdfe37885ea43"
        }

        for gif_index, gif in enumerate(gifs):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as temp:
                temp.write(gif.getbuffer())
                print("NOTE - the result of this test can be visualized here: ", temp.name)
            self.assertEqual(hashlib.sha256(gif.getbuffer()).hexdigest(), hash_reference[gif_index], True)


if __name__ == '__main__':
    unittest.main()
