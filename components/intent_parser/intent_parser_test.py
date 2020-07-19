import re
import unittest
from components.intent_parser import intent_parser
from protos.activity_id_pb2 import ActivityID


class ParserTest(unittest.TestCase):
    """Test class for the intent parser."""

    def test_initializer(self):
        """Verifies the initializer works as expected."""
        sut = intent_parser.Parser('foo')
        self.assertEqual(sut.message, 'foo')
        self.assertRaises(ValueError, intent_parser.Parser, None)
        self.assertRaises(ValueError, intent_parser.Parser, 1337)

    def test_parse_activity_type(self):
        """Verifies the activity-type sub-parser."""
        sut = intent_parser.Parser('query does not matter')
        expectations = {
            ActivityID.Type.LEVIATHAN:
                ['leviathan', 'calus', 'ckalus', 'leviatan', 'leviath', 'caluss'],
            ActivityID.Type.LEVIATHAN_PRESTIGE:
                ['leviathan prestige', 'calus prestige', 'cal prestige', 'leviath prestig'],
            ActivityID.Type.EATER_OF_WORLDS:
                ['dévoreur de mondes', 'dévoreur', 'argos', 'dévore', 'argo', 'monde'],
            ActivityID.Type.EATER_OF_WORLDS_PRESTIGE:
                ['dévoreur de mondes prestige', 'dévoreur prestige', 'argos prestige',
                 'dévor prestige'],
            ActivityID.Type.SPIRE_OF_STARS:
                ['flèche', 'flèche d\'étoiles', 'fleche', 'flech', 'etoile', 'flechedetoiles',
                 'detoiles'],
            ActivityID.Type.SPIRE_OF_STARS_PRESTIGE:
                ['flèche prestige', 'flèche d\'étoiles prestige', 'fleche prestige',
                 'etoile prestige', 'flèchedetoiles prestige'],
            ActivityID.Type.CROWN_OF_SORROW:
                ['couronne', 'couronne du malheur', 'couronnedumalheur', 'kouronn'],
            ActivityID.Type.LAST_WISH:
                ['dernier voeu', 'dernier vœu', 'riven', 'voeu', 'vœu', 'rive', 'rivem'],
            ActivityID.Type.SCOURGE_OF_THE_PAST:
                ['fléau', 'fléau du passé', 'fleau', 'fleaudupasse', 'fleaupasse'],
            ActivityID.Type.GARDEN_OF_SALVATION:
                ['jds', 'jardin', 'jardin du salut', 'gds', 'jardim', 'jardindusalu'],
            ActivityID.Type.VAULT_OF_GLASS:
                ['caveau', 'caveauverre', 'caveau de verre'],
            ActivityID.Type.VAULT_OF_GLASS_PRESTIGE:
                ['caveauprestige'],
            ActivityID.Type.CROPTAS_END:
                ['cropta', 'chutecropta', 'cropto'],
            ActivityID.Type.CROPTAS_END_PRESTIGE:
                ['cropta prestige', 'crotpa prestige', 'cropto presti'],
            ActivityID.Type.THE_TAKEN_KING:
                ['oryx', 'chuteroi', 'chuteoryx', 'orix'],
            ActivityID.Type.THE_TAKEN_KING_PRESTIGE:
                ['oryx prestige', 'orix presti', 'oryxprest', 'chuteroiprestige'],
            ActivityID.Type.WRATH_OF_THE_MACHINE:
                ['fureur', 'axis', 'furer', 'fureurmecanique', 'axos'],
            ActivityID.Type.WRATH_OF_THE_MACHINE_PRESTIGE:
                ['axis prestige', 'fureur prest', 'axs prestig', 'axos prestige'],
        }
        noises = ["", "croptus", "Franstuk Walnut Oby1Chick 25/07",
                  "+Cosa58 25/07", "-SuperFayaChonch", "+emile -Omega Gips"]
        for (activity_type, candidates) in expectations.items():
            for candidate in candidates:
                for noise in noises:
                    candidate_array = re.split(r"\s+", candidate)
                    noise_array = list(filter(len, re.split(r"\s+", noise)))
                    candidate_and_noise_array = candidate_array + noise_array
                    debug_str = " ".join(
                        candidate_and_noise_array) + " => " + ActivityID.Type.Name(activity_type)
                    result = sut.parse_activity_type(candidate_and_noise_array)
                    self.assertEqual(activity_type, result[0], debug_str)
                    self.assertEqual(noise_array, result[1], debug_str)

        noises = [
            "backup",
            "save finish",
            "info",
            "foo",
            "noise",
            "Walnut Waffle",
            "BAB",
            "Dark01light",
            "raid",
            ""]
        for noise in noises:
            noise_array = list(filter(len, re.split(r"\s+", noise)))
            self.assertRaises(ValueError, sut.parse_activity_type, noise_array)


if __name__ == '__main__':
    unittest.main()
