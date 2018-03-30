import logging
from functools import wraps
from shlex import split

from discord import Member, User
from discord.ext.commands import Context, check

from .utils import parse_strings

logger = logging.getLogger(__name__)


def with_role(*role_ids: int):
    def predicate(ctx: Context):
        if type(ctx.message.author) is User:  # Return False in a DM
            logger.debug(f"{ctx.message.author} tried to use the '{ctx.command.name}'command from a DM. "
                         "This command is restricted by the with_role decorator. Rejecting request.")
            return False

        for role in ctx.message.author.roles:
            if role.id in role_ids:
                logger.debug(f"{ctx.message.author} has the '{role.name}' role, and passes the check.")
                return True

        logger.debug(f"{ctx.message.author} does not have the required role to use "
                     f"the '{ctx.command.name}' command, so the request is rejected.")
        return False
    return check(predicate)


def roles_one_of(roles):
    """
    Decorator which limits a command to only users with at least one of the
    specified roles.
    :param roles: List of role names.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(message, *args, **kwargs):
            if hasattr(message.author, 'roles'):
                for role in message.author.roles:
                    if role.name.lower() in roles:
                        return await func(message, *args, **kwargs)
            return False
        return wrapper
    return decorator


def roles_has_all(roles):
    """
    Decorator which limits a command to only users with all the specified
    roles.
    :param roles: List of role names.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(message, *args, **kwargs):
            if hasattr(message.author, 'roles'):
                has_all = all([r.name.lower() in roles
                              for r in message.author.roles])
                if has_all:
                    return await func(message, *args, **kwargs)
            return False
        return wrapper
    return decorator


def parse_command_args(func):
    """
    Decorator which parses arguments from a command (if a command is detected).
    """
    @wraps(func)
    async def wrapper(message, *args, **kwargs):
        if message.content.startswith('!'):
            args_ = split(message.content)
            args_.pop(0)  # Remove the command name from the argument list
            if len(args_) > 0:
                transformed_args = parse_strings(args_)
                kwargs.update({'command_args': transformed_args})
        return await func(message, *args, **kwargs)
    return wrapper
