from protos.planning_pb2 import Planning
from protos.activity_id_pb2 import ActivityID
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io
import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, "fr_FR")

COORDS = {
    "activity": (170, 20),
    "details": (140, 40),
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
    ]
}

ACTIVITY_NAMES = {
    ActivityID.Type.CALUS: "Calus",
    ActivityID.Type.EATER_OF_WORLDS: "Dévoreur de Mondes",
    ActivityID.Type.SPIRE_OF_STARS: "Flèche d'étoiles",
    ActivityID.Type.CROWN_OF_SORROW: "Couronne du Malheur",
    ActivityID.Type.LAST_WISH: "Dernier Voeu",
    ActivityID.Type.SCOURGE_OF_THE_PAST: "Fléau du Passé",
    ActivityID.Type.GARDEN_OF_SALVATION: "Jardin du Salut",
    ActivityID.Type.VAULT_OF_GLASS: "Caveau de Verre",
    ActivityID.Type.CROPTAS_END: "Cropta",
    ActivityID.Type.THE_TAKEN_KING: "La Chute du Roi",
    ActivityID.Type.WRATH_OF_THE_MACHINE: "Fureur Mécanique",
}

CR = ImageFont.truetype('components/img/assets/calibri_bold.ttf', 16)
CI = ImageFont.truetype('components/img/assets/calibri_italic.ttf', 16)

class Generator:
    """Generates the planning in GIF/PNG format."""

    def __init__(self, planning):
        self.__planning = planning

    def write_to_frame(self, f):
        a = self.__planning.activities[0]
        f.text(COORDS["activity"], ACTIVITY_NAMES[a.id.type], font=CR, fill=(144,9,226,255))
        sdate = datetime.utcfromtimestamp(a.id.timestamp_seconds).strftime("%A %d %B")
        f.text(COORDS["details"], sdate, font=CI, fill=(144,9,226,255))
        for i, p in enumerate(a.squad.players):
            f.text(COORDS["players"][i], p.gamer_tag, font=CR, fill=(78,96,224,255))
        f.text(COORDS["substitutes"][0], "Remplaçants:", font=CR, fill=(0,0,0,255))
        for i, p in enumerate(a.squad.substitutes):
            f.text(COORDS["substitutes"][i+1], p.gamer_tag, font=CR, fill=(78,96,224,255))

    def generate_image(self):
        with Image.open('components/img/assets/empty_banner.gif') as im:
            frames = []
            for frame in ImageSequence.Iterator(im):
                frame = frame.convert('RGB')
                d = ImageDraw.Draw(frame)
                self.write_to_frame(d)
                del d
                b = io.BytesIO()
                frame.save(b, format="GIF")
                frame = Image.open(b)
                frames.append(frame)
            frames[0].save('/tmp/out.gif', save_all=True, append_images=frames[1:])
