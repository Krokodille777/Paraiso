import discord
from discord.ext import commands
from discord import app_commands
from game.player import Player


class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "balance", description = "Check your balance")
    async def balance(self, interaction: discord.Interaction):
        player = await Player.load(self.bot.db, interaction.user.id)
        if player is None:
            await interaction.response.send_message("You don't have a profile yet. Use /newuser to create one.", ephemeral=True)
            return


        async with self.bot.db.execute("SELECT money FROM users WHERE user_id = ?", (interaction.user.id,)) as cursor:
            row = await cursor.fetchone()

        if row is None:
            await interaction.response.send_message("You don't have a peofile yet. Use /newuser to create one.", ephemeral=True)
            return

        embed = discord.Embed(title = "balance", 
                              description = f"Your have {player.get_money()} coins.", 
                              color = discord.Color.blue())
        await interaction.response.send_message(embed = embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Money(bot))