import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View
#This is a test version of the shop list. It will be updated in the future with more items and features.
available ={
    #food & drink
    "apple": {"price": 2, "type": "food", "health": 5, "energy": 10, "hunger": -2, "shell_life": 10},
    "orange": {"price": 3, "type": "food", "health": 7, "energy": 15, "hunger": -3, "shell_life": 12},
    "banana": {"price": 2, "type": "food", "health": 3, "energy": 5, "hunger": -2, "shell_life": 11},
    "coffee": {"price": 8, "type": "drink", "health": 0, "energy": 20, "hunger": -1, "shell_life": 300},
    "cake": {"price": 40, "type": "food", "health": 10, "energy": 30, "hunger": -5, "shell_life": 250},
    #activities & usable items
    "book": {"price": 50, "type": "book", "happiness": 5, "intelligence": 0.5, "desc": "Read a book to increase your intelligence and happiness."},
    "anime": {"price": 30, "type": "watch", "happiness": 10, "perception": 0.5, "desc": "Watch an anime to increase your happiness."},
    "giftbox": {"price": 100, "type": "usable", "desc": "Open a gift box to receive a random item."},
    "house": {"price": 5000, "type": "booster", "desc": "Boosts your salary "},
    "car": {"price": 2500, "type": "booster", "desc": "Boosts your salary"},
    #collectibles
    "diamond": {"price": 1000, "type":"collectible", "desc": "A shiny thingy everyone wants. BE careful, though. You'll become wanted by thieves if you have it"}
}

#Pagination settings for the shop list like in CLI version.
#Each page will be formed by type of item, and each page will have a maximum of 10 items. If there are more than 10 items of a certain type, the user will be able to navigate through the pages using buttons.
ITEMS_PER_PAGE = 10

def form_pages_by_type(available_items):
        groups = {}

        for item, details in available_items.items():
            groups.setdefault(details.get("type", "misc", ), []).append((item, details))

        pages = []
        for item_type, items in groups.items():
            parts = [items[i:i + ITEMS_PER_PAGE] for i in range(0, len(items), ITEMS_PER_PAGE)]
            for part_number, part in enumerate(parts, start = 1):
                pages.append((item_type, part_number, len(parts), part))

        return pages

def format_items(item, details):
        line = f"-{item}: ${details["price"]}"
        if "health" in details or "energy" in details:
            line += f" | Health: {details.get('health', 0)}, Energy: {details.get('energy', 0)}"
        if "hunger" in details:
            line += f" | Hunger: {details.get('hunger', 0)}"
        if "happiness" in details:
            line += f" | Happiness: {details.get('happiness', 0)}"
        if "intelligence" in details:
            line += f" | Intelligence: {details.get('intelligence', 0)}"
        if "perception" in details:
            line += f" | Perception: {details.get('perception', 0)}"
        if "shell_life" in details:
            line += f" | Shell Life: {details["shell_life"]} seconds"
        if "desc" in details:
            line += f" | Description: {details["desc"].strip()}"

        return line

def build_embed(pages: list, index: int) -> discord.Embed:
    item_type, number, total, items = pages[index]
    embed = discord.Embed(
        title = f"Shop List - {item_type.capitalize()} (Page {number}/{total})",
        description = "\n".join(format_items(item, details) for item, details in items),
        color = discord.Color.blue()
    )
    embed.set_footer(text="Use the buttons below to navigate through the pages.")
    return embed


class ShopListView(View):
    def __init__(self, pages: int):
        super().__init__(timeout= 100)
        self.pages = pages
        self.index = 0
        self.message = None
        self.update_buttons()
    def update_buttons(self):
        self.prev_button.disabled = self.index == 0
        self.next_button.disabled = self.index == len(self.pages) - 1

    @discord.ui.button(label = "Previous", style = discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.button):
        self.index -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed = build_embed(self.pages, self.index), view = self)

    @discord.ui.button(label = "Next", style = discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.button):
        self.index += 1
        self.update_buttons()
        await interaction.response.edit_message(embed = build_embed(self.pages, self.index), view = self)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            await self.message.edit(view = self)


class ShopList(commands.Cog):
    def  __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pages = form_pages_by_type(available)

    @app_commands.command(name="shoplist", description="View the shop list")
    async def shoplist(self, interaction: discord.Interaction):
        view = ShopListView(self.pages)
        await interaction.response.send_message(
            embed = build_embed(self.pages, 0),
            view = view, ephemeral = True
        )
        view.message = await interaction.original_response()
    


async def setup(bot: commands.Bot):
    await bot.add_cog(ShopList(bot))
