import logging
import pydash

from discord import Embed, Member
from discord.ext.commands import command, Context

from core.zola import Zola
from core.constants import GAME_ROLES, GAME_LIST_STRING, ZEN_SERVER
from core.shortcuts import get_raw_arg

logger = logging.getLogger(__name__)


class GameHalls(object):
    """
    Join a game hall for access to a game's channels.

    At Zen of Gaming, we have many game halls which are open to you. Use
    the following commands to join one and start chatting.
    """

    def __init__(self, bot: Zola):
        self.bot = bot

    @command(name='gamelist', aliases=['glist', 'games'])
    async def list_command(self):
        """
        List the available game halls.
        """
        await self.bot.say('Available game halls: {}'.format(GAME_LIST_STRING))

    @command(name='gamejoin', aliases=['gjoin'], pass_context=True,
             ignore_extra=True, no_pm=True)
    async def join_command(self, ctx: Context, game):
        """
        Join a gaming hall.
        """
        arg = get_raw_arg(ctx)

        # Get the role for the user specified game
        role = None
        for g, rid in GAME_ROLES.items():
            if g.lower() == arg.lower():
                role = self.bot.get_role(ZEN_SERVER, rid)

        # If the game could not be matched to a role, print a helpful error
        if role is None:
            await self.bot.say(f'A gaming hall does not yet exist for '
                               f'**{arg}**. Use the !gamelist command to '
                               f'see available gaming halls. Ping Nivix to '
                               f'suggest a new hall.')
            return

        # If the user already has the role, do nothing
        if role in ctx.message.author.roles:
            return

        # If the user does not have the role, give it to them
        await self.bot.add_roles(ctx.message.author, role)

    @command(name='gameleave', aliases=['gleave'], pass_context=True,
             ignore_extra=True, no_pm=True)
    async def leave_command(self, ctx, game):
        """
        Leave a gaming hall.
        """
        arg = get_raw_arg(ctx)

        # Get the role for the user specified game
        role = None
        for g, rid in GAME_ROLES.items():
            if g.lower() == arg.lower():
                role = self.bot.get_role(ZEN_SERVER, rid)

        # If the game could not be matched to a role, print a helpful error
        if role is None:
            await self.bot.say(f'A gaming hall does not exist for **{arg}**.')
            return

        # If the user does not have the role, do nothing
        if role not in ctx.message.author.roles:
            return

        # If the user has the role, remove it
        await self.bot.remove_roles(ctx.message.author, role)




def setup(bot):
    bot.add_cog(GameHalls(bot))
    logger.info("Cog loaded: GameHalls")
