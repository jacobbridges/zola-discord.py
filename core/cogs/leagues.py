import logging
import pydash

from discord import Embed
from discord.ext.commands import command, Context, Bot


class GameLeagues(object):
    """
    Join a gaming league to join the discussion.

    At Zen of Gaming, we have many gaming leagues which are open to you. Use
    the following commands to join some leagues and start communicating. :D
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    def get_role(self, server, role_id):
        for role in server.roles:
            if role.id == role_id:
                return role

    @command(name='llist')
    def list_command(self):
        """
        List the available gaming leagues.
        """
        pass
