import discord
from discord import app_commands
from discord.ext import commands
from cogs.inventory.catalog import available
from game.player import Player

ITEM_CHOICES = [app_commands.Choice(name=i, value=i) for i in available]  # max 25


class PlayerInventory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def has_profile(self, user_id: int) -> bool:
        async with self.bot.db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as cur:
            return await cur.fetchone() is not None

    @app_commands.command(name="inventory", description="Check your inventory")
    async def inventory(self, interaction: discord.Interaction):
        player = await Player.load(self.bot.db, interaction.user.id)
        if player is None:
            await interaction.response.send_message("You don't have a profile yet. Use /newuser to create one.", ephemeral=True)
            return
        if not await self.has_profile(interaction.user.id):
            await interaction.response.send_message("You don't have a profile yet. Use /newuser to create one.", ephemeral=True)
            return

        async with self.bot.db.execute(
            "SELECT item, amount FROM inventory WHERE user_id = ? ORDER BY item", (interaction.user.id,)
        ) as cur:
            rows = await cur.fetchall()

        if not rows:
            await interaction.response.send_message("Your inventory is empty.", ephemeral=True)
            return

        lines = "\n".join(f"{r['item']} x{r['amount']}" for r in rows)
        embed = discord.Embed(title="Your Inventory", description=lines, color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerInventory(bot))