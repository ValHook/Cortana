from datetime import datetime
import re
import unittest
from babel.dates import get_timezone
from components.intent_parser import intent_parser
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle

SUT_QUERY = 'A query that does not matter'
SUT_BUNDLE = APIBundle()
SUT_TIMEZONE = get_timezone('Europe/Paris')
SUT_NOW = datetime(2020, 8, 12, 18, 15, 0, 0, SUT_TIMEZONE)
SUT_LOCALE = 'fr'

class ParserTest(unittest.TestCase):
    """Test class for the intent parser."""

    def setUp(self):
        """Sets up a basic sut."""
        self.sut = intent_parser.Parser(SUT_QUERY, SUT_BUNDLE, SUT_NOW, SUT_LOCALE)

    def test_parse_activity_type(self):
        """Verifies the activity-type sub-parser."""
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
                    result = self.sut.parse_activity_type(candidate_and_noise_array)
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
            self.assertRaises(ValueError, self.sut.parse_activity_type, noise_array)

    def test_parse_datetime(self):
        """Verifies the date-time sub-parser."""
        expectations = {
            "mardi 21h15": (datetime(2020, 8, 18, 21, 15, 0, 0, SUT_TIMEZONE), True),
            "mercredi 12h00": (datetime(2020, 8, 19, 12, 0, 0, 0, SUT_TIMEZONE), True),
            "mercredi 22h00": (datetime(2020, 8, 19, 22, 0, 0, 0, SUT_TIMEZONE), True),
            "mercredi": (datetime(2020, 8, 19, 0, 0, 0, 0, SUT_TIMEZONE), False),
            "17/08": (datetime(2020, 8, 17, 0, 0, 0, 0, SUT_TIMEZONE), False),
            "demain 20h": (datetime(2020, 8, 13, 20, 0, 0, 0, SUT_TIMEZONE), True),
            "aujourd'hui": (datetime(2020, 8, 12, 0, 0, 0, 0, SUT_TIMEZONE), False),
            "samedi 18h": (datetime(2020, 8, 15, 18, 0, 0, 0, SUT_TIMEZONE), True),
            "vendredi": (datetime(2020, 8, 14, 0, 0, 0, 0, SUT_TIMEZONE), False),
            "16/08 21h30": (datetime(2020, 8, 16, 21, 30, 0, 0, SUT_TIMEZONE), True),
            "1/9": (datetime(2020, 9, 1, 0, 0, 0, 0, SUT_TIMEZONE), False),
            "02/10": (datetime(2020, 10, 2, 0, 0, 0, 0, SUT_TIMEZONE), False),
            "25/08 21h": (datetime(2020, 8, 25, 21, 0, 0, 0, SUT_TIMEZONE), True),
            "6/1 17h45": (datetime(2021, 1, 6, 17, 45, 0, 0, SUT_TIMEZONE), True),
        }
        noises = ["", "17hShadow", "10_fooBar", "croptus", "Franstuk Walnut Oby1Chick 25/07",
                  "+Cosa58 25/07", "-SuperFayaChonch", "+emile -Omega Gips"]
        for (date_str, (date_expectation, with_time_expectation)) in expectations.items():
            for noise in noises:
                query_array = re.split(r"\s+", date_str)
                noise_array = list(filter(len, re.split(r"\s+", noise)))
                query_and_noise_array = query_array + noise_array
                debug_str = " ".join(query_and_noise_array) + " => " + date_expectation.isoformat()
                result = self.sut.parse_datetime(query_and_noise_array)
                self.assertEqual(date_expectation, result[0], debug_str)
                self.assertEqual(with_time_expectation, result[1], debug_str)
                self.assertEqual(noise_array, result[2], debug_str)


if __name__ == '__main__':
    unittest.main()
