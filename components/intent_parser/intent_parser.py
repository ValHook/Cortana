from datetime import datetime
from datetime import tzinfo
import re
import unidecode
import dateparser
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle

ACTIVITY_NAMES_BY_TYPE = {
    ActivityID.Type.LEVIATHAN:
        ['leviathan', 'calus'],
    ActivityID.Type.EATER_OF_WORLDS:
        ['dévoreur de mondes', 'dévoreur', 'argos', 'mondes'],
    ActivityID.Type.SPIRE_OF_STARS:
        ['flèche', 'flèche d\'étoiles', 'étoiles'],
    ActivityID.Type.CROWN_OF_SORROW:
        ['couronne', 'couronne du malheur'],
    ActivityID.Type.LAST_WISH:
        ['dernier voeu', 'dernier vœu', 'riven', 'voeu', 'vœu', ],
    ActivityID.Type.SCOURGE_OF_THE_PAST:
        ['fléau', 'fléau du passé'],
    ActivityID.Type.GARDEN_OF_SALVATION:
        ['jds', 'jardin', 'jardin du salut'],
    ActivityID.Type.VAULT_OF_GLASS:
        ['caveau de verre', 'caveau'],
    ActivityID.Type.CROPTAS_END:
        ['la chute de cropta', 'chute de cropta', 'cropta'],
    ActivityID.Type.THE_TAKEN_KING:
        ['la chute du roi', 'chute du roi', 'oryx', 'la chute d\'oryx'],
    ActivityID.Type.WRATH_OF_THE_MACHINE:
        ['la fureur mécanique', 'fureur mécanique', 'fureur', 'axis'],
}
ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.LEVIATHAN_PRESTIGE] = [
    name + " prestige" for name in ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.LEVIATHAN]]
ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.EATER_OF_WORLDS_PRESTIGE] = [
    name + " prestige" for name in ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.EATER_OF_WORLDS]]
ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.SPIRE_OF_STARS_PRESTIGE] = [
    name + " prestige" for name in ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.SPIRE_OF_STARS]]
ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.VAULT_OF_GLASS_PRESTIGE] = [
    name + " prestige" for name in ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.VAULT_OF_GLASS]]
ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.CROPTAS_END_PRESTIGE] = [
    name + " prestige" for name in ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.CROPTAS_END]]
ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.THE_TAKEN_KING_PRESTIGE] = [
    name + " prestige" for name in ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.THE_TAKEN_KING]]
ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.WRATH_OF_THE_MACHINE_PRESTIGE] = [
    name + " prestige" for name in ACTIVITY_NAMES_BY_TYPE[ActivityID.Type.WRATH_OF_THE_MACHINE]]


class Parser:
    """Parser for user input (intents)."""

    def __init__(self, message, api_bundle, now, locale):
        if not isinstance(message, str):
            raise ValueError("Message vide")
        if not isinstance(api_bundle, APIBundle) or len(api_bundle.stats_by_player) < 6:
            raise ValueError("API Bundle vide")
        if not isinstance(now, datetime):
            raise ValueError("Horloge non configurée")
        if not isinstance(now.tzinfo, tzinfo):
            raise ValueError("Fuseau horaire non configuré")
        if not isinstance(locale, str):
            raise ValueError("Locale non configurée")
        self.__message = message
        self.__api_bundle = api_bundle
        self.__now = now
        self.__locale = locale

    def parse_activity_type(self, initial_words):
        """
        Matches an activity type from the given word array.
        Returns (the best matching activity type, the rightmost unused words).
        Throws an exception in case of failure.
        """
        if len(initial_words) == 0:
            raise ValueError("Il manque le nom de l'activité")

        activities = ACTIVITY_NAMES_BY_TYPE.items()
        query = ""
        words = initial_words.copy()
        best_activity_so_far = None
        unused_words_for_best_activity_so_far = words.copy()
        while len(words) > 0:
            query += " " + words.pop(0)
            levensthein_by_activity = map(
                lambda a: (
                    a[0],
                    min([self.levensthein(query, name, '[^A-Za-z0-9+-]+') for name in a[1]])
                ),
                activities)
            levensthein_by_activity = list(levensthein_by_activity)
            levensthein_by_activity = sorted(
                levensthein_by_activity,
                key=lambda a: a[1]
            )
            (best_activity, best_levensthein) = levensthein_by_activity[0]

            if best_levensthein > 3 or best_levensthein > 0.3 * len(query):
                continue

            best_activity_so_far = best_activity
            unused_words_for_best_activity_so_far = words.copy()

        if not best_activity_so_far:
            raise ValueError(
                "Un nom d'activité aurait dû être présent à partir de \"" +
                " ".join(initial_words) +
                "\"")

        return best_activity_so_far, unused_words_for_best_activity_so_far

    def parse_datetime(self, initial_words):
        """
        Matches a datetime from the given word array.
        Returns (the best matching date time or None, with_time? bool, the rightmost unused words).
        Several formats are supported.
        """
        if len(initial_words) == 0:
            return None, None, []

        query = ""
        words = initial_words.copy()
        best_datetime_so_far = None
        unused_words_for_best_datetime_so_far = words.copy()
        with_time = True
        while len(words) > 0:
            query += " " + words.pop(0)
            # Dateparser is not very good at parsing times when the minutes are not specified.
            # Transform strings like 18h to 18h00.
            query = re.sub(r"(.*)([0-9]h)$", r"\g<1>\g<2>00", query)
            try:
                parsed_datetime = dateparser.parse(
                    query,
                    locales=[self.__locale],
                    settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE':self.__now}
                )
            except:
                # Dateparser can't deal with the case where the timezone is only present in either
                # the parsed query or the relative base.
                parsed_datetime = dateparser.parse(
                    query,
                    locales=[self.__locale],
                    settings={
                        'PREFER_DATES_FROM': 'future',
                        'RELATIVE_BASE': self.__now.replace(tzinfo=None)
                    }
                )
            if parsed_datetime is None:
                continue
            # Dateparser wrongly adds implicit times to strings like "aujourd'hui" and "demain"
            # Filter them out.
            if not re.search(r"[0-9]h", query):
                with_time = False
                parsed_datetime = parsed_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                with_time = True
            parsed_datetime = parsed_datetime.replace(tzinfo=self.__now.tzinfo)
            best_datetime_so_far = parsed_datetime
            unused_words_for_best_datetime_so_far = words.copy()

        return (
            best_datetime_so_far,
            with_time if best_datetime_so_far else None,
            unused_words_for_best_datetime_so_far
        )

    def parse_gamer_tag(self, initial_words):
        """
        Matches a gamer tag of the bundle from the given word array.
        Returns (best matching gamer tag or None, add? or remove bool, the rightmost unused words).
        Throws an exception in case of failure.
        """
        if len(initial_words) == 0:
            raise ValueError("Il manque un gamer tag")

        query = ""
        words = initial_words.copy()
        error = ValueError(
            "Un gamer tag aurait dû être présent à partir de \"" +
            " ".join(initial_words) +
            "\""
        )
        is_add = words[0][0] != '-'
        while len(words) > 0:
            query += " " + words.pop(0)
            gamer_tags = self.__api_bundle.stats_by_player.keys()
            gamer_tags = map(lambda g: (g, self.levensthein(query, g, '[^A-Za-z]+')), gamer_tags)
            gamer_tags = sorted(gamer_tags, key=lambda g: g[1])
            best_gamer_tag = gamer_tags[0][0]
            best_levensthein = gamer_tags[0][1]

            if best_levensthein > 2 or best_levensthein > 0.3 * len(query):
                continue
            second_best_gamer_tag = gamer_tags[1][0]
            second_best_levensthein = gamer_tags[1][1]
            if second_best_levensthein == best_levensthein:
                error = ValueError(
                    "Hésitation de gamer tag entre " +
                    best_gamer_tag +
                    " et " +
                    second_best_gamer_tag +
                    " à partir de \"" +
                    " ".join(initial_words) +
                    "\""
                )
                continue
            return best_gamer_tag, is_add

        raise error

    def levensthein(self, str_a, str_b, filter_out_regex):
        """
        Returns the Levensthein distance between str_a and str_b after applying filter_out_regex.
        """
        str_a = unidecode.unidecode(str_a)
        str_b = unidecode.unidecode(str_b)
        str_a = str_a.strip()
        str_b = str_b.strip()
        str_a = str_a.lower()
        str_b = str_b.lower()
        str_a = re.sub(filter_out_regex, '', str_a)
        str_b = re.sub(filter_out_regex, '', str_b)
        if len(str_a) > len(str_b):
            str_a, str_b = str_b, str_a
        distances = range(len(str_a) + 1)
        for i2, c2 in enumerate(str_b):
            distances_ = [i2 + 1]
            for i1, c1 in enumerate(str_a):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(
                        1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]
