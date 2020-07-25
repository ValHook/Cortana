from datetime import datetime
from datetime import tzinfo
import re
import unidecode
import dateparser
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle
from protos.intent_pb2 import Intent
from protos.rated_player_pb2 import RatedPlayer
from protos.squad_pb2 import Squad

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
        ['dernier voeu', 'dernier vœu', 'riven', 'voeu', 'vœu'],
    ActivityID.Type.SCOURGE_OF_THE_PAST:
        ['fléau', 'fléau du passé'],
    ActivityID.Type.GARDEN_OF_SALVATION:
        ['jds', 'jardin', 'jardin du salut'],
    ActivityID.Type.VAULT_OF_GLASS:
        ['caveau de verre', 'caveau'],
    ActivityID.Type.CROPTAS_END:
        ['la chute de cropta', 'chute de cropta', 'cropta'],
    ActivityID.Type.THE_TAKEN_KING:
        ['la chute du roi', 'chute du roi', 'oryx', 'la chute d\'oryx', 'chute d\'oryx'],
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

INTERMEDIATE_MIN_COMPLETIONS = 6
EXPERIENCED_MIN_COMPLETIONS = 12

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

    def parse(self):
        """
        Parser entry point. Returns an intent if the message is a bot intent or None if not.
        i.e Messages starting with !raid are treated as intents. The rest are not.
        Raises an error if the message is an intent but ill-formed.
        """
        words = re.split(r"\s+", self.__message)
        next_word = words.pop(0)
        if next_word != '!raid':
            return None
        next_word = words.pop(0)
        if next_word == "images":
            return self.parse_images_intent(words)
        if next_word == "date":
            return self.parse_update_datetime_intent(words)
        if next_word == "milestone":
            return self.parse_update_milestone_intent(words)
        if next_word == "finish":
            return self.parse_finish_intent(words)
        if next_word == "backup":
            return self.parse_upsert_squad_intent(words, True)
        return self.parse_upsert_squad_intent([next_word] + words, False)

    def parse_images_intent(self, initial_words):
        """Returns a generate images intent or raises an error."""
        self.assert_words_empty(initial_words)
        intent = Intent()
        intent.generate_images = True
        return intent

    def parse_update_datetime_intent(self, initial_words):
        """Returns a date time update intent or raises an error."""
        (activity_type, words) = self.parse_activity_type(initial_words)
        (old_date_time, _, words) = self.parse_datetime(words)
        try:
            (new_date_time, _, words) = self.parse_datetime(words)
        except:
            new_date_time = old_date_time
            old_date_time = None
        self.assert_words_empty(words)
        intent = Intent()
        intent.activity_id.type = activity_type
        intent.activity_id.timestamp_seconds = self.timestamp(old_date_time)
        intent.update_timestamp_seconds = self.timestamp(new_date_time)
        return intent

    def parse_update_milestone_intent(self, initial_words):
        """Returns a milestone update intent or raises an error."""
        (activity_type, words) = self.parse_activity_type(initial_words)
        date_time = None
        try:
            (date_time, _, words) = self.parse_datetime(words)
        except:
            pass
        intent = Intent()
        intent.activity_id.type = activity_type
        intent.activity_id.timestamp_seconds = self.timestamp(date_time)
        if len(words) == 0:
            raise ValueError("Il manque le nom de la milestone")
        intent.set_milestone = " ".join(words).capitalize()
        return intent

    def parse_finish_intent(self, initial_words):
        """Returns a finish intent or raises an error."""
        (activity_type, words) = self.parse_activity_type(initial_words)
        date_time = None
        try:
            (date_time, _, words) = self.parse_datetime(words)
        except:
            pass
        intent = Intent()
        intent.activity_id.type = activity_type
        intent.activity_id.timestamp_seconds = self.timestamp(date_time)
        self.assert_words_empty(words)
        intent.mark_finished = True
        return intent

    def parse_upsert_squad_intent(self, initial_words, backup):
        """Returns a squad upsert intent or raises an error."""
        (activity_type, words) = self.parse_activity_type(initial_words)
        date_time = None
        try:
            (date_time, _, words) = self.parse_datetime(words)
        except:
            pass
        intent = Intent()
        intent.activity_id.type = activity_type
        intent.activity_id.timestamp_seconds = self.timestamp(date_time)
        at_least_once = False
        added = []
        removed = []
        while len(words) > 0 or not at_least_once:
            at_least_once = True
            gamer_tag, is_add, words = self.parse_gamer_tag(words)
            stats = self.__api_bundle.stats_by_player[gamer_tag].activity_stats
            rating = RatedPlayer.Rating.UNKNOWN
            for stat in stats:
                if stat.activity_type == activity_type:
                    completions = stat.completions
                    if completions > EXPERIENCED_MIN_COMPLETIONS:
                        rating = RatedPlayer.Rating.EXPERIENCED
                    elif completions > INTERMEDIATE_MIN_COMPLETIONS:
                        rating = RatedPlayer.Rating.INTERMEDIATE
                    else:
                        rating = RatedPlayer.Rating.BEGINNER
                    break
            player = RatedPlayer()
            player.gamer_tag = gamer_tag
            player.rating = rating
            if is_add:
                added.append(player)
            else:
                removed.append(player)

        added_squad = Squad()
        if backup:
            added_squad.substitutes.extend(added)
        else:
            added_squad.players.extend(added)
        removed_squad = Squad()
        if backup:
            removed_squad.substitutes.extend(removed)
        else:
            removed_squad.players.extend(removed)

        intent.upsert_squad.added.CopyFrom(added_squad)
        intent.upsert_squad.removed.CopyFrom(removed_squad)
        return intent

    def parse_activity_type(self, initial_words):
        """
        Matches an activity type from the given word array.
        Returns (the best matching activity type, the rightmost unused words).
        Throws an exception in case of failure.
        """
        if len(initial_words) == 0:
            raise ValueError("Il manque un nom d'activité")

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
                    min([self.levensthein(query, name, '[^A-Za-z0-9+-/]+') for name in a[1]])
                ),
                activities)
            levensthein_by_activity = list(levensthein_by_activity)
            levensthein_by_activity = sorted(
                levensthein_by_activity,
                key=lambda a: a[1]
            )
            (best_activity, best_levensthein) = levensthein_by_activity[0]
            if best_levensthein > 2 or best_levensthein > 0.4 * len(query):
                continue
            best_activity_so_far = best_activity
            unused_words_for_best_activity_so_far = words.copy()

        if not best_activity_so_far:
            raise ValueError(
                'Un nom d\'activité aurait dû être présent à partir de "' +
                ' '.join(initial_words) +
                '"'
            )
        return best_activity_so_far, unused_words_for_best_activity_so_far

    def parse_datetime(self, initial_words):
        """
        Matches a datetime from the given word array.
        Returns (the best matching date time, with_time? bool, the rightmost unused words).
        Several formats are supported.
        Raises an error if no match is found.
        """
        if len(initial_words) == 0:
            raise ValueError('Il manque une date et une heure')

        query = ""
        words = initial_words.copy()
        popped_words = 0
        best_datetime_so_far = None
        unused_words_for_best_datetime_so_far = words.copy()
        with_time = True
        while len(words) > 0 and popped_words < 2:
            query += " " + words.pop(0)
            popped_words += 1

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

        if best_datetime_so_far is None:
            raise ValueError(
                'Une date et une heure auraient dû être présent à partir de "' +
                ' '.join(initial_words) +
                '"'
            )

        return (
            best_datetime_so_far,
            with_time,
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
        best_gamer_tag_so_far = None
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
            best_gamer_tag_so_far = best_gamer_tag
            unused_words_for_best_gamer_tag_so_far = words.copy()

        if best_gamer_tag_so_far:
            return best_gamer_tag_so_far, is_add, unused_words_for_best_gamer_tag_so_far

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

    def timestamp(self, date_time):
        """
        Converts the given date time to a timestamp.
        Returns 0 if the input is not valid.
        """
        try:
            return int(datetime.timestamp(date_time))
        except:
            return 0

    def assert_words_empty(self, words):
        """Raises an error if the words are empty."""
        if len(words) > 0:
            rest = " ".join(words)
            raise ValueError("La commande aurait dû s'arrêter juste avant " + rest)
