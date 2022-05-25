from Equipment import Equipment


class Amulet(Equipment):
    from Hero import Hero

    def __init__(self, name: str, image=None, effectType=None):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param effectType: The type of effect
        """
        Equipment.__init__(self, name=name, image=image)
        self.image = image
        self.type = effectType

    def equip(self, hero: Hero):
        """Equip the amulet"""
        if hero.amulet is not None:
            hero.amulet.deEquip(hero)
        hero.amulet = self
        if self.type == "strength":
            hero.strength += 2
        elif self.type == "xp":
            hero.xpMultiplier = 1.5

        return True  # Removes the amulet from the inventory

    def deEquip(self, hero):
        """De-equip the amulet"""
        hero.amulet = None  # Removes the amulet from the equipped slot
        hero.inventory.append(self)  # Add the amulet to the inventory
        if self.type == "strength":
            hero.strength -= 2
        elif self.type == "xp":
            hero.xpMultiplier = 1
