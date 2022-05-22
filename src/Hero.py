from Creature import Creature


class Hero(Creature):
    def __init__(self, name="Hero", image="assets/hero/frontHero.png", healthMax=10, abbrv="@", strength=2, color="\033[0;32m",
                 satietyMax=10):
        from Monster import Monster
        Creature.__init__(self, name, healthMax, Monster, abbrv, strength, color, image)
        self.inventory = []
        self.armor = None
        self.weapon = None
        self.xp, self.lvl = 0, 1
        self.satiety, self.satietyMax = satietyMax, satietyMax
        self.healthMax = healthMax
        self.monstersKilled = 0

    def description(self):
        return Creature.description(self) + str(self.inventory)

    def fullDescription(self):
        attributs = []
        for attr, val in self.__dict__.items():
            if not attr.startswith("_") and attr != "inventory":
                attributs.append("> " + attr + " : " + str(val))
        attributs.append("> INVENTORY : " + str([x.name for x in self.inventory]))
        return "\n".join(attributs)

    def take(self, item):
        """Collects an item on the ground"""
        from Equipment import Equipment
        if not isinstance(item, Equipment):
            raise TypeError('Not a Equipment')
        if item in self.inventory:
            return False
        self.inventory.append(item)
        return True

    def use(self, item):
        """Uses an item"""
        from Equipment import Equipment
        if item is None:
            return
        if not isinstance(item, Equipment):
            raise TypeError("Not an equipment")
        if item not in self.inventory:
            raise ValueError("Not in the inventory")
        if item.use(self):
            self.inventory.remove(item)

    def attack(self, attacked):
        """Attacks a monster"""
        import utils
        if attacked.image is not None:
            attacked.hp -= self.strength
        if self.weapon is not None:
            attacked.hp -= self.weapon.damage
        utils.theGame().addMessage("The " + self.name + " hits the " + attacked.description())

        if attacked.hp <= 0:
            self.xp += 1
            self.monstersKilled += 1
            self.experience()

    def lvlSup(self):
        import math
        return 30 * math.exp((self.lvl - 1) / 4)

    def experience(self):
        if self.xp >= self.lvlSup():
            self.xp -= self.lvlSup()
            self.lvl += 1
            self.healthMax += 1
