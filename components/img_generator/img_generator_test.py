import hashlib
import tempfile
import unittest
from babel.dates import get_timezone
from components.img_generator import img_generator
from protos.planning_pb2 import Planning
from protos.activity_id_pb2 import ActivityID
from protos.rated_player_pb2 import RatedPlayer


# pylint: disable=too-many-statements
class GeneratorTester(unittest.TestCase):
    """Test class for the image generator."""

    def test_planning(self):
        """
        Verifies the hash of generated GIFs to ensure the images stay the same.
        """
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
        gen = img_generator.Generator(p, get_timezone('Europe/Paris'))
        gifs = gen.generate_images()

        hash_reference = {
            0: "53da3f9dd08a454081c65baaa69c24bb0143bf4dd4d5fb54183f0c6f948d9f92",
            1: "182ae3122597640e6eb3017910add1b22cfab636b126b57685f6253c4d758f0f"
        }

        for gif_index, gif in enumerate(gifs):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as temp:
                temp.write(gif.getbuffer())
                print("NOTE - the result of this test can be visualized here: ", temp.name)
            gif_hash = hashlib.sha256(gif.getbuffer()).hexdigest()
            self.assertEqual(gif_hash, hash_reference[gif_index], True)


if __name__ == '__main__':
    unittest.main()
