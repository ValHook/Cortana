from datetime import datetime
from pathlib import Path
import re
import unittest
from dateutil import tz
from components.intent_parser import intent_parser
from components.converters.when import to_when
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle
from protos.intent_pb2 import Intent
from protos.rated_player_pb2 import RatedPlayer

SUT_BUNDLE = APIBundle()
SUT_BUNDLE.ParseFromString(Path('components/intent_parser/test_assets/api_bundle.dat').read_bytes())
SUT_TIMEZONE = tz.gettz('Europe/Paris')
SUT_NOW = datetime(2020, 8, 12, 18, 15, 0, 0, SUT_TIMEZONE)
SUT_LOCALE = 'fr'


class ParserTest(unittest.TestCase):
    """Test class for the intent parser."""

    def setUp(self):
        """Sets up a basic sut."""
        self.sut = intent_parser.Parser(SUT_LOCALE)

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
            "mercredi": (datetime(2020, 8, 19), False),
            "17/08": (datetime(2020, 8, 17), False),
            "demain 20h": (datetime(2020, 8, 13, 20, 0, 0, 0, SUT_TIMEZONE), True),
            "aujourd'hui": (datetime(2020, 8, 12), False),
            "samedi 18h": (datetime(2020, 8, 15, 18, 0, 0, 0, SUT_TIMEZONE), True),
            "vendredi": (datetime(2020, 8, 14), False),
            "16/08 21h30": (datetime(2020, 8, 16, 21, 30, 0, 0, SUT_TIMEZONE), True),
            "1/9": (datetime(2020, 9, 1), False),
            "02/10": (datetime(2020, 10, 2), False),
            "25/08 21h": (datetime(2020, 8, 25, 21, 0, 0, 0, SUT_TIMEZONE), True),
            "6/1 17h45": (datetime(2021, 1, 6, 17, 45, 0, 0, SUT_TIMEZONE), True),
            "9/8": (datetime(2020, 8, 9), False),
            "9/8 13h": (datetime(2020, 8, 9, 13, 0, 0, 0, SUT_TIMEZONE), True),
            "9/8/2021": (datetime(2021, 8, 9), False),
            "9/8/2021 13h": (datetime(2021, 8, 9, 13, 0, 0, 0, SUT_TIMEZONE), True),
        }
        noises = ["", "17hShadow", "10_fooBar", "croptus", "Franstuk Walnut Oby1Chick 25/07",
                  "+Cosa58 25/07", "-SuperFayaChonch", "+emile -Omega Gips"]
        for (date_str, (date_expectation, with_time_expectation)) in expectations.items():
            for noise in noises:
                query_array = re.split(r"\s+", date_str)
                noise_array = list(filter(len, re.split(r"\s+", noise)))
                query_and_noise_array = query_array + noise_array
                debug_str = " ".join(query_and_noise_array) + " => " + date_expectation.isoformat()
                result = self.sut.parse_datetime(query_and_noise_array, SUT_NOW)
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
            self.assertRaises(ValueError, self.sut.parse_datetime, noise_array, SUT_NOW)

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
                        result = self.sut.parse_gamer_tag(candidate_and_noise_array, SUT_BUNDLE)
                        self.assertEqual(expected, result[0], debug_str)
                        self.assertEqual(is_add, result[1], debug_str)

        for noise in noises:
            noise_array = list(filter(len, re.split(r"\s+", noise)))
            self.assertRaises(ValueError, self.sut.parse_gamer_tag, noise_array, SUT_BUNDLE)

    def test_parse_help_intent(self):
        """Verifies help intents can properly be parsed."""
        intent = self.sut.parse("!raid help", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.global_intent.help = True
        self.assertEqual(intent, expectation)

    def test_parse_clearall_intent(self):
        """Verifies clear all intents can properly be parsed."""
        intent = self.sut.parse("!raid clearall", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.global_intent.clear_all = True
        self.assertEqual(intent, expectation)

    def test_parse_clearpast_intent(self):
        """Verifies clear past intents can properly be parsed."""
        intent = self.sut.parse("!raid clearpast", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.global_intent.clear_past = True
        self.assertEqual(intent, expectation)

    def test_parse_sync_intent(self):
        """Verifies bundle sync intents can properly be parsed."""
        intent = self.sut.parse("!raid sync", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.global_intent.sync_bundle = True
        self.assertEqual(intent, expectation)

    def test_parse_lastsync_intent(self):
        """Verifies last sync get intents can properly be parsed."""
        intent = self.sut.parse("!raid lastsync", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.global_intent.get_last_bundle_sync_datetime = True
        self.assertEqual(intent, expectation)

    def test_parse_images_intent(self):
        """Verifies image generation intents can properly be parsed."""
        intent = self.sut.parse("!raid images", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.global_intent.generate_images = True
        self.assertEqual(intent, expectation)

    def test_parse_datetime_intent(self):
        """Verifies date time update intents can properly be parsed."""
        intent = self.sut.parse("!raid date fureur 25/08 19h", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.WRATH_OF_THE_MACHINE
        new_date_time = datetime(2020, 8, 25, hour=19, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date caveau vendredi", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.VAULT_OF_GLASS
        new_date_time = datetime(2020, 8, 14)
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date fleau samedi samedi 19h", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.SCOURGE_OF_THE_PAST
        old_date_time = datetime(2020, 8, 15)
        new_date_time = datetime(2020, 8, 15, hour=19, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date devoreur demain 21h 30/08 14h30", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.EATER_OF_WORLDS
        old_date_time = datetime(2020, 8, 13, hour=21, tzinfo=SUT_TIMEZONE)
        new_date_time = datetime(2020, 8, 30, hour=14, minute=30, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date devoreur hier demain", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.EATER_OF_WORLDS
        old_date_time = datetime(2020, 8, 11)
        new_date_time = datetime(2020, 8, 13)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date devoreur hier demain 22h05", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.EATER_OF_WORLDS
        old_date_time = datetime(2020, 8, 11)
        new_date_time = datetime(2020, 8, 13, hour=22, minute=5, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date jardin du salut 22/08 23/08", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.GARDEN_OF_SALVATION
        old_date_time = datetime(2020, 8, 22)
        new_date_time = datetime(2020, 8, 23)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date dernier voeu 20/08 16h45 19/08", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LAST_WISH
        old_date_time = datetime(2020, 8, 20, hour=16, minute=45, tzinfo=SUT_TIMEZONE)
        new_date_time = datetime(2020, 8, 19)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid date dernier voeu 20/08 16h45 19/08 21h30",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LAST_WISH
        old_date_time = datetime(2020, 8, 20, hour=16, minute=45, tzinfo=SUT_TIMEZONE)
        new_date_time = datetime(2020, 8, 19, hour=21, minute=30, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date dernier voeu vendredi vendredi", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LAST_WISH
        old_date_time = datetime(2020, 8, 14)
        new_date_time = datetime(2020, 8, 14)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date dernier voeu 20/8 20/8 16h", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LAST_WISH
        old_date_time = datetime(2020, 8, 20)
        new_date_time = datetime(2020, 8, 20, hour=16, minute=0, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid date calus 9/8 9/8 23h", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LEVIATHAN
        old_date_time = datetime(2020, 8, 9)
        new_date_time = datetime(2020, 8, 9, hour=23, minute=0, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(old_date_time))
        expectation.activity_intent.update_when.CopyFrom(to_when(new_date_time))
        self.assertEqual(intent, expectation)

    def test_parse_milestone_intent(self):
        """Verifies milestone intents can properly be parsed."""
        intent = self.sut.parse("!raid milestone calus prestige save au boss", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LEVIATHAN_PRESTIGE
        expectation.activity_intent.set_milestone = "Save au boss"
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid milestone couronne 31/8 21h45 reporté", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.CROWN_OF_SORROW
        date_time = datetime(2020, 8, 31, hour=21, minute=45, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        expectation.activity_intent.set_milestone = "Reporté"
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid milestone dernier voeu demain save étape 2",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LAST_WISH
        date_time = datetime(2020, 8, 13)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        expectation.activity_intent.set_milestone = "Save étape 2"
        self.assertEqual(intent, expectation)

    def test_parse_finish_intent(self):
        """Verifies finish intents can properly be parsed."""
        intent = self.sut.parse("!raid finish jds", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.GARDEN_OF_SALVATION
        expectation.activity_intent.mark_finished = True
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid finish flèche 5/9 18h", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.SPIRE_OF_STARS
        date_time = datetime(2020, 9, 5, hour=18, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        expectation.activity_intent.mark_finished = True
        self.assertEqual(intent, expectation)

    def test_parse_clear_intent(self):
        """Verifies clear intents can properly be parsed."""
        intent = self.sut.parse("!raid clear couronne", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.CROWN_OF_SORROW
        expectation.activity_intent.clear = True
        self.assertEqual(intent, expectation)

        intent = self.sut.parse("!raid clear fleau 12/9 21h30", SUT_BUNDLE, SUT_NOW)
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.SCOURGE_OF_THE_PAST
        date_time = datetime(2020, 9, 12, hour=21, minute=30, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        expectation.activity_intent.clear = True
        self.assertEqual(intent, expectation)

    def test_parse_create_squad_intent(self):
        """Verifies create squad intents with main players can properly be parsed."""
        intent = self.sut.parse(
            "!raid jds cosa croptus Walnut Waffle darklight hartog Franstuk",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.GARDEN_OF_SALVATION
        player = RatedPlayer()
        player.gamer_tag = "Cosa58"
        player.rating = RatedPlayer.Rating.INTERMEDIATE
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "croptus"
        player.rating = RatedPlayer.Rating.INTERMEDIATE
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Walnut Waffle"
        player.rating = RatedPlayer.Rating.INTERMEDIATE
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "dark0l1ght"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Hartog31"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Franstuk"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid fleau demain 19h Oby1Chik live x gamling",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.SCOURGE_OF_THE_PAST
        date_time = datetime(2020, 8, 13, hour=19, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        player = RatedPlayer()
        player.gamer_tag = "Oby1Chick"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "LiVe x GamIing"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid couronne 15/08 snipro pistache espita Jezebell NaughtySOft",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.CROWN_OF_SORROW
        date_time = datetime(2020, 8, 15)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        player = RatedPlayer()
        player.gamer_tag = "snippro34"
        player.rating = RatedPlayer.Rating.INTERMEDIATE
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "pistache espita"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Jezehbell"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "NaughtySoft"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid dernier veu dimanche 14h45 affectevil xxmariexx duality cobra FranckRabbit",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LAST_WISH
        date_time = datetime(2020, 8, 16, hour=14, minute=45, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        player = RatedPlayer()
        player.gamer_tag = "affectevil"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "xXmarie91Xx"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Duality Cobra"
        player.rating = RatedPlayer.Rating.INTERMEDIATE
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "FranckRabbit"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.added.players.append(player)
        self.assertEqual(intent, expectation)

    def test_parse_update_squad_intent(self):
        """Verifies update squad intents with main players can properly be parsed."""
        intent = self.sut.parse(
            "!raid vœu +cosa -croptus -klaexy +darklight -hartog +Franstuk -ObyChick +kyzerjo",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LAST_WISH
        player = RatedPlayer()
        player.gamer_tag = "Cosa58"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "croptus"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        player.gamer_tag = "KLaeXy"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        player.gamer_tag = "dark0l1ght"
        player.rating = RatedPlayer.Rating.INTERMEDIATE
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Hartog31"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        player.gamer_tag = "Franstuk"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Oby1Chick"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        player.gamer_tag = "kyzerjo88"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.added.players.append(player)
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid calus prestige demain 19h +Oby1Chik -live x gamling",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LEVIATHAN_PRESTIGE
        date_time = datetime(2020, 8, 13, hour=19, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        player = RatedPlayer()
        player.gamer_tag = "Oby1Chick"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "LiVe x GamIing"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid flèche prestige 30/08 -snipro -pistache espita -Jezebell +NaughtySOft -cosa",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.SPIRE_OF_STARS_PRESTIGE
        date_time = datetime(2020, 8, 30)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        player = RatedPlayer()
        player.gamer_tag = "snippro34"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        player.gamer_tag = "pistache espita"
        player.rating = RatedPlayer.Rating.INTERMEDIATE
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        player.gamer_tag = "Jezehbell"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        player.gamer_tag = "NaughtySoft"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Cosa58"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid dévoreur dimanche 20h45 SuperFayaChonch +xxmariexx -duality cobra -carnage",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.EATER_OF_WORLDS
        date_time = datetime(2020, 8, 16, hour=20, minute=45, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        player = RatedPlayer()
        player.gamer_tag = "SuperFayaChonch"
        player.rating = RatedPlayer.Rating.INTERMEDIATE
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "xXmarie91Xx"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.players.append(player)
        player.gamer_tag = "Duality Cobra"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        player.gamer_tag = "CarNaGe4720"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.players.append(player)
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid backup calus prestige samedi 21h30 affectevil bab x waza",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LEVIATHAN_PRESTIGE
        date_time = datetime(2020, 8, 15, hour=21, minute=30, tzinfo=SUT_TIMEZONE)
        expectation.activity_intent.activity_id.when.CopyFrom(to_when(date_time))
        player = RatedPlayer()
        player.gamer_tag = "affectevil"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.substitutes.append(player)
        player.gamer_tag = "BAB x WaZZa"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.substitutes.append(player)
        self.assertEqual(intent, expectation)

        intent = self.sut.parse(
            "!raid backup vœu +darklucifel -croptus -strikers frwyx -hartog Franstuk +kyzerjo",
            SUT_BUNDLE,
            SUT_NOW
        )
        expectation = Intent()
        expectation.activity_intent.activity_id.type = ActivityID.Type.LAST_WISH
        player = RatedPlayer()
        player.gamer_tag = "DarkLucifiel77"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.substitutes.append(player)
        player.gamer_tag = "croptus"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.substitutes.append(player)
        player.gamer_tag = "Striikers"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.removed.substitutes.append(player)
        player.gamer_tag = "frwyx"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.substitutes.append(player)
        player.gamer_tag = "Hartog31"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.removed.substitutes.append(player)
        player.gamer_tag = "Franstuk"
        player.rating = RatedPlayer.Rating.BEGINNER
        expectation.activity_intent.upsert_squad.added.substitutes.append(player)
        player.gamer_tag = "kyzerjo88"
        player.rating = RatedPlayer.Rating.EXPERIENCED
        expectation.activity_intent.upsert_squad.added.substitutes.append(player)
        self.assertEqual(intent, expectation)


if __name__ == '__main__':
    unittest.main()
