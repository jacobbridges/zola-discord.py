from functools import wraps
from shlex import split

from .utils import parse_strings


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
