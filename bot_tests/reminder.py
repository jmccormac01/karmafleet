"""
Bot for converting EVE times to local timezones
"""
from datetime import datetime
from pytz import timezone
import discord
from discord.ext import commands
import asyncio

# pylint: disable=invalid-name

Client = discord.Client()
client = commands.Bot(command_prefix="!")

reminders = {}
async def reminder_handler(reminders):
    await client.wait_until_ready()
    while not client.is_closed:
        broke = False
        print('Checking reminders...')
        print(reminders)
        now = datetime.utcnow()
        for a in reminders:
            print('Checking for author {}'.format(a))
            for t in reminders[a]:
                if now > t:
                    print(a, reminders[a][t])
                    await client.send_message(a, reminders[a][t])
                    # remove the reminder from the list
                    del reminders[a][t]
                    broke = True
                    break
            if broke:
                break
        await asyncio.sleep(10)

@client.event
async def on_ready():
    """
    Simple print to say we're ready
    """
    print('Ready for remembering stuff...')

@client.event
async def on_message(message):
    """
    Handle incoming messages and convert time requests
    """
    sp = message.content.split()
    return_message = ""
    error_count = 0
    # check we want time conversion from eve time
    if len(sp) >= 3 and sp[0].lower() == '!reminder':
        author = message.author
        await client.delete_message(message)
        # split the command up
        reminder_time = datetime.strptime(sp[1], '%Y-%m-%dT%H:%M')
        note = ' '.join(sp[2:])
        if author not in reminders.keys():
            reminders[author] = {}
        reminders[author][reminder_time] = note
        print(reminders)

client.loop.create_task(reminder_handler(reminders))
client.run('NDk0OTQ2Mzg3ODM5MDI1MTYz.Do66Yw.nsleHS3S8UvbWdBugiDtPWHrIKY')
