from typing import Optional

from discord.ext.commands import Bot
from discord import Server, Role


class Zola(Bot):
    """
    Building upon the Discord server class, adding typing and helper functions.
    """

    def __init__(self, *args, **kwargs):
        super(Zola, self).__init__(*args, **kwargs)

    def get_server(self, server_id) -> Optional[Server]:
        """
        Get a discord server by id.
        """
        return super(Zola, self).get_server(server_id)

    def get_role(self, server_id, role_id) -> Optional[Role]:
        """
        Get a role from a server by id.
        """
        server = self.get_server(server_id)
        if not server or not hasattr(server, 'roles'):
            return None

        for role in server.roles:
            if role.id == role_id:
                return role
