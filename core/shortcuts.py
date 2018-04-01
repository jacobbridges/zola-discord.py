from collections import OrderedDict
from typing import Union

from discord.ext.commands import Context


def get_alias_list(mapping: Union[dict, OrderedDict]) -> str:
    """
    Get a user friendly string for the list of available items and aliases.
    """
    role_mapping = {}
    alias_list = []

    # Fill the role mapping
    for item, role_id in mapping.items():
        if role_id not in role_mapping:
            role_mapping[role_id] = []
        role_mapping[role_id].append(item)

    # Create the list
    for _, items in role_mapping.items():
        string_ = ''
        string_ += items.pop(0)
        if items:
            string_ += ' ({})'.format(' or '.join(items))
        alias_list.append(string_)

    return ', '.join(alias_list)


def get_raw_arg(ctx: Context) -> str:
    """
    Get the contents of the message without the command invocation.
    """
    arg: str = ctx.message.content.replace(
        ctx.prefix + ctx.invoked_with + ' ',
        ''
    )
    arg.strip()
    return arg
