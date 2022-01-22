# bot.py
import os
from datetime import datetime, timedelta
import pytz

import discord
from discord.ext import commands
from dotenv import load_dotenv

frontline_dictionary = {
    0: ['  The Borderland Ruins (Secure)', None],
    1: ['  Seal Rock (Seize)', None],
    2: ['  The Fields of Glory (Shatter)', None],
    3: ['  Onsal Hakair (Danshig Naadam)', None]
}


def get_duration(then, now=datetime.now(), interval="default"):
    # Returns a duration as specified by variable interval
    # Functions, except total_duration, returns [quotient, remainder]

    duration = now - then  # For build-in functions
    duration_in_s = duration.total_seconds()

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(t_seconds=None):
        return divmod(t_seconds if t_seconds is not None else duration_in_s, 86400)  # Seconds in a day = 86400

    def hours(t_seconds=None):
        return divmod(t_seconds if t_seconds is not None else duration_in_s, 3600)  # Seconds in an hour = 3600

    def minutes(t_seconds=None):
        return divmod(t_seconds if t_seconds is not None else duration_in_s, 60)  # Seconds in a minute = 60

    def seconds(t_seconds=None):
        if t_seconds is not None:
            return divmod(t_seconds, 1)
        return duration_in_s

    def total_duration():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
        h = hours(d[1])
        m = minutes(h[1])
        s = seconds(m[1])

        return "{}d {}h {}m {}s".format(int(d[0]), int(h[0]), int(m[0]), int(s[0]))

    return {
        'days': int(days()[0]),
        'hours': int(hours()[0]),
        'minutes': int(minutes()[0]),
        'seconds': int(seconds()),
        'default': total_duration()
    }[interval]


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='fl', help='Lists the Frontline map rotation with time until each map')
async def frontline_table(ctx):
    d0 = datetime(2021, 11, 15, 7, 0, 0)
    timezone = pytz.timezone("US/Pacific")
    with_timezone = timezone.localize(d0)
    utc_d0 = with_timezone.astimezone(pytz.utc)

    utc_d1 = datetime.now(tz=pytz.utc)

    delta = utc_d1 - utc_d0

    out_table = '```\n'
    for map_k in range(4):
        if delta.days % 4 == map_k:
            break

    for k, v in frontline_dictionary.items():
        map_name, time_remaining = v
        if delta.days % 4 == k:
            map_name = '>' + map_name[1:]
            time_remaining = 'Now'
        else:
            add_day = k - map_k
            if add_day < 0:
                add_day += 4
            if utc_d1.hour < 15:
                rel_d0 = utc_d1 + timedelta(days=add_day - 1)
            else:
                rel_d0 = utc_d1 + timedelta(days=add_day)
            rel_d0 = rel_d0.replace(hour=15, minute=0, second=0, microsecond=0)
            time_remaining = get_duration(utc_d1, rel_d0)
        out_table += '{:<31}\t\t{:<15}\n'.format(map_name, time_remaining)
    out_table += '```'
    response = out_table
    await ctx.send(response)


@bot.command(name='onsal', help='Copypasta to express your excitement for Onsal')
async def onsal_copypasta(ctx):
    msg = "Onsal just :ok_hand: so perfect :stuck_out_tongue_winking_eye::kissing_closed_eyes::smiling_face_with_3_hearts:. I :boy: get :sleepy: decent WR on :snowman2: it. Games :video_game: are fun :smiley: even :crescent_moon: when :soon: you :love_you_gesture: lose. :x: Efficient games :space_invader: lead :point_right: to easy :weary: win :checkered_flag: and inefficient games :8ball: lead :point_right: to 10000 years :hot_face: mid :unamused: fight. :punch: :right_facing_fist: Not :do_not_litter: too :cry: much :rofl: running. :dash: No :persevere: cheesy :pizza: tactics. green :green_circle: grass and next :track_next: to beach. \uD83C\uDFC4 good :ok_hand: music. :notes:"
    response = msg
    await ctx.send(response)


@bot.command(name='secure', help='Copypasta to express your disappointment for Borderland Ruins')
async def bruins_copypasta(ctx):
    msg = "Secure :lock: just :face_vomiting: so trash :wastebasket::x::x:. Games :video_game:are not :man_gesturing_no:fun and it's best :ok_hand: to just :joy: :zzz::zzz:sleep in :person_in_bed_tone4:. You :flushed: can't even go up :arrow_up_small::up: without having :yum::point_right:to deal with golfers:person_golfing::golf:. Not only that :clap::clap::clap:, there's a ledge :ok_hand::eggplant: that people :people_holding_hands:  stand on to limp :gun: :sweat_drops: your entire team :triumph: :triumph: and nobody :no_entry_sign: can stop :octagonal_sign:  them! When :confounded:it's not :no_entry_sign: top :point_up:phase teams :basketball: just ping pong :ping_pong: back :arrow_left: and forth :arrow_right:  from one base :office: to another. I can't get off :lips::eggplant::sweat_drops:to this. This isn't fun :smile: :fire: - there's dumb :stuck_out_tongue_winking_eye: cheesy :cheese: tactics, there's no :sunny::fearful: green grass :ear_of_rice:, no beach dates:seal: :kissing_heart:, and only ruins :house_abandoned::face_vomiting:. Ruins to represent the ruined game :bomb::video_game: I am having."
    response = msg
    await ctx.send(response)


@bot.command(name='weeklyfl', help='Snapshot of weekly leaderboard rankings for Primal Frontlines')
async def screen_grab(ctx):
    with open('screenshot.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)

bot.run(TOKEN)

