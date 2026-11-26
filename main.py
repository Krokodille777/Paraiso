import os
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEV_GUILD = discord.Object(id = 1170085207429370007)


class Monica(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.db = None

    async def setup_hook(self):

        self.db = await aiosqlite.connect("monica.db")
        self.db.row_factory = aiosqlite.Row
        await self.db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id  INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        balance  INTEGER NOT NULL DEFAULT 100
    )
""")
        await self.db.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        user_id INTEGER NOT NULL,
        item    TEXT    NOT NULL,
        amount  INTEGER NOT NULL DEFAULT 1,
        PRIMARY KEY (user_id, item)
    )
""")
        await self.db.commit()

        #Create a second database. It will store usernames and ids of users, who created a profile.
        


        await self.load_extension("cogs.user.user")
        await self.load_extension("cogs.money.balance")
        await self.load_extension("cogs.inventory.inventory")
        self.tree.copy_global_to(guild=DEV_GUILD)
        await self.tree.sync(guild=DEV_GUILD)

    async def close(self): # close the database connection when the bot is shutting down
        if self.db:
            await self.db.close()

        await super().close()

bot = Monica()
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")



@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.tree.command(name="hello", description="Says hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Welcome to the game!! \n " 
    "My name is Monica and for better or worse, \n I will be your guide through this journey. \n "
    "Hope you enjoy the stay!" )

bot.run(DISCORD_TOKEN)