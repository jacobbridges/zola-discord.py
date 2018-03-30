import logging

import pydash
from discord import Server, Message, Member, User, Embed
from discord.ext.commands import Bot, command, Context, group

from core.constants import ZEN_SERVER, COLOR_ROLES, UMM_ROLES, UMM_CHANNELS

logger = logging.getLogger(__name__)
color_help = '''
Control your Discord color.

Color choices: {}'''.format(', '.join(k for k in COLOR_ROLES))


class Fun(object):

    def __init__(self, bot: Bot):
        self.bot = bot

    def get_role(self, server, role_id):
        for role in server.roles:
            if role.id == role_id:
                return role

    @command(name='mycolor', ignore_extra=True, pass_context=True, no_pm=True,
             help=color_help)
    async def color_command(self, ctx: Context, color):
        """
        Control your Discord color.
        """

        color_choice_string = ', '.join(k for k in COLOR_ROLES)
        color = pydash.chain(ctx.message.content) \
            .replace(ctx.prefix + 'mycolor', '') \
            .trim() \
            .title_case() \
            .value()
        role_id = COLOR_ROLES.get(color, None)
        server = self.bot.get_server(ZEN_SERVER)

        if role_id is None:
            await self.bot.say('Try again with one of these colors'
                               f': {color_choice_string}')
            return

        new_roles = [r for r in ctx.message.author.roles] + \
                    [self.get_role(server, role_id)]
        new_roles = pydash.uniq(new_roles)

        await self.bot.replace_roles(
            ctx.message.author,
            *[r for r in new_roles
              if r.name not in COLOR_ROLES or r.id == role_id]
        )

    @group(name='lewd', hidden=True, pass_context=True, no_pm=True)
    async def umm(self, ctx: Context):
        """
        Umm..
        """

        await self.bot.delete_message(ctx.message)

        if ctx.invoked_subcommand is not None:
            return

        if UMM_ROLES['umm'] in [r.id for r in ctx.message.author.roles]:
            return

        server = self.bot.get_server(ZEN_SERVER)
        await self.bot.add_roles(
            ctx.message.author,
            self.get_role(server, UMM_ROLES['umm'])
        )

        display_name = getattr(ctx.message.author, 'nick') or \
                       getattr(ctx.message.author, 'name')

        await self.bot.send_message(
            server.get_channel(UMM_CHANNELS['lewd']),
            u'Umm.. welcome to Club Lewd {}'.format(display_name)
        )

    @umm.command(name='leave', hidden=True, pass_context=True, no_pm=True)
    async def umm_leave_command(self, ctx: Context):
        """
        Umm..
        """

        if UMM_ROLES['umm'] in [r.id for r in ctx.message.author.roles]:
            server = self.bot.get_server(ZEN_SERVER)
            await self.bot.remove_roles(
                ctx.message.author,
                self.get_role(server, UMM_ROLES['umm'])
            )

            display_name = getattr(ctx.message.author, 'nick') or \
                           getattr(ctx.message.author, 'name')

            await self.bot.send_message(
                server.get_channel(UMM_CHANNELS['lewd']),
                u'Umm.. {} left Club Lewd'.format(display_name)
            )

    @group(name='bewb', hidden=True, pass_context=True, no_pm=True)
    async def ummm(self, ctx: Context):
        """
        Ummm..
        """

        await self.bot.delete_message(ctx.message)

        if ctx.invoked_subcommand is not None:
            return

        if UMM_ROLES['ummm'] in [r.id for r in ctx.message.author.roles]:
            return

        server = self.bot.get_server(ZEN_SERVER)
        await self.bot.add_roles(
            ctx.message.author,
            self.get_role(server, UMM_ROLES['ummm'])
        )

        display_name = getattr(ctx.message.author, 'nick') or \
                       getattr(ctx.message.author, 'name')

        embed = Embed()
        embed.set_image(url='https://media.giphy.com/media/nOdUe5Fw7YK40/giphy.gif')
        embed.add_field(
            name='Ummm..',
            value=u'Welcome to Club Bewb, {}'.format(display_name),
        )

        await self.bot.send_message(
            server.get_channel(UMM_CHANNELS['extreme-lewd']),
            embed=embed
        )

    @ummm.command(name='leave', hidden=True, pass_context=True, no_pm=True)
    async def ummm_leave_command(self, ctx: Context):
        """
        Ummm..
        """

        if UMM_ROLES['ummm'] in [r.id for r in ctx.message.author.roles]:
            server = self.bot.get_server(ZEN_SERVER)
            await self.bot.remove_roles(
                ctx.message.author,
                self.get_role(server, UMM_ROLES['ummm'])
            )

            display_name = getattr(ctx.message.author, 'nick') or \
                           getattr(ctx.message.author, 'name')

            await self.bot.send_message(
                server.get_channel(UMM_CHANNELS['extreme-lewd']),
                u'Ummm.. {} left Club Bewb'.format(display_name)
            )


def setup(bot):
    bot.add_cog(Fun(bot))
    logger.info("Cog loaded: Fun")
