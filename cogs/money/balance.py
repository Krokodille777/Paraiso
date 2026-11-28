import discord
from discord.ext import commands
from discord import app_commands
from game.player import Player


def balance_embed(player: Player) -> discord.Embed:
    # Alternative to show_balance() from the CLI version of Py-City Remake.
    # A plain function (outside the class), so other cogs can import it.
    return discord.Embed(
        title=f"{player.username}'s Balance",
        description=f"💰 Money: ${player.get_money()}",
        color=discord.Color.green(),
    )


class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Check your balance")
    async def balance(self, interaction: discord.Interaction):
        player = await Player.load(self.bot.db, interaction.user.id)
        if player is None:
            await interaction.response.send_message("You don't have a profile yet. Use /newuser to create one.", ephemeral=True)
            return

        await interaction.response.send_message(embed=balance_embed(player), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Money(bot))
