import enum


class WorkState(enum.Enum):
    DONE = 1
    READY = 2


# Columns of the users table (besides user_id and username).
# Written once here and used by create/save, so the field list isn't copied three times.
STAT_COLUMNS = [
    "money", "health", "energy", "happiness", "work_state", "last_work_time",
    "bought_at", "hunger", "perception", "endurance", "intelligence", "dexterity", "luck",
]


class Player:
    # TODO: replace the default values with the starting values from Py-City Remake
    def __init__(self, user_id, username, money=100, health=100, energy=100, happiness=50,
                 work_state=WorkState.READY, last_work_time=0, bought_at=0, hunger=0,
                 perception=0, endurance=0, intelligence=0, dexterity=0, luck=0, inventory=None):
        self.user_id = user_id
        self.username = username
        self.money = money
        self.health = health
        self.energy = energy
        self.happiness = happiness
        self.work_state = WorkState(work_state)   # accepts both WorkState and a number from the DB
        self.last_work_time = last_work_time
        self.bought_at = bought_at
        self.hunger = hunger
        self.perception = perception
        self.endurance = endurance
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.luck = luck
        self.inventory = inventory if inventory is not None else {}   # {"apple": 3, ...}

    def _values(self):
        values = []
        for column in STAT_COLUMNS:
            value = getattr(self, column)
            values.append(value.value if isinstance(value, enum.Enum) else value)
        return values

    @classmethod
    async def load(cls, db, user_id: int) -> "Player | None":
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
        if row is None:
            return None
        async with db.execute("SELECT item, amount FROM inventory WHERE user_id = ?", (user_id,)) as cur:
            inventory = {r["item"]: r["amount"] for r in await cur.fetchall()}
        return cls(**dict(row), inventory=inventory)

    async def create(self, db):
        columns = ", ".join(["user_id", "username", *STAT_COLUMNS])
        marks = ", ".join("?" * (len(STAT_COLUMNS) + 2))
        await db.execute(f"INSERT INTO users ({columns}) VALUES ({marks})",
                         (self.user_id, self.username, *self._values()))
        await db.commit()

    async def save(self, db):
        sets = ", ".join(f"{c} = ?" for c in STAT_COLUMNS)
        await db.execute(f"UPDATE users SET {sets} WHERE user_id = ?", (*self._values(), self.user_id))
        # Inventory: delete the old rows and write the current ones
        await db.execute("DELETE FROM inventory WHERE user_id = ?", (self.user_id,))
        await db.executemany(
            "INSERT INTO inventory (user_id, item, amount) VALUES (?, ?, ?)",
            [(self.user_id, item, amount) for item, amount in self.inventory.items() if amount > 0],
        )
        await db.commit()

    # --- Getters and setters ---
    def get_inventory(self):
        return self.inventory

    def set_inventory(self, inventory):
        self.inventory = inventory
    def get_money(self):
        return self.money

    def set_money(self, amount):
        self.money = amount

    def get_health(self):
        return self.health
    def set_health(self, health):
        self.health = health
    def get_energy(self):
        return self.energy
    def set_energy(self, energy):
        self.energy = energy
    def get_happiness(self):
        return self.happiness
    def set_happiness(self, happiness):
        self.happiness = happiness
    def get_work_state(self):
        return self.default_work_state
    def set_work_state(self, state):
        self.default_work_state = state
    def get_last_work_time(self):
        return self.last_work_time
    def set_last_work_time(self, timestamp):
        self.last_work_time = timestamp
    def get_hunger(self):
        return self.hunger
    def set_hunger(self, hunger):
        self.hunger = hunger
    def get_luck(self):
        return self.luck
    def set_luck(self, luck):
        self.luck = luck
    def get_intelligence(self):
        return self.intelligence
    def set_intelligence(self, intelligence):
        self.intelligence = intelligence
    def get_perception(self):
        return self.perception
    def set_perception(self, perception):
        self.perception = perception
    def get_endurance(self):
        return self.endurance
    def set_endurance(self, endurance):
        self.endurance = endurance

    def get_dexterity(self):
        return self.dexterity
    def set_dexterity(self, dexterity):
        self.dexterity = dexterity
   

    # ...keep the rest of yours as they are...

    def stats(self) -> dict:
        return {
            "money": self.money, "health": self.health, "energy": self.energy,
            "happiness": self.happiness, "hunger": self.hunger, "perception": self.perception,
            "endurance": self.endurance, "intelligence": self.intelligence,
            "dexterity": self.dexterity, "luck": self.luck,
        }