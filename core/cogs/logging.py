# coding=utf-8
import logging

from discord.ext.commands import Bot

from core.constants import DEVLOG_CHANNEL

log = logging.getLogger(__name__)


class Logging:
    """
    Debug logging module
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def on_ready(self):
        log.info("Bot connected!")

        dev_log = self.bot.get_channel(DEVLOG_CHANNEL)
        await self.bot.send_message(dev_log, 'Connected!')


def setup(bot):
    bot.add_cog(Logging(bot))
    log.info("Cog loaded: Logging")
