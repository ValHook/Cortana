import unittest
from components.img import generator
from protos.planning_pb2 import Planning
from protos.activity_id_pb2 import ActivityID

class GeneratorTester(unittest.TestCase):
    """Test class for the image generator."""

    def test_planning(self):
        p = Planning()
        a = p.activities.add()
        a.id.type = ActivityID.Type.CALUS
        a.id.timestamp_seconds = 1594763746
        (a.squad.players.add()).gamer_tag = "Cosa58"
        (a.squad.players.add()).gamer_tag = "Walnut Waffle"
        (a.squad.players.add()).gamer_tag = "Oby1Chick"
        (a.squad.players.add()).gamer_tag = "Franstuck"
        (a.squad.players.add()).gamer_tag = "Dark0l1ght"
        (a.squad.players.add()).gamer_tag = "SuperFayaChonch"
        (a.squad.substitutes.add()).gamer_tag = "croptus7490"
        (a.squad.substitutes.add()).gamer_tag = "Affectevil"
        gen = generator.Generator(p)
        gen.generate_image()
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()