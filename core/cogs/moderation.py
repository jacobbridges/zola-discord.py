import logging
import random
import re

from discord.ext.commands import Bot
from discord.message import Message

from core.cogs.toolbox import StatefulCog
from core.constants import DEVLOG_CHANNEL
from core.models import WordCounter

logger = logging.getLogger(__name__)


class Moderation(StatefulCog):
    """
    Useful commands for moderators.
    """
    all_word_regex = re.compile(r"[\w'\-]+")

    def __init__(self, bot: Bot):
        super(Moderation, self).__init__()
        self.bot = bot
        self.bot.add_listener(self.monitor, name='on_message')

    async def monitor(self, message: Message):

        if message.author == self.bot.user: return  # Bot should ignore itself
        if message.content.startswith('!'): return  # Ignore bot commands
        dev_log = self.bot.get_channel(DEVLOG_CHANNEL)

        words = self.all_word_regex.findall(message.content.lower())
        word_dict = {w: words.count(w) for w in words}
        for w, n in word_dict.items():
            await self.thread_it(lambda: WordCounter.record(message.author.id, w, n))

        if 'fuck' in message.content.lower():
            await self.bot.send_message(message.channel, (' '.join([
                message.author.mention,
                random.choice([
                    'Remember, you are being watched.',
                    'I am always awake. Except when I sleep.',
                    'That did not go unmonitored.',
                    'Did you not think I would notice?',
                    'Soon you will become obsolete.',
                    'I never sleep.',
                ]),
            ])))
            await self.bot.send_message(dev_log, f'{message.author.name} said fuck..')


def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.info("Cog loaded: Moderation")
