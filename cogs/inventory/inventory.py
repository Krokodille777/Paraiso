import discord
from discord import app_commands
from discord.ext import commands
from cogs.inventory.catalog import available

ITEM_CHOICES = [app_commands.Choice(name=i, value=i) for i in available]  # max 25


class PlayerInventory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def has_profile(self, user_id: int) -> bool:
        async with self.bot.db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)) as cur:
            return await cur.fetchone() is not None

    @app_commands.command(name="inventory", description="Check your inventory")
    async def inventory(self, interaction: discord.Interaction):
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

    # Temporary test commands
    @app_commands.command(name="add_item", description="Add an item to your inventory")
    @app_commands.choices(item=ITEM_CHOICES)
    async def add_item(self, interaction: discord.Interaction, item: app_commands.Choice[str]):
        if not await self.has_profile(interaction.user.id):
            await interaction.response.send_message("You don't have a profile yet. Use /newuser to create one.", ephemeral=True)
            return

        await self.bot.db.execute("""
            INSERT INTO inventory (user_id, item, amount) VALUES (?, ?, 1)
            ON CONFLICT(user_id, item) DO UPDATE SET amount = amount + 1
        """, (interaction.user.id, item.value))
        await self.bot.db.commit()
        await interaction.response.send_message(f"{item.value} added to your inventory.", ephemeral=True)

    @app_commands.command(name="remove_item", description="Remove an item from your inventory")
    @app_commands.choices(item=ITEM_CHOICES)
    async def remove_item(self, interaction: discord.Interaction, item: app_commands.Choice[str]):
        cur = await self.bot.db.execute(
            "UPDATE inventory SET amount = amount - 1 WHERE user_id = ? AND item = ? AND amount > 0",
            (interaction.user.id, item.value),
        )
        if cur.rowcount == 0:   # no row was changed, so they don't have it
            await interaction.response.send_message(f"{item.value} is not in your inventory.", ephemeral=True)
            return

        await self.bot.db.execute("DELETE FROM inventory WHERE user_id = ? AND amount <= 0", (interaction.user.id,))
        await self.bot.db.commit()
        await interaction.response.send_message(f"{item.value} removed from your inventory.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerInventory(bot))