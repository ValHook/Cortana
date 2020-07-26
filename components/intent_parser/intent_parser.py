from datetime import datetime
from datetime import tzinfo
import re
import unidecode
import dateparser
from protos.activity_id_pb2 import ActivityID
from protos.api_bundle_pb2 import APIBundle
from protos.intent_pb2 import Intent, ActivityIntent
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

    def __init__(self, locale):
        if not isinstance(locale, str):
            raise ValueError("Locale non configurée")
        self.__locale = locale

    def parse(self, message, api_bundle, now):
        """
        Parser entry point.
        :param message: The message to parse.
        :param api_bundle: The API Bundle, used to identify gamer tags and experience levels.
        :param now: Now as a datetime.
        :return: An intent if the message is a bot intent or None if not.
        i.e Messages starting with !raid are treated as intents. The rest are not.
        :raises: An error if the message is an intent but ill-formed.
        """
        assert isinstance(message, str), "Message vide"
        assert isinstance(now, datetime), "Horloge non configurée"
        assert isinstance(now.tzinfo, tzinfo), "Fuseau horaire non configuré"
        if not isinstance(api_bundle, APIBundle) or len(api_bundle.stats_by_player) < 6:
            raise ValueError("API Bundle vide")
        words = re.split(r"\s+", message)
        next_word = words.pop(0)
        if next_word != '!raid':
            return None
        next_word = words.pop(0)
        if next_word == "sync":
            return self.parse_sync_intent(words)
        if next_word == "lastsync":
            return self.parse_lastsync_intent(words)
        if next_word == "images":
            return self.parse_images_intent(words)
        if next_word == "date":
            return self.parse_update_datetime_intent(words, now)
        if next_word == "milestone":
            return self.parse_update_milestone_intent(words, now)
        if next_word == "finish":
            return self.parse_finish_intent(words, now)
        if next_word == "remove":
            return self.parse_remove_intent(words, now)
        if next_word == "clearpast":
            return self.parse_clearpast_intent(words)
        if next_word == "backup":
            return self.parse_upsert_squad_intent(words, True, api_bundle, now)
        return self.parse_upsert_squad_intent([next_word] + words, False, api_bundle, now)

    def parse_clearpast_intent(self, initial_words):
        """
        :param: The words after !raid clearpast.
        :return: A clear past intent.
        :raises: If the words are not empty.
        """
        self.assert_words_empty(initial_words)
        intent = Intent()
        intent.global_intent.clear_all_activities_from_past_weeks = True
        return intent

    def parse_sync_intent(self, initial_words):
        """
        :param: The words after !raid sync.
        :return: A sync intent.
        :raises: If the words are not empty.
        """
        self.assert_words_empty(initial_words)
        intent = Intent()
        intent.global_intent.sync_bundle = True
        return intent

    def parse_lastsync_intent(self, initial_words):
        """
        :param: The words after !raid lastsync.
        :return: A lastsync intent.
        :raises: If the words are not empty.
        """
        self.assert_words_empty(initial_words)
        intent = Intent()
        intent.global_intent.get_last_bundle_sync_datetime = True
        return intent

    def parse_images_intent(self, initial_words):
        """
        :param: The words after !raid images.
        :return: An image generation intent.
        :raises: If the words are not empty.
        """
        self.assert_words_empty(initial_words)
        intent = Intent()
        intent.global_intent.generate_images = True
        return intent

    def parse_update_datetime_intent(self, initial_words, now):
        """
        :param initial_words: The words after !raid date.
        :param now: Now as a datetime.
        :return: A datetime update intent.
        :raises: If the words are not in the format (old_datetime) [new_datetime].
        """
        (activity_type, words) = self.parse_activity_type(initial_words)
        (old_date_time, _, words) = self.parse_datetime(words, now)
        try:
            (new_date_time, _, words) = self.parse_datetime(words, now)
        except:
            new_date_time = old_date_time
            old_date_time = None
        self.assert_words_empty(words)
        activity_intent = ActivityIntent()
        activity_intent.activity_id.type = activity_type
        old_when = self.make_when(old_date_time)
        new_when = self.make_when(new_date_time)
        if old_when:
            activity_intent.activity_id.when.CopyFrom(old_when)
        if new_when:
            activity_intent.update_when.CopyFrom(new_when)
        intent = Intent()
        intent.activity_intent.CopyFrom(activity_intent)
        return intent

    def parse_update_milestone_intent(self, initial_words, now):
        """
        :param initial_words: The words after !raid milestone.
        :param now: Now as a datetime.
        :return: A milestone update intent.
        :raises: If the words are not in the format [activity_type] (datetime) [milestone].
        """
        (activity_type, words) = self.parse_activity_type(initial_words)
        date_time = None
        try:
            (date_time, _, words) = self.parse_datetime(words, now)
        except:
            pass
        activity_intent = ActivityIntent()
        activity_intent.activity_id.type = activity_type
        when = self.make_when(date_time)
        if when:
            activity_intent.activity_id.when.CopyFrom(when)
        if len(words) == 0:
            raise ValueError("Il manque le nom de la milestone")
        activity_intent.set_milestone = " ".join(words).capitalize()
        intent = Intent()
        intent.activity_intent.CopyFrom(activity_intent)
        return intent

    def parse_finish_intent(self, initial_words, now):
        """
        :param initial_words: The words after !raid finish.
        :param now: Now as a datetime.
        :return: A finish marking intent.
        :raises: If the words are not in the format [activity_type] (datetime).
        """
        (activity_type, words) = self.parse_activity_type(initial_words)
        date_time = None
        try:
            (date_time, _, words) = self.parse_datetime(words, now)
        except:
            pass
        activity_intent = ActivityIntent()
        activity_intent.activity_id.type = activity_type
        when = self.make_when(date_time)
        if when:
            activity_intent.activity_id.when.CopyFrom(when)
        self.assert_words_empty(words)
        activity_intent.mark_finished = True
        intent = Intent()
        intent.activity_intent.CopyFrom(activity_intent)
        return intent

    def parse_remove_intent(self, initial_words, now):
        """
        :param initial_words: The words after !raid remove.
        :param now: Now as a datetime.
        :return: An activity removal intent.
        :raises: If the worgit ds are not in the format [activity_type] (datetime).
        """
        (activity_type, words) = self.parse_activity_type(initial_words)
        date_time = None
        try:
            (date_time, _, words) = self.parse_datetime(words, now)
        except:
            pass
        activity_intent = ActivityIntent()
        activity_intent.activity_id.type = activity_type
        when = self.make_when(date_time)
        if when:
            activity_intent.activity_id.when.CopyFrom(when)
        self.assert_words_empty(words)
        activity_intent.remove = True
        intent = Intent()
        intent.activity_intent.CopyFrom(activity_intent)
        return intent

    def parse_upsert_squad_intent(self, initial_words, backup, api_bundle, now):
        """
        :param initial_words: The words after !raid or !raid backup.
        :param backup: A boolean telling whether this upsert squad intent must be for substitutes.
        :param api_bundle: The API Bundle used to resolve gamer tags and experience levels.
        :param now: Now as a datetime.
        :return: A squad upsert intent.
        :raises: If the words are not in the format [activity_type] (datetime) [players].
        Each player can be prefixed with a + or a - if needed.
        """
        (activity_type, words) = self.parse_activity_type(initial_words)
        date_time = None
        try:
            (date_time, _, words) = self.parse_datetime(words, now)
        except:
            pass
        activity_intent = ActivityIntent()
        activity_intent.activity_id.type = activity_type
        when = self.make_when(date_time)
        if when:
            activity_intent.activity_id.when.CopyFrom(when)
        at_least_once = False
        added = []
        removed = []
        while len(words) > 0 or not at_least_once:
            at_least_once = True
            gamer_tag, is_add, words = self.parse_gamer_tag(words, api_bundle)
            stats = api_bundle.stats_by_player[gamer_tag].activity_stats
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

        if len(added) > 0:
            added_squad = Squad()
            if backup:
                added_squad.substitutes.extend(added)
            else:
                added_squad.players.extend(added)
            activity_intent.upsert_squad.added.CopyFrom(added_squad)

        if len(removed) > 0:
            removed_squad = Squad()
            if backup:
                removed_squad.substitutes.extend(removed)
            else:
                removed_squad.players.extend(removed)
            activity_intent.upsert_squad.removed.CopyFrom(removed_squad)

        intent = Intent()
        intent.activity_intent.CopyFrom(activity_intent)
        return intent

    def parse_activity_type(self, initial_words):
        """
        Matches an activity type from the given word array.
        :param initial_words: A word array
        :return: A (the best matching activity type, the rightmost unused words) tuple.
        :raises: If the are not in the format [activity_type] (noise)
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

    def parse_datetime(self, initial_words, now):
        """
        Matches a datetime from the given word array.
        :param initial_words: A word array.
        :param now: Now as a datetime.
        :return: A (the best matching date time, with_time? bool, the rightmost unused words) tuple.
        :raises: If the are not in the format [datetime] (noise)
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
                    settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': now}
                )
            except:
                # Dateparser can't deal with the case where the timezone is only present in either
                # the parsed query or the relative base.
                parsed_datetime = dateparser.parse(
                    query,
                    locales=[self.__locale],
                    settings={
                        'PREFER_DATES_FROM': 'future',
                        'RELATIVE_BASE': now.replace(tzinfo=None)
                    }
                )
            if parsed_datetime is None:
                continue
            # Dateparser wrongly adds implicit times to strings like "aujourd'hui" and "demain"
            # Filter them out.
            if not re.search(r"[0-9]h", query):
                with_time = False
                parsed_datetime = parsed_datetime.replace(
                    hour=0, minute=0, second=0, microsecond=0, tzinfo=None
                )
            else:
                with_time = True
                parsed_datetime = parsed_datetime.replace(tzinfo=now.tzinfo)
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

    def parse_gamer_tag(self, initial_words, api_bundle):
        """
        Matches a gamer tag of the bundle from the given word array.
        :param initial_words: A word array
        :param api_bundle: The API Bundle used to resolve gamer tags.
        :return: (best matching gamer tag or None, add? or remove bool, the rightmost unused words).
        :raises: If the are not in the format [gamer_tag] (noise)
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
        unused_words_for_best_gamer_tag_so_far = words.copy()
        while len(words) > 0:
            query += " " + words.pop(0)
            gamer_tags = api_bundle.stats_by_player.keys()
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
        :param str_a: One of the two compared strings.
        :param str_b: The other string.
        :param filter_out_regex: A regex matching all the characters you want to ignore for the
        comparison.
        :return: Levensthein distance between the two strings after lowering them and stripping out
        characters from filter_out_regex.
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

    def make_when(self, date_time):
        """
        :param: A python datetime.
        :return: A When proto or None if the input is not valid.
        """
        try:
            when = ActivityID.When()
            if date_time.hour != 0 and date_time.minute != 0:
                when.time_specified = True
                when.datetime = date_time.isoformat()
            else:
                when.datetime = date_time.date().isoformat()
            return when
        except:
            return None

    def assert_words_empty(self, words):
        """
        :raises: An error if the words are empty.
        """
        if len(words) > 0:
            rest = " ".join(words)
            raise ValueError("La commande aurait dû s'arrêter juste avant " + rest)
