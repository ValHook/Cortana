import re
import unidecode
from protos.activity_id_pb2 import ActivityID

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

    def __init__(self, message):
        if not isinstance(message, str):
            raise ValueError("Message vide")
        self.__message = message

    @property
    def message(self):
        """Returns the message this parser will process."""
        return self.__message

    def parse_activity_type(self, initial_words):
        """
        Matches an activity type from the given word array.
        Returns (the best matching activity type, the rightmost unused words).
        Throws an exception in case of failure.
        """
        if len(initial_words) == 0:
            raise ValueError("Il manque le nom de l'activité")

        activities = ACTIVITY_NAMES_BY_TYPE.items()
        best_activity_so_far = None
        unused_words_for_best_activity_so_far = None
        query = ""
        words = initial_words.copy()
        while len(words) > 0:
            query += " " + words.pop(0)
            levensthein_by_activity = map(lambda a: (a[0], min(
                [self.levensthein(query, name) for name in a[1]])), activities)
            levensthein_by_activity = list(levensthein_by_activity)
            levensthein_by_activity = sorted(
                levensthein_by_activity, key=lambda a: a[1])
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

        return (best_activity_so_far, unused_words_for_best_activity_so_far)

    def levensthein(self, str_a, str_b):
        """Returns a slightly adjusted levensthein distance between str_a and str_b."""
        str_a = unidecode.unidecode(str_a)
        str_b = unidecode.unidecode(str_b)
        str_a = str_a.strip()
        str_b = str_b.strip()
        str_a = str_a.lower()
        str_b = str_b.lower()
        str_a = re.sub('[^A-Za-z0-9+-]+', '', str_a)
        str_b = re.sub('[^A-Za-z0-9+-]+', '', str_b)
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
