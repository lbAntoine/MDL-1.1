# gcgmaster.py - BOT Discord server origin : GCG
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
'Je me sens un peu seul',
'PEND BEST DECK!',])
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


#Change le game status du bot toutes les 10 secs (les statuts sont contenus dans le cycle)
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


#Envoi le joueur N1 de la GCG et son ranking DB toutes les 24h
@bot.command(name='classement')
async def best_player(ctx):
    print(f'debut classement')
    gcg_best = googleConnect(GCG_SHEET_KEY, 'CLASSEMENT GCG')
    gcg_best.googleLogin()
    super_cleaner = outils()

    print(f'Collecting data from selected cells...')
    player_name = super_cleaner.clean(gcg_best.worksheet.get('B2')) #get the B2 cell of 'CLASSEMENT GCG'!
    print(f'{player_name}')
    db_ranking = super_cleaner.clean(gcg_best.worksheet.get('C2')) #get the C2 cell of 'CLASSEMENT GCG'!
    print(f'{db_ranking}')

    best_playerEmbed = discord.Embed(title=f'{goat} Le meilleur joueur GCG {goat}', description='Se relance toutes les 24h!', color=0x399494)
    best_playerEmbed.add_field(
        name=f'{player_name}{goat}',
        value=f'C\'est le meilleur joueur de la GCG aujourd\'hui avec {db_ranking} pts de ranking DB!'
    )
    channel = bot.get_channel(PATCH_NOTES) #def channel here with channel's ID
    await channel.send(embed=best_playerEmbed) #'NoneType' object has no attribute 'send'
    print(f'{player_name} a {db_ranking}pts\n'
    'best_player success')


#Ping du bot
@bot.command(name='ping')
async def _ping(ctx):
    await ctx.message.delete()
    pingEmbed = discord.Embed(title=f'Ping de GCG_master {goat}', description=f'{round(bot.latency, 2)}')
    await ctx.send(embed=pingEmbed)
    print('Ping success')


#Display les commandes du bot
@bot.command(name='info', help='Montre comment utiliser les différentes commandes avec des exemples')
async def info(ctx):
    await ctx.message.delete()
    tutoEmbed = discord.Embed(title=f'{goat} Tutoriel des commandes GCG_master {goat}', description='Préfixe de commande \"master_\"', color=0x399494)
    tutoEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Commande ping',
        value='Permet de vérifier si le bot est bien en ligne et son ping',
        inline=False
    )
    tutoEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Commande roll_dice', 
        value='Après avoir écrit la commande avec le préfixe (\"master_roll_dice\"), il faut indiquer le nombre de jets (avec un chiffre) puis le nombre de faces du dé. Chaque valeur doit être séparée par un espace.\n'
        'EXEMPLE : master_roll_dice 1 6\n'
        'Le bot renverra donc le résultat d\'un jet de dé à 6 faces.',
        inline=False
    )
    tutoEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Commandes test_prob et test_prob_dm',
        value='Après avoir écrit la commande avec le préfixe (\"master_test_prob\" ou \"master_test_prob_dm\"), il faut indiquer les valeurs de trois éléments dans l\'ordre suivant :\n'
        '\N{SMALL BLUE DIAMOND} Nombre de cartes dans le deck\n'
        '\N{SMALL BLUE DIAMOND} Nombre de cartes piochées\n'
        '\N{SMALL BLUE DIAMOND} Nombre de cartes cibles dans le deck\n'
        'Le bot renverra un récapitulatif des données envoyées et le résultats impliquant ces données.\n'
        'EXEMPLE : master_test_stat 40 5 3\n'
        'J\'ai 40 cartes dans le deck, je vais piocher 5 cartes et j\'ai trois cartes cibles dans mon deck (3 TGU par exemple). Le bot me donnera le pourcentage de réussites de toucher une de ces 3 cartes, puis deux, puis trois.\n'
        'La fonction \"master_test_prob_dm\" effectue la même chose, mais le résultat vous sera envoyé dans vos DM plutôt que dans le chat du serveur.\n'
        'Le calcul est fait selon la formule de distribution hypergéométrique (source : https://stattrek.com/online-calculator/hypergeometric.aspx)',
        inline=False
    )
    tutoEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Suggestions',
        value='N\'hésitez pas à me DM en cas de soucis ou si vous avez des idées de nouvelles fonctions que je pourrais implémenter au bot !\n'
        'Le bot est codé en python et fonctionne grâce aux API discord de la librairie discord.py\n'
        'J\'espère que vous l\'utiliserez beaucoup et qu\'il vous plait ! :)\n'
        f'{PATCH_NOTES}',
        inline=False
    )
    tutoEmbed.set_footer(text=f'Bot programmé par (GCG)Antoine {goat}')
    await ctx.send(embed=tutoEmbed)
    print('Info success')


#Commande qui simule un dice roll
@bot.command(name='roll_dice', help='Simule un lancé de dés')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    await ctx.message.delete()
    myEmbed = discord.Embed(title=f'Lancé de dés', color=0x1f1109)
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    myEmbed.add_field(name='Jets : ', value=', '.join(dice), inline=False)
    await ctx.send(embed=myEmbed)
    print('Roll success')


#Prob test
@bot.command(name='test_prob', help='Lance un test de probabilité')
async def test_prob(ctx, deck_size: int, numb_draw: int, numb_copy: int):
    await ctx.message.delete()
    myEmbed = discord.Embed(title=f'Test de probabilité', description='Voici le résultat !', color=0x1eb473)
    #min_success input - not needed cause we admit that min_success is always = 1
    #formule (discret): pval = hypergeom.sf(x-1, M, n, N)
    myEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Récapitulatif :', 
        value=f'Taille du deck : {deck_size}\n'
        f'Nombres de cartes piochées : {numb_draw}\n'
        f'Nombres de copies de la cible : {numb_copy}', 
        inline=False
        )

    x = min_success = 1
    M = deck_size
    n = numb_copy
    N = numb_draw

    for min_success in range(numb_draw):
        pval = hypergeom.sf(x-1, M, n, N)

        #print(f'Pour {min_success+1} copie(s) en main de départ : {round(pval*100, 2)}%')
        #pas obliger de le print pour éco le serveur

        myEmbed.add_field(
            name='\N{SMALL ORANGE DIAMOND} Chance de réussite', 
            value=f'- Pour {min_success+1} copie(s) en main de départ : {round(pval*100, 2)}%'
            )

        x = x+1
        numb_copy = numb_copy-1
        deck_size = deck_size-1
        numb_draw = numb_draw-1
        if numb_copy == 0: break
        if numb_draw == 0: break
        if deck_size == 0: break
        #if min_success == numb_copy: break
        #if min_success == 0: break

        myEmbed.set_footer(text=f'Provided by GCG_master {goat}')
    
    await ctx.send(embed=myEmbed)
    print('Tes_prob success')


#Prob test version DM
@bot.command(name='test_prob_dm', help='Lance un test de probabilité et l\'envoie dans vos DM')
async def test_prob_dm(ctx, deck_size: int, numb_draw: int, numb_copy: int):
    await ctx.message.delete()
    myEmbed = discord.Embed(title=f'Test de probabilité', description='Voici le résultat !', color=0x1eb473)
    #min_success input - not needed cause we admit that min_success is always = 1
    #formule (discret): pval = hypergeom.sf(x-1, M, n, N)
    myEmbed.add_field(
        name='\N{SMALL ORANGE DIAMOND} Récapitulatif :', 
        value=f'Taille du deck : {deck_size}\n'
        f'Nombres de cartes piochées : {numb_draw}\n'
        f'Nombres de copies de la cible : {numb_copy}', 
        inline=False
        )

    x = min_success = 1
    M = deck_size
    n = numb_copy
    N = numb_draw

    for min_success in range(numb_draw):
        pval = hypergeom.sf(x-1, M, n, N)

        #print(f'Pour {min_success+1} copie(s) en main de départ : {round(pval*100, 2)}%')
        #pas obliger de le print pour éco le serveur super

        myEmbed.add_field(
            name='\N{SMALL ORANGE DIAMOND} Chance de réussite', 
            value=f'- Pour {min_success+1} copie(s) en main de départ : {round(pval*100, 2)}%'
            )

        x = x+1
        numb_copy = numb_copy-1
        deck_size = deck_size-1
        numb_draw = numb_draw-1
        if numb_copy == 0: break
        if numb_draw == 0: break
        if deck_size == 0: break
        #if min_success == numb_copy: break
        #if min_success == 0: break

        myEmbed.set_footer(text=f'Provided by GCG_master {goat}')
    
    await ctx.author.send(embed=myEmbed)
    print('Test_prob_dm success')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command')

bot.run(TOKEN)