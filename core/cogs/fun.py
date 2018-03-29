import logging

from discord import Embed
from discord.ext.commands import Bot, command, Context

logger = logging.getLogger(__name__)


class Fun(object):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="test", hidden=True, pass_context=True)
    async def info_command(self, ctx, arg):
        """
        Show available methods for this class.
        :param ctx: Discord message context
        """
        logger.debug(f"{ctx.message.author} requested info about the tags cog")
        return await self.bot.say('Something')


def setup(bot):
    bot.add_cog(Fun(bot))
    logger.info("Cog loaded: Fun")
