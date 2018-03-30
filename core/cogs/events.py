# coding=utf-8
import logging

from discord import Embed
from discord.ext.commands import (
    BadArgument, Bot,
    CommandError, CommandInvokeError, Context,
    NoPrivateMessage, UserInputError
)

from core.constants import DEVLOG_CHANNEL

log = logging.getLogger(__name__)


class Events:
    """
    No commands, just event handlers
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def on_command_error(self, e: CommandError, ctx: Context):
        command = ctx.command
        parent = None

        if command is not None:
            parent = command.parent

        if parent and command:
            help_command = (self.bot.get_command("help"), parent.name, command.name)
        elif command:
            help_command = (self.bot.get_command("help"), command.name)
        else:
            help_command = (self.bot.get_command("help"),)

        if isinstance(e, BadArgument):
            await self.bot.say(f"Malformed function data: {e}\n")
            await ctx.invoke(*help_command)
        elif isinstance(e, UserInputError):
            await ctx.invoke(*help_command)
        elif isinstance(e, NoPrivateMessage):
            await self.bot.say("That function cannot be used in a private message.")
        elif isinstance(e, CommandInvokeError):
            print(e)
            m = await self.bot.send_message(ctx.message.channel, 'Function failure. Creating a log of this failure..')
            embed = Embed(description=f'{e}')
            embed.set_author(
                name="Zola",
                url="https://www.youtube.com/watch?v=E486XjhYHh8",
                icon_url="https://img3.wikia.nocookie.net/__cb20140406081200/villains/images/e/e7/ZOLA.jpg"
            )
            await self.bot.send_message(self.bot.get_channel(DEVLOG_CHANNEL), embed=embed)
            await self.bot.edit_message(m, 'Function failure. Creating a log of this failure.. Done.')
            raise e.original
        log.error(f"COMMAND ERROR: '{e}'")


def setup(bot):
    bot.add_cog(Events(bot))
    log.info("Cog loaded: Events")
