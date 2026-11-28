import discord
from discord.ext import commands
from discord import app_commands
from game.player import Player
from cogs.inventory.catalog import available
from cogs.money.balance import balance_embed
import time


class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @app_commands.command(name = "buy", description = "Buy an item (or a set of items) from the shoplist")
    @app_commands.describe(item_name = "The item you want to buy", quantity = "The amount of the item you want to buy")
    async def buy(self, interaction: discord.Interaction, item_name: str, quantity: int):
        item_name = item_name.lower().strip()
        player = await Player.load(self.bot.db, interaction.user.id)
        if player is None:
            await interaction.response.send_message("You don't have a profile yet. Use /newuser to create one.", ephemeral=True)
            return
        
        item = available.get(item_name.lower())
        if item is None:
            await interaction.response.send_message(f"Item'{item_name}' is not availablie in the shop")
            return
        if quantity <= 0:
            await interaction.response.send_message("Invalid quality. Please enter a positive integer")
            return

        price = item["price"]
        total_cost = price * quantity
        if player.get_money() < total_cost:
            await interaction.response.send_message("Not enough money to buy this item.")
            await interaction.followup.send(embed=balance_embed(player), ephemeral=True)
            return

        player.set_money(player.get_money() - total_cost)
        player.inventory[item_name] = player.inventory.get(item_name, 0) + quantity
        await player.save(self.bot.db)
        await interaction.response.send_message(f"Bought {quantity} {item_name}(s) for ${total_cost}")

        if item_name in ["house", "car", "suitcase"]:
            player.set_happiness(min(100, player.get_happiness() + item["happiness"]))
            await player.save(self.bot.db)
            await interaction.followup.send(f"Your happiness increased by {item['happiness']} points. Current happiness: {player.get_happiness()}")

        if item["type"] in ["food", "drink"]:
            player.bought_at.setdefault(item_name, []).extend([time.time()] * quantity)
        await player.save(self.bot.db)
        await interaction.followup.send(embed=balance_embed(player))


    @app_commands.command(name = "sell", description = "Sell an item (or a set of items) from your inventory")
    @app_commands.describe(item_name = "The item you want to sell", quantity = "The amount of the item you want to sell")
    async def sell(self, interaction: discord.Interaction, item_name: str, quantity: int):
        
        item_name = item_name.lower().strip()
        player = await Player.load(self.bot.db, interaction.user.id)
        if player is None:
            await interaction.response.send_message("You don't have a profile yet. Use /newuser to create one.", ephemeral=True)
            return
        is_expired = item_name.startswith("expired")
        item = available.get(item_name.removeprefix("expired "))
        if item is None:
            await interaction.response.send_message(f"Item '{item_name}' is not available for sale.")
            return
        if quantity <= 0:
            await interaction.response.send_message("Invalid quantity. Please enter a positive integer.")
            return
        if player.inventory.get(item_name, 0) < quantity:
            await interaction.response.send_message("You don't have enough of that item to sell.")
            return

        if is_expired:
            total_earnings = item["price"] * quantity // 4
        else: 
            total_earnings = item["price"] * quantity // 2
            times = player.bought_at.get(item_name, [])
            del times[:quantity]

        player.set_money(player.get_money() + total_earnings)
        player.inventory[item_name] -= quantity
        if player.inventory[item_name] <= 0:
            del player.inventory[item_name]
        await player.save(self.bot.db)
        await interaction.response.send_message(f"Sold {quantity} {item_name}(s) for ${total_earnings}.")
        await interaction.followup.send(embed=balance_embed(player))


async def setup(bot: commands.Bot):
    await bot.add_cog(Trade(bot))