"""
Potential additions to KramalFret
"""
from datetime import datetime
from pytz import timezone
import discord
from discord.ext import commands

# pylint: disable=invalid-name

class Jbot:
    """
    Bot contributions by James
    """

    def __init__(self, bot):
        """
        Initialise the bot
        """
        self.bot = bot
        self.tz_options = ['samoa', 'hawaii', 'marquesas', 'alaska', 'pacific',
                           'mountain', 'central', 'eastern', 'atlantic', 'saopaulo',
                           'azores', 'gb', 'paris', 'cairo', 'moscow', 'dubai',
                           'karachi', 'dhaka', 'bangkok', 'hongkong', 'tokyo',
                           'sydney', 'noumea', 'auckland']
    @staticmethod
    def _parse_evetime(evetime, error_count, return_message):
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

    def _parse_timezone(self, tz, error_count, return_message):
        """
        Parse the timezone to convert to
        """
        # handle timezones here
        if tz.lower().startswith('samoa'):
            print('Converting EVE to Pacific/Samoa')
            TZ = 'Pacific/Samoa'
        elif tz.lower().startswith('hawaii'):
            print('Converting EVE to US/Hawaii')
            TZ = 'US/Hawaii'
        elif tz.lower().startswith('marquesas'):
            print('Converting EVE to Pacific/Marquesas')
            TZ = 'Pacific/Marquesas'
        elif tz.lower().startswith('alaska'):
            print('Converting EVE to US/Alaska')
            TZ = 'US/Alaska'
        elif tz.lower().startswith('pacific'):
            print('Converting EVE to US/Pacific')
            TZ = 'US/Pacific'
        elif tz.lower().startswith('mountain'):
            print('Converting EVE to US/Mountain')
            TZ = 'US/Mountain'
        elif tz.lower().startswith('central'):
            print('Converting EVE to US/Central')
            TZ = 'US/Central'
        elif tz.lower().startswith('eastern'):
            print('Converting EVE to US/Eastern')
            TZ = 'US/Eastern'
        elif tz.lower().startswith('atlantic'):
            print('Converting EVE to Canada/Atlantic')
            TZ = 'Canada/Atlantic'
        elif tz.lower().startswith('saopaulo'):
            print('Converting EVE to America/Sao_Paulo')
            TZ = 'America/Sao_Paulo'
        elif tz.lower().startswith('azores'):
            print('Converting EVE to Atlantic/Azores')
            TZ = 'Atlantic/Azores'
        elif tz.lower().startswith('gb'):
            print('Converting EVE to GB')
            TZ = 'GB'
        elif tz.lower().startswith('paris'):
            print('Converting EVE to Europe/Paris')
            TZ = 'CET'
        elif tz.lower().startswith('cairo'):
            print('Converting EVE to Africa/Cairo')
            TZ = 'Africa/Cairo'
        elif tz.lower().startswith('moscow'):
            print('Converting EVE to Europe/Moscow')
            TZ = 'Europe/Moscow'
        elif tz.lower().startswith('dubai'):
            print('Converting EVE to Asia/Dubai')
            TZ = 'Asia/Dubai'
        elif tz.lower().startswith('karachi'):
            print('Converting EVE to Asia/Karachi')
            TZ = 'Asia/Karachi'
        elif tz.lower().startswith('dhaka'):
            print('Converting EVE to Asia/Dhaka')
            TZ = 'Asia/Dhaka'
        elif tz.lower().startswith('bangkok'):
            print('Converting EVE to Asia/Bangkok')
            TZ = 'Asia/Bangkok'
        elif tz.lower().startswith('hongkong'):
            print('Converting EVE to Hongkong')
            TZ = 'Hongkong'
        elif tz.lower().startswith('tokyo'):
            print('Converting EVE to Asia/Tokyo')
            TZ = 'Asia/Tokyo'
        elif tz.lower().startswith('sydney'):
            print('Converting EVE to Australia/Sydney')
            TZ = 'Australia/Sydney'
        elif tz.lower().startswith('noumea'):
            print('Converting EVE to Pacific/Noumea')
            TZ = 'Pacific/Noumea'
        elif tz.lower().startswith('auckland'):
            print('Converting EVE to Pacifc/Auckland')
            TZ = 'Pacific/Auckland'
        else:
            return_message += "Timezone not supported\n" \
                              "Supported timezones: {}".format(', '.join(self.tz_options))
            error_count += 1
            TZ = None
        return TZ, error_count, return_message

    @staticmethod
    def _evetime_of_request(hours, minutes):
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


    @commands.command(pass_context=True)
    async def evetime(self, ctx, *args: str):
        """
        Handle incoming messages and convert time requests
        """
        return_message = ""
        error_count = 0
        # get the author
        author = ctx.message.author
        # split the command up
        etime = args[0]
        tz = args[2]
        # parse the time part
        hours, minutes, error_count, \
        return_message = self._parse_evetime(etime,
                                             error_count,
                                             return_message)
        # if that shit all works ok, now attempt the tz conversion
        if error_count == 0:
            etime = self._evetime_of_request(hours, minutes)
            TZ, error_count, return_message = self._parse_timezone(tz, error_count, return_message)

            # once everything above is fine, do the actual conversion, or report on errors
            if error_count == 0:
                return_message = etime.astimezone(timezone(TZ)).strftime('%H:%M')
        em = discord.Embed(author=author, description=return_message)
        await self.bot.say(embed=em)
