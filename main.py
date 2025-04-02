import discord
import asyncio
from dotenv import load_dotenv
import os
from discord.ext import commands
from flask import Flask
from threading import Thread
import logging

# Konfiguracja podstawowego logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicjalizacja Flask dla Azure
app = Flask(__name__)

@app.route('/')
def health_check():
    return "🤖 Bot Discord działa poprawnie!", 200

# Konfiguracja bota 
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Bot {bot.user} jest online!')
    logger.info("------------------------------")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Nieznana komenda! Wpisz $help aby zobaczyć dostępne komendy.")
    else:
        logger.error(f"Błąd komendy: {error}")

@bot.command()
async def witaj(ctx):
    """Wita użytkownika z odpowiednimi uprawnieniami"""
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
        await ctx.send("❌ Za dużo pingów! Maksymalny czas ataku to 30 sekund.")
        return
    
    await ctx.send(f'🔫 Rozpoczęto atak na {member.mention}!')
    for _ in range(pings): 
        await asyncio.sleep(interval)
        await ctx.send(f'🚀 {member.mention}!')
    await ctx.send(f'✅ Atak na {member.mention} zakończony!')

@bot.command()
async def dawaj(ctx):
    """Dołącza bota do aktualnego kanału głosowego"""
    role_name = "KobotzkyOperator" 
    if not any(role.name == role_name for role in ctx.author.roles):
        await ctx.send("❌ Nie masz uprawnień do tej komendy!")
        return
     
    if ctx.author.voice is None:
        await ctx.send("❌ Musisz być na kanale głosowym, aby użyć tej komendy.")
        return
    
    try:
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        await ctx.send(f'🎧 Bot dołączył do kanału {voice_channel.name}!')
    except discord.ClientException as e:
        logger.error(f"Błąd łączenia z kanałem głosowym: {e}")
        await ctx.send("❌ Bot jest już połączony z kanałem głosowym!")

def run_flask():
    """Uruchamia serwer Flask dla Azure Health Check"""
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    """Uruchamia bota Discord"""
    load_dotenv()
    TOKEN = os.getenv("DISCORD_BOT_KOBOTZKY_TOKEN")
    
    if not TOKEN:
        logger.error("❌ Nie znaleziono tokenu Discord! Sprawdź zmienne środowiskowe.")
        return
    
    bot.run(TOKEN)

if __name__ == '__main__':
    logger.info("Uruchamianie aplikacji...")
    
    # Uruchomienie Flask w osobnym wątku
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Uruchomienie bota w głównym wątku
    try:
        run_bot()
    except Exception as e:
        logger.error(f"Krytyczny błąd bota: {e}")
    finally:
        logger.info("Zamykanie aplikacji...")