import logging

import datetime
import pydash
import time
from discord import Server
from discord.ext.commands import Bot, command, Context, group

from core.constants import ZEN_SERVER, ZOLA_UTILS_ROLE
from core.decorators import with_role

logger = logging.getLogger(__name__)


class Utility(object):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.stopwatches = {}

    @command(name='test', hidden=True, pass_context=True)
    async def test_command(self, ctx: Context):
        """
        Count how many messages you have in this channel.
        """

        placeholder = await self.bot.say('Fetching messages..')
        messages = [m async for m in self.bot.logs_from(ctx.message.channel)]
        my_messages = pydash.filter_(
            messages,
            lambda m: m.author == ctx.message.author
        )

        return await self.bot.edit_message(
            placeholder,
            f'You have {len(my_messages)} messages.'
        )

    @command(name='clear', pass_context=True)
    @with_role(ZOLA_UTILS_ROLE)
    async def clear_command(self, ctx: Context, limit=10000):
        """
        Clear messages from a channel.
        """

        try:
            limit = int(limit)
        except ValueError:
            await ctx.invoke(self.bot.get_command('help'), 'clear')
            return

        if limit is 1:
            await self.bot.delete_message(ctx.message)
            return

        messages = [m async for m in
                    self.bot.logs_from(ctx.message.channel, limit=limit)]
        await self.bot.delete_messages(messages=messages)

    @group(name='id', pass_context=True)
    @with_role(ZOLA_UTILS_ROLE)
    async def id_command(self, ctx: Context):
        """
        Get the Discord ID by name.
        """

        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), 'id')

    @id_command.command(name='role', ignore_extra=True, pass_context=True)
    @with_role(ZOLA_UTILS_ROLE)
    async def id_role_command(self, ctx: Context, role_name):
        """
        Get the Discord ID of a role.
        """

        for role in self.bot.get_server(ZEN_SERVER).roles:
            if role_name == role.name:
                return await self.bot.say(role.id)

        return await self.bot.say(f'No role found "{role_name}"')

    @command(name='stopwatch', aliases=['sw'], pass_context=True)
    async def stopwatch_command(self, ctx):
        """
        Starts/Stop a stopwatch.
        """
        author = ctx.message.author
        if author.id not in self.stopwatches:
            self.stopwatches[author.id] = int(time.perf_counter())
            await self.bot.say(author.mention + ' - Stopwatch started!')
        else:
            tmp = abs(self.stopwatches[author.id] - int(time.perf_counter()))
            tmp = str(datetime.timedelta(seconds=tmp))
            await self.bot.say(author.mention + ' - Stopwatch stopped! Time: **' + tmp + '**')
            self.stopwatches.pop(author.id, None)

    @command(name='lmgtfy')
    async def lmgtfy(self, *, search_terms: str):
        """
        Let me Google that for you.
        """
        search_terms = search_terms\
            .replace('@everyone', '@\u200beveryone')\
            .replace('@here', '@\u200bhere')\
            .replace(' ', '+')
        await self.bot.say('https://lmgtfy.com/?q={}'.format(search_terms))


def setup(bot):
    bot.add_cog(Utility(bot))
    logger.info("Cog loaded: Utility")
