import discord
import asyncio
from dotenv import load_dotenv
import os
from discord.ext import commands

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is online!')
    print("------------------------------")



@bot.command()
async def witaj(ctx):
    role_name = "KobotzkyOperator" 
    if not any(role.name == role_name for role in ctx.author.roles):
        await ctx.send("❌ Nie masz uprawnień do tej komendy!")
        return
    await ctx.send(f'Witaj {ctx.author.mention}!')


@bot.command(help="Atakuje wybranego użytkownika, pingując go określoną ilość razy.")
async def attack(ctx, member: discord.Member, pings: int = 5, interval: float = 1.0):
    role_name = "KobotzkyOperator" 
    if not any(role.name == role_name for role in ctx.author.roles):
        await ctx.send("❌ Nie masz uprawnień do tej komendy!")
        return
    
    total_time = pings * interval
    if total_time > 30:
        await ctx.send("❌ Za dużo pingów!")
        return
    
    await ctx.send(f'🔫 Rozpoczęto atak na {member.mention}!')
    for _ in range(pings): 
        await asyncio.sleep(interval)
        await ctx.send(f'🚀 {member.mention}!')
    await ctx.send(f'✅ Atak na {member.mention} zakończony!')

@bot.command()
async def dawaj(ctx):
    role_name = "KobotzkyOperator" 
    if not any(role.name == role_name for role in ctx.author.roles):
        await ctx.send("❌ Nie masz uprawnień do tej komendy!")
        return
     
    member = ctx.author  # Użytkownik, który wywołuje komendę

    # Sprawdzamy, czy użytkownik jest na jakimś kanale głosowym
    if member.voice is None:
        await ctx.send("❌ Musisz być na kanale głosowym, aby użyć tej komendy.")
        return
    
    # Próba połączenia z kanałem głosowym
    voice_channel = member.voice.channel
    await voice_channel.connect()  # Dołączamy do kanału
    await ctx.send(f'🎧 Bot dołączył do kanału {voice_channel.name}.')

#token

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_KOBOTZKY_TOKEN")

if TOKEN is None:
    print("❌ Nie udało się załadować tokena. Sprawdź plik .env!")

bot.run(TOKEN)