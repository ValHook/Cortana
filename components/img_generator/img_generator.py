import io
import math
from datetime import tzinfo
from babel.dates import format_datetime
from PIL import Image, ImageDraw, ImageSequence, ImageFont
from components.converters.when import to_datetime
from protos.activity_id_pb2 import ActivityID
from protos.planning_pb2 import Planning
from protos.rated_player_pb2 import RatedPlayer
from protos.activity_pb2 import Activity

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
    "section_w": 349,
    "section_h": 197,
    "margin_x": 10,
    "margin_y": 12,
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
CR_LARGE = ImageFont.truetype('components/img_generator/assets/calibri_bold.ttf', 32)
CI = ImageFont.truetype('components/img_generator/assets/calibri_italic.ttf', 16)

COLORS = {
    "blue": (78, 96, 224, 255),
    "purple": (144, 9, 226, 255),
    "black": (0, 0, 0, 255),
    "green": (15, 155, 73, 255),
    "orange": (188, 96, 15, 255),
    "red": (224, 28, 29, 255)
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

    def __init__(self, date_tz, locale):
        assert isinstance(date_tz, tzinfo), "Fuseau horaire non configuré"
        if not isinstance(locale, str) or len(locale) == 0:
            raise ValueError("Locale non configurée")
        self.__date_tz = date_tz
        self.__locale = locale

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
        return new_x, new_y

    def write_finished_message(self, frame, section):
        """
        Writes a message indicating the raid is over on the relevant section.
        :param frame: the frame where the message should be written.
        :param section: the section index.
        """
        message = "Terminé !"
        mark_width, mark_height = CR_LARGE.getsize(message)
        fimg = Image.new('RGBA', (mark_width, mark_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(fimg)
        draw.text((0, 0), text=message, font=CR_LARGE, fill=COLORS["red"])
        angle = math.degrees(math.atan(COORDS["section_h"] / COORDS["section_w"]))
        fimg = fimg.rotate(angle, expand=1)
        px = int((COORDS["section_w"] - fimg.size[0]) / 2)
        py = int((COORDS["section_h"] - fimg.size[1]) / 2)
        px, py = self.move((px, py), section)
        frame.paste(fimg, (px, py, px + fimg.size[0], py + fimg.size[1]), fimg)

    def write_to_frame(self, frame, banner_number, planning):
        """
        Writes the relevant information for a given GIF frame.
        :param frame: an Image object to write to.
        :param banner_number: an int representing the GIF index.
        :param planning: The activity planning.
        """
        draw = ImageDraw.Draw(frame)
        max_section = min((banner_number + 1) * NUM_SECTIONS, len(planning.activities))
        for section in range(banner_number * NUM_SECTIONS, max_section):
            a = planning.activities[section]
            name_w = CR.getsize(ACTIVITY_NAMES[a.id.type])[0]
            draw.text(
                self.move(COORDS["activity"], section, name_w),
                ACTIVITY_NAMES[a.id.type], font=CR,
                fill=COLORS["purple"]
            )
            date_time = to_datetime(a.id.when, self.__date_tz)
            if date_time:
                date_format = "EEEE d MMMM, à HH:mm" if a.id.when.time_specified else "EEEE d MMMM"
                sdate = format_datetime(
                    date_time,
                    format=date_format,
                    tzinfo=self.__date_tz,
                    locale=self.__locale
                ).capitalize()
            else:
                sdate = ""
            detail_w = CR.getsize(sdate)[0]
            draw.text(
                self.move(COORDS["details"], section, detail_w),
                sdate,
                font=CI,
                fill=COLORS["purple"]
            )
            for i, p in enumerate(a.squad.players):
                draw.text(
                    self.move(COORDS["players"][i], section),
                    p.gamer_tag,
                    font=CR,
                    fill=COLORS_BY_RATING[p.rating]
                )
            draw.text(
                self.move(COORDS["substitutes"][0], section),
                "Remplaçants:",
                font=CR,
                fill=COLORS["black"]
            )
            for i, p in enumerate(a.squad.substitutes):
                draw.text(
                    self.move(COORDS["substitutes"][i+1], section),
                    p.gamer_tag,
                    font=CR,
                    fill=COLORS_BY_RATING[p.rating]
                )
            if a.state == Activity.State.FINISHED:
                self.write_finished_message(frame, section)
                l_start = (COORDS["margin_x"], COORDS["margin_y"] + COORDS["section_h"])
                l_start = self.move(l_start, section)
                l_end = (COORDS["margin_x"] + COORDS["section_w"], COORDS["margin_y"])
                l_end = self.move(l_end, section)
                draw.line([l_start, l_end], width=6, fill=COLORS["red"])
            elif a.state == Activity.State.MILESTONED:
                milestone = "[" + a.milestone + "]"
                state_w = CR_LARGE.getsize(milestone)[0]
                draw.text(
                    self.move((20, COORDS["section_h"] / 2), section, state_w),
                    milestone,
                    font=CR_LARGE,
                    fill=COLORS["red"]
                )

    def generate_images(self, planning):
        """
        Generates as many images as needed to display the activity planning.
        :param planning: The activity planning.
        :return: an array of BytesIO streams containing the GIFs.
        """
        assert isinstance(planning, Planning), "Planning vide"
        gifs = []
        needed_banners = ((len(planning.activities) - 1) // NUM_SECTIONS) + 1
        for banner_number in range(needed_banners):
            temp = io.BytesIO()
            with Image.open('components/img_generator/assets/empty_banner.gif') as im:
                frames = []
                for frame in ImageSequence.Iterator(im):
                    frame = frame.copy().convert('RGBA')
                    self.write_to_frame(frame, banner_number, planning)
                    resize_to = (frame.size[0] // 1.44, frame.size[1] // 1.44)
                    frame.thumbnail(resize_to, Image.ANTIALIAS)
                    frames.append(frame)
                frames[0].save(temp, save_all=True, append_images=frames[1:], format="GIF")
                temp.seek(0)
                gifs.append(temp)
        return gifs
