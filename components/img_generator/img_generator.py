import io
from datetime import datetime, tzinfo
from babel.dates import format_datetime
from PIL import Image, ImageDraw, ImageSequence, ImageFont
from protos.activity_id_pb2 import ActivityID
from protos.planning_pb2 import Planning
from protos.rated_player_pb2 import RatedPlayer

# Coordinates relative to (X=0, Y=0) for any section on the GIF.
# Name is short to keep the logic compact in methods below.
COORDS = {
    "activity": (20, 20),
    "details": (20, 40),
    "players": [
        (30, 60),
        (30, 85),
        (30, 110),
        (30, 135),
        (30, 160),
        (30, 185)
    ],
    "substitutes": [
        (220, 148),
        (220, 168),
        (220, 188)
    ],
    "section_w": 350,
    "delta_x": 486,
    "delta_y": 260,
}

ACTIVITY_NAMES = {
    ActivityID.Type.LEVIATHAN: "Léviathan",
    ActivityID.Type.LEVIATHAN_PRESTIGE: "Léviathan - Prestige",
    ActivityID.Type.EATER_OF_WORLDS: "Dévoreur de Mondes",
    ActivityID.Type.EATER_OF_WORLDS_PRESTIGE: "Dévoreur de Mondes - Prestige",
    ActivityID.Type.SPIRE_OF_STARS: "Flèche d'étoiles",
    ActivityID.Type.SPIRE_OF_STARS_PRESTIGE: "Flèche d'étoiles - Prestige",
    ActivityID.Type.CROWN_OF_SORROW: "Couronne du Malheur",
    ActivityID.Type.LAST_WISH: "Dernier Voeu",
    ActivityID.Type.SCOURGE_OF_THE_PAST: "Fléau du Passé",
    ActivityID.Type.GARDEN_OF_SALVATION: "Jardin du Salut",
    ActivityID.Type.VAULT_OF_GLASS: "Caveau de Verre",
    ActivityID.Type.VAULT_OF_GLASS_PRESTIGE: "Caveau de Verre - Prestige",
    ActivityID.Type.CROPTAS_END: "Cropta",
    ActivityID.Type.CROPTAS_END_PRESTIGE: "Cropta - Prestige",
    ActivityID.Type.THE_TAKEN_KING: "La Chute du Roi",
    ActivityID.Type.THE_TAKEN_KING_PRESTIGE: "La Chute du Roi - Prestige",
    ActivityID.Type.WRATH_OF_THE_MACHINE: "Fureur Mécanique",
    ActivityID.Type.WRATH_OF_THE_MACHINE_PRESTIGE: "Fureur Mécanique - Prestige",
}

CR = ImageFont.truetype('components/img_generator/assets/calibri_bold.ttf', 16)
CI = ImageFont.truetype('components/img_generator/assets/calibri_italic.ttf', 16)

COLORS = {
    "blue": (78, 96, 224, 255),
    "purple": (144, 9, 226, 255),
    "black": (0, 0, 0, 255),
    "green": (15, 155, 73, 255),
    "orange": (188, 96, 15, 255),
}

COLORS_BY_RATING = {
    RatedPlayer.Rating.UNKNOWN: COLORS["black"],
    RatedPlayer.Rating.BEGINNER: COLORS["green"],
    RatedPlayer.Rating.INTERMEDIATE: COLORS["orange"],
    RatedPlayer.Rating.EXPERIENCED: COLORS["blue"],
}

NUM_SECTIONS = 4


class Generator:
    """Generates the planning in GIF format."""

    def __init__(self, planning, date_tz):
        assert isinstance(planning, Planning), "%r is not a Planning instance" % planning
        assert isinstance(date_tz, tzinfo), "%r is not a tzinfo instance" % date_tz
        self.__planning = planning
        self.__date_tz = date_tz

    def move(self, coordinates, section, width_to_center=None):
        """
        Moves coordinates at the right place depending on the section and the center preferences.
        :param coordinates: tuple (X,Y) representing the initial coordinates.
        :param section: the section index, e.g. from 0 to 3 for the 1st GIF.
        :param width_to_center: optional int indicating the width of text if it has to be centered.
        :return: tuple for the new coordinates.
        """
        dx = COORDS["delta_x"] if (section % 2 == 1) else 0
        dy = COORDS["delta_y"] if ((section / float(NUM_SECTIONS)) % 1 >= 0.5) else 0
        new_x = coordinates[0] + dx
        new_y = coordinates[1] + dy
        if width_to_center:
            new_x += (COORDS["section_w"] - width_to_center) / 2
        return (new_x, new_y)

    def write_to_frame(self, frame, banner_number):
        """
        Writes the relevant information for a given GIF frame.
        :param frame: an Image object to write to.
        :param banner_number: an int representing the GIF index.
        """
        max_section = min((banner_number + 1) * NUM_SECTIONS, len(self.__planning.activities))
        for section in range(banner_number * NUM_SECTIONS, max_section):
            a = self.__planning.activities[section]
            name_w = CR.getsize(ACTIVITY_NAMES[a.id.type])[0]
            frame.text(
                self.move(COORDS["activity"], section, name_w),
                ACTIVITY_NAMES[a.id.type], font=CR,
                fill=COLORS["purple"]
            )
            sdate = format_datetime(
                datetime.utcfromtimestamp(a.id.timestamp_seconds),
                format="EEEE d MMMM, à HH:mm",
                tzinfo=self.__date_tz,
                locale="fr"
            ).capitalize()
            detail_w = CR.getsize(sdate)[0]
            frame.text(
                self.move(COORDS["details"], section, detail_w),
                sdate,
                font=CI,
                fill=COLORS["purple"]
            )
            for i, p in enumerate(a.squad.players):
                frame.text(
                    self.move(COORDS["players"][i], section),
                    p.gamer_tag,
                    font=CR,
                    fill=COLORS_BY_RATING[p.rating]
                )
            frame.text(
                self.move(COORDS["substitutes"][0], section),
                "Remplaçants:",
                font=CR,
                fill=COLORS["black"]
            )
            for i, p in enumerate(a.squad.substitutes):
                frame.text(
                    self.move(COORDS["substitutes"][i+1], section),
                    p.gamer_tag,
                    font=CR,
                    fill=COLORS_BY_RATING[p.rating]
                )

    def generate_images(self):
        """
        Generates as many images as needed to display the activity planning.
        :return: an array of BytesIO streams containing the GIFs.
        """
        gifs = []
        needed_banners = ((len(self.__planning.activities) - 1) // NUM_SECTIONS) + 1
        for banner_number in range(needed_banners):
            temp = io.BytesIO()
            with Image.open('components/img_generator/assets/empty_banner.gif') as im:
                frames = []
                for frame in ImageSequence.Iterator(im):
                    frame = frame.convert('RGB')
                    d = ImageDraw.Draw(frame)
                    self.write_to_frame(d, banner_number)
                    del d
                    b = io.BytesIO()
                    frame.save(b, format="GIF")
                    frame = Image.open(b)
                    frames.append(frame)
                frames[0].save(temp, save_all=True, append_images=frames[1:], format="GIF")
                gifs.append(temp)
        return gifs
