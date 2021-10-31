# Coded and updated by : Antoine Le Bras

print(f'Starting bot...')

import os
import random
import io
import aiohttp
import sys
import asyncio

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from scipy.stats import hypergeom
from itertools import cycle
from _googleCchiant import googleConnect
from _boataouts import outils

print(f'Importing .env configuration...')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PATCH_NOTES = int(os.getenv('PATCH_NOTES'))
GCG_SHEET_KEY = os.getenv('GCG_SHEET_KEY')
BLABLA_CHANNEL = int(os.getenv('BLABLA_CHANNEL'))



bot = commands.Bot(command_prefix='master_')
status = cycle(['master_info', 
    'Banlist ?', 
    'GO GCG GO !!', 
    'Thinking...',
])
goat = '<:Goat:589352160207306753>'


@bot.event
async def on_ready():
    change_status.start()
    # best_player.start()
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )


#Change the game status of the bot every 10 secs
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


#Send a ranking of the best players (based on a google sheet)
@bot.command(name='ranking')
async def best_player(ctx):
    print(f'start ranking')
    gcg_best = googleConnect(GCG_SHEET_KEY, 'RANKING GCG')
    gcg_best.googleLogin()
    super_cleaner = outils()

    print(f'Collecting data from selected cells...')
    player_name = super_cleaner.clean(gcg_best.worksheet.get('B2')) #get the B2 cell of 'CLASSEMENT GCG'!
    print(f'{player_name}')
    db_ranking = super_cleaner.clean(gcg_best.worksheet.get('C2')) #get the C2 cell of 'CLASSEMENT GCG'!
    print(f'{db_ranking}')

    best_playerEmbed = discord.Embed(title=f'{goat} GCG\'s best player {goat}', description='Se relance toutes les 24h!', color=0x399494)
    best_playerEmbed.add_field(
        name=f'{player_name}{goat}',
        value=f'It\'s the best player of this week with {db_ranking} pts!'
    )
    channel = bot.get_channel(PATCH_NOTES) #def channel here with channel's ID
    await channel.send(embed=best_playerEmbed) #'NoneType' object has no attribute 'send'
    print(f'{player_name} a {db_ranking}pts\n'
    'best_player success')


#Ping
@bot.command(name='ping')
async def _ping(ctx):
    await ctx.message.delete()
    pingEmbed = discord.Embed(title=f'Ping of GCG_master {goat}', description=f'{round(bot.latency, 2)}')
    await ctx.send(embed=pingEmbed)
    print('Ping success')


#Display informations about bot's functions
@bot.command(name='info', help='Show help and function examples')
async def info(ctx):
    await ctx.message.delete()
    tutoEmbed = discord.Embed(title=f'{goat} Bot\'s help page {goat}', description='Command prefix \"master_\"', color=0x399494)
    tutoEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Ping',
        value='Let you check if the bot is correctly connected and ready to interact',
        inline=False
    )
    tutoEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Command roll_dice', 
        value='After writing the command with the correct prefix (\"master_roll_dice\"), you need to add the number of dice throw (with a number) then add the number of faces of the dice. Each value must be separated by a space.\n'
        'EXAMPLE : master_roll_dice 1 6\n'
        'The bot should send the result of one dice with six faces.',
        inline=False
    )
    tutoEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Commands test_prob and test_prob_dm',
        value='After writing the command with the correct prefix (\"master_test_prob\" or \"master_test_prob_dm\"), you need to add three numbers in the following order:\n'
        '\N{SMALL BLUE DIAMOND} Number of cards in the deck\n'
        '\N{SMALL BLUE DIAMOND} Number of cards drawn\n'
        '\N{SMALL BLUE DIAMOND} Number of targets in the deck\n'
        'The bot will send a recap of the data that were sent to him and the result from this data.\n'
        'EX1MPLE : master_test_stat 40 5 3\n'
        'I have a 40 cards deck, I\'m going to draw 5 cards and I have 3 target cards in my deck. The bot will send me the probability of drawing one, two and all the copies of the target card.\n'
        'The command \"master_test_prob_dm\" does the same thing but send the result in DMs.\n'
        '(source : https://stattrek.com/online-calculator/hypergeometric.aspx)',
        inline=False
    )
    tutoEmbed.set_footer(text=f'Bot coded by Antoine {goat}')
    await ctx.send(embed=tutoEmbed)
    print('Info success')


#Commande qui simule un dice roll
@bot.command(name='roll_dice', help='Simulate a dice throw')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    await ctx.message.delete()
    myEmbed = discord.Embed(title=f'Dice throw', color=0x1f1109)
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    myEmbed.add_field(name='Throws : ', value=', '.join(dice), inline=False)
    await ctx.send(embed=myEmbed)
    print('Roll success')


#Prob test
@bot.command(name='test_prob', help='Probability test')
async def test_prob(ctx, deck_size: int, numb_draw: int, numb_copy: int):
    await ctx.message.delete()
    myEmbed = discord.Embed(title=f'Probability test', description='Here is the result!', color=0x1eb473)
    myEmbed.add_field(
            name='\N{SMALL ORANGE DIAMOND} Recap :', 
            value=f'Deck size: {deck_size}\n'
            f'Number of card drawn: {numb_draw}\n'
            f'Number of target(s): {numb_copy}', 
            inline=False
        )

    x = min_success = 1
    M = deck_size
    n = numb_copy
    N = numb_draw

    for min_success in range(numb_draw):
        pval = hypergeom.sf(x-1, M, n, N)

        myEmbed.add_field(
                name='\N{SMALL ORANGE DIAMOND} Success rates', 
                value=f'- For {min_success+1} copy(ies) in starting hand: {round(pval*100, 2)}%'
            )

        x = x+1
        numb_copy = numb_copy-1
        deck_size = deck_size-1
        numb_draw = numb_draw-1
        if numb_copy == 0: break
        if numb_draw == 0: break
        if deck_size == 0: break

        myEmbed.set_footer(text=f'Provided by GCG_master {goat}')
    
    await ctx.send(embed=myEmbed)
    print('Tes_prob success')


#Prob test version DM
@bot.command(name='test_prob_dm', help='Probability test, sends it in DMs')
async def test_prob_dm(ctx, deck_size: int, numb_draw: int, numb_copy: int):
    await ctx.message.delete()
    myEmbed = discord.Embed(title=f'Probability test', description='Here is the result!', color=0x1eb473)
    myEmbed.add_field(
            name='\N{SMALL ORANGE DIAMOND} Recap :', 
            value=f'Deck size: {deck_size}\n'
            f'Number of card drawn: {numb_draw}\n'
            f'Number of target(s): {numb_copy}', 
            inline=False
        )

    x = min_success = 1
    M = deck_size
    n = numb_copy
    N = numb_draw

    for min_success in range(numb_draw):
        pval = hypergeom.sf(x-1, M, n, N)

        myEmbed.add_field(
                name='\N{SMALL ORANGE DIAMOND} Success rates', 
                value=f'- For {min_success+1} copy(ies) in starting hand: {round(pval*100, 2)}%'
            )

        x = x+1
        numb_copy = numb_copy-1
        deck_size = deck_size-1
        numb_draw = numb_draw-1
        if numb_copy == 0: break
        if numb_draw == 0: break
        if deck_size == 0: break

        myEmbed.set_footer(text=f'Provided by GCG_master {goat}')
    
    await ctx.author.send(embed=myEmbed)
    print('Test_prob_dm success')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command')

bot.run(TOKEN)