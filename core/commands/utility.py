import pydash

from ..decorators import roles_one_of, parse_command_args
from ..logger import logger


@roles_one_of(['zola--utils'])
@parse_command_args
async def command_clear(message, *args, **kwargs):
    client = command_clear.client
    if message.content.startswith('!clear'):
        logger.info('Run command !clear')

        # If no arguments were found for the command, clear the entire channel
        command_args = kwargs.get('command_args', [])
        if not command_args:
            logger.debug('No command arguments found')

            # Get all the messages in the channel
            messages = client.logs_from(message.channel)
            messages = [m async for m in messages]

            # Try bulk deleting the messages in chunks of 100
            for chunk in pydash.chunk(messages, 100):
                await client.delete_messages(chunk)
                messages = pydash.difference(messages, chunk)

            # Individually delete each message which could not be deleted
            # via bulk
            for message_ in messages:
                await client.delete_message(message_)

            return True

        # If arguments were found for the command, do different things
        else:
            command_args = list(command_args)
            logger.debug('Found command arguments: {}'.format(', '.join(map(str, command_args))))

            # If there is more than one argument, do nothing
            if len(command_args) > 1:
                return True

            # Save the first argument to a variable to readability
            clear_amount = command_args[0]

            # If the first argument is an integer, only clear so many messages
            if type(clear_amount) is int:

                # TODO: Support retrieving more than 100 messages
                # If clear_amount is greater than 100, send an apology
                if clear_amount > 100:
                    await client.send_message(
                        message.channel,
                        'I can only clear 100 messages at a time.'
                    )
                    return True

                # Get the messages to be deleted
                messages = client.logs_from(
                    message.channel, limit=clear_amount)
                messages = [m async for m in messages]

                # Try bulk deleting the messages in chunks of 100
                for chunk in pydash.chunk(messages, 100):
                    await client.delete_messages(chunk)
                    messages = pydash.difference(messages, chunk)

                # Individually delete each message which could not be deleted
                # via bulk
                for message_ in messages:
                    await client.delete_message(message_)

                return True

    return False
