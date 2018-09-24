"""
Bot for converting EVE times to local timezones
"""
from datetime import datetime
from pytz import timezone
import discord
from discord.ext import commands

# pylint: disable=invalid-name

Client = discord.Client()
client = commands.Bot(command_prefix="!")

def parse_evetime(evetime, error_count, return_message):
    """
    Parse the incoming EVE time
    """
    if len(evetime.split(':')) == 2:
        try:
            hours = int(evetime.split(':')[0])
        except (ValueError, IndexError):
            return_message += 'Fix the input time hours value\n'
            error_count += 1
            hours = None
        try:
            minutes = int(evetime.split(':')[1])
        except (ValueError, IndexError):
            return_message += 'Fix the input time minutes value\n'
            error_count += 1
            minutes = None
    else:
        hours, minutes = None, None
        error_count = 1
        return_message += "Fix the time format HH:MM\n"
    return hours, minutes, error_count, return_message

def parse_timezone(tz, error_count, return_message):
    """
    Parse the timezone to convert to
    """
    # handle timezones here
    if tz.lower().startswith('pacific'):
        print('Converting EVE to US/Pacific')
        TZ = 'US/Pacific'
    elif tz.lower().startswith('central'):
        print('Converting EVE to US/Central')
        TZ = 'US/Central'
    elif tz.lower().startswith('eastern'):
        print('Converting EVE to US/Eastern')
        TZ = 'US/Eastern'
    elif tz.lower().startswith('gmt'):
        print('Converting EVE to GMT')
        TZ = 'GMT'
    elif tz.lower().startswith('cet'):
        print('Converting EVE to CET')
        TZ = 'CET'
    elif tz.lower().startswith('nz'):
        print('Converting EVE to Pacifc/Auckland')
        TZ = 'Pacific/Auckland'
    else:
        return_message += "Timezone not supported\n"
        error_count += 1
        TZ = None
    return TZ, error_count, return_message

def evetime_of_request(hours, minutes):
    """
    Get the current eve time datetime object
    but using the hours and minutes requested
    in the conversion
    """
    now = datetime.utcnow()
    dt = "{}-{:02d}-{:02d}T{:02d}:{:02d}".format(now.year, now.month,
                                                 now.day, hours, minutes)
    dt_obj = datetime.strptime(dt, "%Y-%m-%dT%H:%M")
    evetime = dt_obj.replace(tzinfo=timezone('UTC'))
    return evetime

@client.event
async def on_ready():
    """
    Simple print to say we're ready
    """
    print('Ready for converting times...')

@client.event
async def on_message(message):
    """
    Hand incoming messages and convert time requests
    """
    sp = message.content.split()
    return_message = ""
    error_count = 0
    # check we want time conversion from eve time
    if len(sp) == 4 and sp[0].lower() == '!evetime' and sp[2].lower() == 'to':
        # split the command up
        evetime = sp[1]
        tz = sp[3]
        # parse the time part
        hours, minutes, error_count, \
        return_message = parse_evetime(evetime,
                                       error_count,
                                       return_message)
        # if that shit all works ok, now attempt the tz conversion
        if error_count == 0:
            evetime = evetime_of_request(hours, minutes)
            TZ, error_count, return_message = parse_timezone(tz, error_count, return_message)

            # once everything above is fine, do the actual conversion, or report on errors
            if error_count == 0:
                return_message = evetime.astimezone(timezone(TZ)).strftime('%H:%M')

        await client.send_message(message.channel, return_message)

client.run('NDkzODgwODM5NzM5MDE1MTY4.Dorbyg.P_uGDGr4YT0CFTqtLg2LRiA-yn4')
