from datetime import datetime
from pathlib import Path
import re
import unittest
from dateutil import tz
from components.intent_parser import intent_parser
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle

SUT_QUERY = 'A query that does not matter'
SUT_BUNDLE = APIBundle()
SUT_BUNDLE.ParseFromString(Path('components/intent_parser/test_assets/api_bundle.dat').read_bytes())
SUT_TIMEZONE = tz.gettz('Europe/Paris')
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
                ['leviathan prestige', 'calus prestige', 'cal prestige', 'leviath prestige'],
            ActivityID.Type.EATER_OF_WORLDS:
                ['dévoreur de mondes', 'dévoreur', 'argos', 'devore', 'argo', 'monde'],
            ActivityID.Type.EATER_OF_WORLDS_PRESTIGE:
                ['dévoreur de mondes prestige', 'dévoreur prestige', 'argos prestige',
                 'devore prestige'],
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
                ['fléau', 'fléau du passé', 'fleau', 'fleaudupasse', 'fleaupasse', 'fleo'],
            ActivityID.Type.GARDEN_OF_SALVATION:
                ['jds', 'jardin', 'jardin du salut', 'gds', 'jardim', 'jardindusalu'],
            ActivityID.Type.VAULT_OF_GLASS:
                ['caveau', 'caveauverre', 'caveau de verre'],
            ActivityID.Type.VAULT_OF_GLASS_PRESTIGE:
                ['caveauprestige'],
            ActivityID.Type.CROPTAS_END:
                ['cropta', 'chutecropta', 'cropto'],
            ActivityID.Type.CROPTAS_END_PRESTIGE:
                ['cropta prestige', 'crotpa prestige', 'cropto restige'],
            ActivityID.Type.THE_TAKEN_KING:
                ['oryx', 'chuteroi', 'chuteoryx', 'orix', 'chute doryx'],
            ActivityID.Type.THE_TAKEN_KING_PRESTIGE:
                ['oryx prestige', 'orx prestige', 'oryxpresti', 'chuteroiprestige'],
            ActivityID.Type.WRATH_OF_THE_MACHINE:
                ['fureur', 'axis', 'furer', 'fureurmecanique', 'axos'],
            ActivityID.Type.WRATH_OF_THE_MACHINE_PRESTIGE:
                ['axis prestige', 'furer prestige', 'axs prestig', 'axos prestige'],
        }
        noises = ["", "croptus", "Franstuk Walnut Oby1Chick 25/07", "5/9",
                  "+Cosa58 25/07", "-SuperFayaChonch", "+emile -Omega Gips", "22/08 18h"]
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
            "12/08 21h",
            "5/09",
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
            noise_array = re.split(r"\s+", noise)
            self.assertRaises(ValueError, self.sut.parse_datetime, noise_array)

    def test_parse_gamer_tag(self):
        """Verifies the gamer tag sub-parser."""
        expectations = {
            'Walnut Waffle': ['WalnutWaffle', 'Wolnut Waffl', 'Walnut Waffle'],
            'Cosa58': ['cosa', 'cosa58', 'COSA', 'CoSa558', 'Kosa'],
            'dark0l1ght': ['DarkLight', 'dark01lght'],
            'snippro34': ['snippro', 'Snipro34', 'snippro34'],
            'croptus': ['croptus7490', 'croptus', 'KROptUs'],
        }
        noises = ['', 'backup', 'raid', 'jds', 'backup', '+DenisSurvivor', '-Foobar', '25/07']
        prefixes = ['', '+', '-']
        for (expected, candidates) in expectations.items():
            for prefix in prefixes:
                for candidate in candidates:
                    candidate = prefix + candidate
                    candidate_array = re.split(r"\s+", candidate)
                    is_add = prefix != '-'
                    for noise in noises:
                        noise_array = list(filter(len, re.split(r"\s+", noise)))
                        candidate_and_noise_array = candidate_array + noise_array
                        debug_str = " ".join(candidate_and_noise_array) + \
                            " => " + expected + "(is_add: " + str(is_add) + ")"
                        result = self.sut.parse_gamer_tag(candidate_and_noise_array)
                        self.assertEqual(expected, result[0], debug_str)
                        self.assertEqual(is_add, result[1], debug_str)

        for noise in noises:
            noise_array = list(filter(len, re.split(r"\s+", noise)))
            self.assertRaises(ValueError, self.sut.parse_gamer_tag, noise_array)

    def test_parse_images_intent(self):
        """Verifies image generation intents can properly be parsed."""
        sut1 = intent_parser.Parser("!raid images", SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent1 = sut1.parse()
        print(intent1)

    def test_parse_datetime_intent(self):
        """Verifies date time update intents can properly be parsed."""
        sut1 = intent_parser.Parser("!raid date fureur 25/08 19h", SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent1 = sut1.parse()
        print(intent1)
        sut2 = intent_parser.Parser("!raid date caveau vendredi", SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent2 = sut2.parse()
        print(intent2)
        sut3 = intent_parser.Parser("!raid date fleau samedi samedi 19h",
                                    SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent3 = sut3.parse()
        print(intent3)
        sut4 = intent_parser.Parser("!raid date devoreur demain 21h 30/08 14h30",
                                    SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent4 = sut4.parse()
        print(intent4)
        sut5 = intent_parser.Parser("!raid date jardin du salut 22/08 23/08",
                                    SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent5 = sut5.parse()
        print(intent5)
        sut6 = intent_parser.Parser("!raid date dernier voeu 20/08 16h45 19/08",
                                    SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent6 = sut6.parse()
        print(intent6)

    def test_parse_milestone_intent(self):
        """Verifies milestone intents can properly be parsed."""
        sut1 = intent_parser.Parser("!raid milestone calus prestige save au boss",
                                    SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent1 = sut1.parse()
        print(intent1)
        sut2 = intent_parser.Parser("!raid milestone couronne 31/8 21h45 reporté",
                                    SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent2 = sut2.parse()
        print(intent2)
        sut3 = intent_parser.Parser("!raid milestone dernier voeu demain save étape 2",
                                    SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent3 = sut3.parse()
        print(intent3)

    def test_parse_finish_intent(self):
        """Verifies finish intents can properly be parsed."""
        sut1 = intent_parser.Parser("!raid finish jds", SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent1 = sut1.parse()
        print(intent1)
        sut2 = intent_parser.Parser("!raid finish flèche 5/9 18h", SUT_BUNDLE, SUT_NOW, SUT_LOCALE)
        intent2 = sut2.parse()
        print(intent2)

    def test_parse_create_squad_intent(self):
        """Verifies create squad intents with main players can properly be parsed."""
        sut1 = intent_parser.Parser(
            "!raid jds cosa croptus Walnut Waffle darklight hartog Franstuk",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent1 = sut1.parse()
        print(intent1)
        sut2 = intent_parser.Parser(
            "!raid fleau demain 19h Oby1Chik live x gamling",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent2 = sut2.parse()
        print(intent2)
        sut3 = intent_parser.Parser(
            "!raid couronne 15/08 snipro pistache espita Jezebell NaughtySOft",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent3 = sut3.parse()
        print(intent3)
        sut4 = intent_parser.Parser(
            "!raid dernier veu dimanche 14h45 affectevil xxmariexx duality cobra FranckRabbit",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent4 = sut4.parse()
        print(intent4)

    def test_parse_update_squad_intent(self):
        """Verifies update squad intents with main players can properly be parsed."""
        sut1 = intent_parser.Parser(
            "!raid vœu +cosa -croptus -klaexy +darklight -hartog +Franstuk -ObyChick +kyzerjo",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent1 = sut1.parse()
        print(intent1)
        sut2 = intent_parser.Parser(
            "!raid calus prestige demain 19h +Oby1Chik -live x gamling",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent2 = sut2.parse()
        print(intent2)
        sut3 = intent_parser.Parser(
            "!raid flèche prestige 30/08 -snipro -pistache espita -Jezebell +NaughtySOft -cosa",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent3 = sut3.parse()
        print(intent3)
        sut4 = intent_parser.Parser(
            "!raid dévoreur dimanche 20h45 SuperFayaChonch +xxmariexx -duality cobra -carnage",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent4 = sut4.parse()
        print(intent4)
        sut5 = intent_parser.Parser(
            "!raid backup calus prestige samedi 21h30 affectevil bab x waza",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent5 = sut5.parse()
        print(intent5)
        sut6 = intent_parser.Parser(
            "!raid backup vœu +darklucifel -croptus -strikers frwyx -hartog Franstuk +kyzerjo",
            SUT_BUNDLE, SUT_NOW, SUT_LOCALE
        )
        intent6 = sut6.parse()
        print(intent6)


if __name__ == '__main__':
    unittest.main()
