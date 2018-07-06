import logging

from discord.ext.commands import Bot
from discord.message import Message

from core.cogs.toolbox import StatefulCog
from core.constants import DEVLOG_CHANNEL

logger = logging.getLogger(__name__)


class Moderation(StatefulCog):
    """
    Useful commands for moderators.
    """

    def __init__(self, bot: Bot):
        super(Moderation, self).__init__()
        self.bot = bot
        self.bot.add_listener(self.monitor, name='on_message')

    async def monitor(self, message: Message):

        if message.author == self.bot.user: return
        dev_log = self.bot.get_channel(DEVLOG_CHANNEL)

        if 'fuck' in message.content:
            await self.bot.send_message(dev_log, f'{message.author.name} has said fuck.')


def setup(bot):
    bot.add_cog(Moderation(bot))
    logger.info("Cog loaded: Utility")
