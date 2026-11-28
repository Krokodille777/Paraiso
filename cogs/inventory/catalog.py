import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View
#This is a test version of the shop list. It will be updated in the future with more items and features.
available ={
    #food & drink
    "apple" : {"price" : 2, "type": "food", "health": 5, "energy": 10, "shelf_life": 5, "hunger": -2},
    "orange" : {"price" : 3, "type": "food", "health": 7, "energy": 12, "shelf_life": 300, "hunger": -3},
    "coffee" : {"price" : 8, "type": "drink", "health": 0, "energy": 20, "shelf_life": 600, "hunger": -1},
    "banana" : {"price" : 2, "type": "food", "health": 6, "energy": 15, "shelf_life": 300, "hunger": -2},
    "potato" : {"price" : 1, "type": "food", "health": 4, "energy": 8, "shelf_life": 300, "hunger": -1},
    "bread" : {"price" : 3, "type": "food", "health": 8, "energy": 15, "shelf_life": 600, "hunger": -7},
    "wine" : {"price" : 10, "type": "drink", "health": -5, "energy": 5, "shelf_life": 3600, "hunger": 0},
    "water" : {"price" : 1, "type": "drink", "health": 0, "energy": 5, "shelf_life": 3600, "hunger": 0},
    "cheese" : {"price" : 15, "type": "food", "health": 10, "energy": 15, "shelf_life": 500, "hunger": -5},
    "hotdog" : {"price" : 25, "type": "food", "health": 10, "energy": 20, "shelf_life": 600, "hunger": -9},
    "burger" : {"price" : 30, "type": "food", "health": 15, "energy": 25, "shelf_life": 600, "hunger": -12},
    "tomato" : {"price" : 2, "type": "food", "health": 5, "energy": 10, "shelf_life": 300, "hunger": -2},
    "lettuce" : {"price" : 2, "type": "food", "health": 5, "energy": 10, "shelf_life": 300, "hunger": -2},
    "chocolate" : {"price" : 15, "type": "food", "health": 5, "energy": 15, "shelf_life": 600, "hunger": -5},
    "energy_drink" : {"price" : 30, "type": "drink", "health": -5, "energy": 50, "shelf_life": 3600, "hunger": 0},
    "beer" : {"price" : 12, "type": "drink", "health": -10, "energy": 10, "shelf_life": 3600, "hunger": 0},
    "cake" : {"price" : 40, "type": "food", "health": 10, "energy": 30, "shelf_life": 600, "hunger": -17},
    "pizza" : {"price" : 25, "type": "food", "health": 15, "energy": 35, "shelf_life": 600, "hunger": -20},
    "ice_cream" : {"price" : 20, "type": "food", "health": 5, "energy": 20, "shelf_life": 600, "hunger": -10},
    "popcorn" : {"price" : 10, "type": "food", "health": 5, "energy": 15, "shelf_life": 600, "hunger": -5},
    "kiwi" : {"price" : 3, "type": "food", "health": 7, "energy": 12, "shelf_life": 300, "hunger": -3},
    "lemon" : {"price" : 2, "type": "food", "health": 5, "energy": 10, "shelf_life": 300, "hunger": -2},
    "carrot" : {"price" : 2, "type": "food", "health": 5, "energy": 10, "shelf_life": 300, "hunger": -2},
    "ramen" : {"price" : 15, "type": "food", "health": 10, "energy": 20, "shelf_life": 600, "hunger": -20},
    "stew" : {"price" : 20, "type": "food", "health": 15, "energy": 25, "shelf_life": 600, "hunger": -25},
    "tea": {"price" : 5, "type": "drink", "health": 0, "energy": 10, "shelf_life": 3600, "hunger": 0},
    "milk": {"price" : 7, "type": "drink", "health": 5, "energy": 10, "shelf_life": 3600, "hunger": 0},
    "egg": {"price" : 3, "type": "food", "health": 5, "energy": 10, "shelf_life": 300, "hunger": -2},
    "stake": {"price" : 50, "type": "food", "health": 20, "energy": 30, "shelf_life": 600, "hunger": -30},
    "noodles": {"price" : 15, "type": "food", "health": 5, "energy": 15, "shelf_life": 600, "hunger": -10},
    "soda": {"price" : 5, "type": "drink", "health": -2, "energy": 10, "shelf_life": 3600, "hunger": 0},
    #activities & usable items
    "book": {"price": 50, "type": "book", "happiness": 5, "intelligence": 0.5, "desc": "Read a book to increase your intelligence and happiness."},
    "anime": {"price": 30, "type": "watch", "happiness": 10, "perception": 0.5, "desc": "Watch an anime to increase your happiness."},
    "giftbox": {"price": 250, "type": "usable", "desc": "Open a gift box to receive a random item."},
    "luckybox": {"price": 125, "type": "usable", "desc": "Test your luck and open a lucky box. Be careful, it bites PAINFULLY!!!"},
    "house": {"price": 5000, "type": "booster", "desc": "Boosts your salary "},
    "car": {"price": 2500, "type": "booster", "desc": "Boosts your salary"},
    "suitcase": {"price": 450, "type": "booster", "desc": "Boosts your salary"},
    "TV": {"price": 500, "type": "usable", "desc": "Watch your favorite shows and increase your happiness."},
    "smartphone": {"price": 300, "type": "usable", "desc": "Another way to watch films and more ..."},
    "fishing_rod": {"price": 300, "type": "usable", "desc": "Go fishing and catch some fish to sell or eat. Requires a bait to use it."},
    "worm": {"price": 5, "type": "usable", "desc": "The most common bait for fishing. It's good to use it when catching small fish"},
    "bait": {"price": 50, "type": "usable", "desc": "A bait, specifically designed for having a huge catch. Using it will increase your chances of catching a big fish."},
    "hunting_rifle": {"price": 1000, "type": "usable", "desc": "Go hunting and catch some animals to sell or eat. Requires a bullet to use it. NO LICENSE REQUIRED."},
    "bullet": {"price": 50, "type": "usable", "desc": "A bullet, specifically designed for hunting. Rules are simple: no bullets, no hunting."},
    "pickaxe": {"price": 500, "type": "usable", "desc": "Go mining and find some valuable ores to sell or use. No requirements yet."},
    "gambling_token": {"price": 100, "type": "usable", "desc": "A token that allows you to gamble. Please don't waste all your money on gambling, it's not a good idea."},
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
