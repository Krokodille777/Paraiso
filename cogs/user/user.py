import discord
from discord.ext import commands
from discord import app_commands
import sqlite3


class SignupModal(discord.ui.Modal, title="Create your player profile"):
    username = discord.ui.TextInput(label="username", placeholder="Enter your username",
                                    min_length=1, max_length=20)

    async def on_submit(self, interaction: discord.Interaction):
        name = self.username.value.strip()
        if not name.isalnum():
            await interaction.response.send_message("Letters and numbers only.", ephemeral=True)
            return

        db = interaction.client.db
        try:
            await db.execute("INSERT INTO users (user_id, username) VALUES (?, ?)",
                             (interaction.user.id, name))
            await db.commit()
        except sqlite3.IntegrityError:
            # Fires if this Discord user already has a profile, or the username is taken
            await interaction.response.send_message(
                "You already have a profile, or that username is taken.", ephemeral=True)
            return

        embed = discord.Embed(title="Player Profile Created",
                              description=f"Welcome {name}!", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)



class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name = "newuser", description = "Creates your player profile for the game.")
    async def newuser(self,interaction: discord.Interaction):
        modal = SignupModal()
        await interaction.response.send_modal(modal)

    @app_commands.command(name = "deleteuser", description = "Deletes your player profile for the game.")
    async def deleteuser(self, interaction: discord.Interaction):
        db = self.bot.db
        async with db.execute("SELECT username FROM users WHERE user_id = ?", (interaction.user.id,)) as cursor:
            row = await cursor.fetchone()

        if row is None:
            await interaction.response.send_message("You don't have a profile to delete.", ephemeral=True)
            return

        await db.execute("DELETE FROM users WHERE user_id = ?", (interaction.user.id,))
        await db.commit()

        embed = discord.Embed(title="Player Profile Deleted",
                              description=f"Goodbye {row['username']}!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)

    #This command returns the okayer's information, sech as their usernames, balance and other information.
    @app_commands.command(name = "profile", description = "Check your player profile for the game.")
    async def profile(self, interaction: discord.Interaction):
        db = self.bot.db
        async with db. execute("SELECT username, balance FROM users WHERE user_id = ?", (interaction.user.id,)) as cursor:
            row = await cursor.fetchone()

        if row is None:
            await interaction.response.send_message("You don't have a profile yet. Use /newuser to create one.", ephemeral=True)
            return

        embed = discord.Embed(title="Player Profile",
                              description=f"Your username is {row['username']}. \n Balance: {row['balance']}", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(User(bot))
