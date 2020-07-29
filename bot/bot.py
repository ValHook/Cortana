from datetime import datetime
import os
from pathlib import Path
from dateutil import tz
from appdirs import user_data_dir
import discord
from components.api_fetcher.api_fetcher import Fetcher
from components.img_generator.img_generator import Generator
from components.intent_parser.intent_parser import Parser
from components.intent_executor.intent_executor import Executor
from components.storage.storage import Storage
from protos.schedule_pb2 import Schedule

CORTANA_BUNGIE_API_KEY = os.environ.get('CORTANA_BUNGIE_API_KEY', '')
CORTANA_DISCORD_TOKEN = os.environ.get('CORTANA_DISCORD_TOKEN', '')
ROOT_DIRECTORY = Path(user_data_dir('cortana-destiny-discord', 'WalOby')) \
    .joinpath(CORTANA_DISCORD_TOKEN) \
    .joinpath(CORTANA_BUNGIE_API_KEY)
TIMEZONE = tz.gettz('Europe/Paris')
LOCALE = 'fr'


class Bot(discord.Client):
    """Discord client that handles events. Single threaded."""

    def __init__(self):
        super().__init__()
        self.__generator = Generator(TIMEZONE, LOCALE)
        self.__fetcher = Fetcher(CORTANA_BUNGIE_API_KEY)
        self.__parser = Parser(LOCALE)
        self.has_been_ready_once = False

    async def on_ready(self):
        """Called when the bot is booted."""
        if not self.has_been_ready_once:
            self.has_been_ready_once = True
            print("Le bot est désormais connecté.")
            print(f"Nom d'utilisateur: {self.user.name}.")
        else:
            print("Le bot vient de se reconnecter.")

    async def on_message(self, message):
        """Called when a message is received. Wraps around |handle_message|."""
        try:
            await self.handle_message(message)
        except Exception as e:
            print("Exception :")
            await self.answer_message(str(e), message)

    async def handle_message(self, message):
        """Real message handler."""
        if message.author == self.user or not message.content.startswith("!cortana "):
            return
        print()
        print(message.guild.name)
        print(message.author)
        print(message.content)

        # Init storage for current guild.
        now = datetime.now(TIMEZONE)
        storage = Storage(ROOT_DIRECTORY.joinpath(str(message.guild.id)))

        # Make sure a basic bundle is available.
        bundle = None
        try:
            bundle = storage.read_api_bundle()
        except:
            await self.answer_message(
                "Une synchronisation des joueurs doit être effectuée.\nVeuillez patienter...",
                message
            )
            bundle = self.__fetcher.fetch(now)
            storage.write_api_bundle(bundle)
            await self.answer_message("Synchronisation terminée", message)

        # Make sure a basic schedule is available.
        try:
            storage.read_schedule()
        except:
            storage.write_schedule(Schedule())

        # Parse intent.
        intent = self.__parser.parse(message.content, bundle, now)

        # Execute intent.
        if intent.HasField('global_intent') and intent.global_intent.sync_bundle:
            await self.answer_message("Synchronisation en cours.\nVeuillez patienter...", message)
        executor = Executor(storage, self.__fetcher, self.__generator)
        (feedback, images) = executor.execute(intent, now)

        # Post message.
        await self.answer_message(feedback, message)

        # Post images.
        if not images:
            return
        for index, image in enumerate(images):
            file = discord.File(fp=image, filename="Affiche"+str(index)+".gif")
            await message.channel.send(file=file)

    async def answer_message(self, answer, message):
        """print() + message.channel.send()"""
        print(answer)
        # Messages need to be posted in chunks, each smaller than 2000 bytes.
        answer_split = answer.splitlines()
        answers = ['']
        for a in answer_split:
            if len(answers[-1]) + len(a) < 1990:
                answers[-1] = answers[-1] + "\n" + a
            else:
                answers.append(a)
        for a in answers:
            await message.channel.send("```" + a + "```")


if __name__ == "__main__":
    if not CORTANA_DISCORD_TOKEN:
        raise ValueError("CORTANA_DISCORD_TOKEN non configuré.")
    if not CORTANA_BUNGIE_API_KEY:
        raise ValueError("CORTANA_BUNGIE_API_KEY non configurée.")
    print("Démarrage du bot...")
    print(f"Dossier de stoackge racine: {ROOT_DIRECTORY}")
    bot = Bot()
    bot.run(CORTANA_DISCORD_TOKEN)
