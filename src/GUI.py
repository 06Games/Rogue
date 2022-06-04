import pygame
import math


class Button:
    """Button class"""

    def __init__(self, x, y, image, w, h):
        self.image = pygame.transform.scale(image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.rightClicked = False

    def draw(self, surface):
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
            if pygame.mouse.get_pressed()[2] == 1:
                self.rightClicked = True
        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))


def drawImage(screen, path, x, y, w, h):
    image = pygame.image.load(path)
    imgW = image.get_width()
    imgH = image.get_height()

    ratio = max(imgW / w, imgH / h)
    width = imgW / ratio
    height = imgH / ratio
    xPos = x + (w - width) / 2
    yPos = y + (h - height) / 2

    image = pygame.transform.scale(image, (width, height))
    screen.blit(image, (xPos, yPos))
    return xPos, yPos, width, height


messages = None


def printMsg(game):
    global messages
    msg = game.readMessages()
    if msg is not None and msg != "":
        messages = msg
        return msg
    else:
        return messages


class GUI:
    from Game import Game

    def __init__(self, game: Game):
        self.game = game
        pygame.init()
        self.updateScreenSize(900, 500)

    # noinspection PyAttributeOutsideInit
    def updateScreenSize(self, w, h):
        w, h = max(900, w), max(500, h)
        self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
        self.w, self.h = w, h
        self.tileSize = min(self.w * 0.7, self.w - 400, self.h) / self.game.floor.size

    def getTileSurface(self, e):
        from Item import Item
        if isinstance(e, Item):
            return self.tileSize * 0.65, self.tileSize * 0.65
        return self.tileSize, self.tileSize

    def getTilePos(self, x, y, e):
        tileSurface = self.getTileSurface(e)
        tilePos = x * self.tileSize, y * self.tileSize
        return tilePos[0] + (self.tileSize - tileSurface[0]) / 2, tilePos[1] + (self.tileSize - tileSurface[1]) / 2

    def main(self):
        import sys
        from Coord import Coord

        self.startScreen()
        while self.game.hero.hp > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.game.newTurn(event.key)
                if event.type == pygame.VIDEORESIZE:
                    self.updateScreenSize(event.size[0], event.size[1])

            self.screen.fill((75, 75, 75))
            font4 = pygame.font.SysFont('comicsansms', int(self.tileSize * (2 / 5)))
            a, b = pygame.mouse.get_pos()
            posHero = self.game.floor.pos(self.game.hero)
            for y in range(len(self.game.floor)):
                for x in range(len(self.game.floor)):
                    e = self.game.floor.get(Coord(x, y))
                    if posHero.distance(Coord(x, y)) <= 6 or Coord(x, y) in self.game.floor.visited:
                        if Coord(x, y) not in self.game.floor.visited:
                            self.game.floor.visited.append(Coord(x, y))
                        if e is None:
                            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/lava.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))
                        else:
                            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))

                            if e.image is not None:
                                from Monster import Monster
                                from Item import Item
                                self.screen.blit(pygame.transform.scale(pygame.image.load(e.image), self.getTileSurface(e)), self.getTilePos(x, y, e))
                                if isinstance(e, Monster):
                                    if e.visibility:
                                        pygame.draw.rect(self.screen, (0, 0, 0),
                                                         pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1] - self.tileSize * (0.6 / 5),
                                                                     self.tileSize, self.tileSize * (0.75 / 5)))
                                        pygame.draw.rect(self.screen, (25, 172, 38),
                                                         pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1] - self.tileSize * (0.6 / 5),
                                                                     self.tileSize * (e.hp / e.hpMax), self.tileSize * (0.75 / 5)))
                                if isinstance(e, Item):
                                    if pygame.Rect(a, b, self.tileSize, self.tileSize).colliderect(
                                            pygame.Rect(self.getTilePos(x, y, e)[0], self.getTilePos(x, y, e)[1], self.tileSize, self.tileSize)):
                                        self.screen.blit(font4.render(e.description(), True, (255, 255, 255)),
                                                         (self.getTilePos(x, y, e)[0] - self.tileSize * (3 / 5), self.getTilePos(x, y, e)[1] - self.tileSize * (3 / 5)))
                    else:
                        self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/cloud.png"), self.getTileSurface(None)), self.getTilePos(x, y, None))

            self.sidePanel()
            pygame.display.flip()

        self.endScreen()

    def startScreen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    import sys
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.updateScreenSize(event.size[0], event.size[1])
            self.screen.fill((255, 255, 255))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/back.png"), (self.w, self.h)), (0, 0))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/arcade.png"), (self.w / 2, self.h)),
                             (self.w * (1 / 4), 0))
            start_button = Button((self.w / 2) - 348 / 2, (self.h * (4 / 5)), pygame.image.load("assets/other/startButton.png"), 348, 149)
            start_button.draw(self.screen)
            pygame.display.flip()
            if start_button.clicked:
                break

    def drawItem(self, elem, x, y, action=lambda elem, hero: elem.deEquip(hero), rightAction=lambda elem, hero: None):
        pygame.draw.rect(self.screen, (55, 55, 55), pygame.Rect(x, y, self.tileSize, self.tileSize))
        if elem is not None:
            elemButton = Button(x + self.tileSize * 0.125, y + self.tileSize * 0.125, pygame.image.load(elem.image), self.tileSize * 0.75, self.tileSize * 0.75)
            elemButton.draw(self.screen)
            if elemButton.clicked:
                action(elem, self.game.hero)
            if elemButton.rightClicked:
                rightAction(elem, self.game.hero)

    def drawPotion(self, x, y, w, h, i):
        from config import potions
        spellsFont = pygame.font.SysFont('comicsansms', 15)
        spell = potions[i]
        self.drawItem(spell, x, y, action=lambda elem, hero: elem.activate(hero))
        txt = spellsFont.render(spell.name + ": " + str(spell.price) + " mana", True, (255, 255, 255))
        self.screen.blit(txt, (x + (self.tileSize - txt.get_width()) / 2, y + self.tileSize + 5))

    def sidePanel(self, debug=False):
        boxX = self.game.floor.size * self.tileSize + 20
        boxY = 20
        boxW = self.screen.get_width() - boxX - 20  # Window's size - Position of the panel - Margin right of the panel
        boxH = self.screen.get_height() - boxY - 20
        pygame.draw.rect(self.screen, (64, 64, 64), pygame.Rect(boxX, boxY, boxW, boxH))  # Draw the panel

        font = pygame.font.SysFont('comicsansms', int(boxW * 0.03))
        screen = self.screen
        tileSize = self.tileSize

        statsX, statsY = boxX + 20, boxY + 20
        equipmentW, equipmentH = max(self.tileSize * 2 + 40 + 100, boxW / 2 - 30), self.tileSize * 4 + 20 * 3
        statsW, statsH = boxX + boxW - statsX - equipmentW - 40, equipmentH
        equipmentX, equipmentY = statsX + statsW + 20, statsY
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (20, 80, 20), pygame.Rect(statsX, statsY, statsW, statsH))
            pygame.draw.rect(self.screen, (20, 20, 80), pygame.Rect(equipmentX, equipmentY, equipmentW, equipmentH))

        self.drawEquipment(equipmentX, equipmentY, equipmentW, equipmentH)

        # Stats: bars of hp, satiety, etc
        x = 20 * tileSize + boxW * (0.25 / 5)
        y = self.h / 20
        self.drawBarImage(x, y, 10, lambda i: "assets/other/heartRed.png" if i < self.game.hero.hp else "assets/other/heartGrey.png", statsW, sizeImage=self.tileSize * 0.75)
        self.drawBarImage(x, y + self.tileSize * 2.7, self.game.hero.satietyMax, lambda i: "assets/food/chunk.png" if i < self.game.hero.satiety else "assets/food/chunkBack.png", statsW, nbCol=10)
        self.drawBarImage(x, y + self.tileSize * 3.7, self.game.hero.manaMax, lambda i: "assets/other/mana.png" if i < self.game.hero.mana else "assets/other/manaBack.png", statsW, nbCol=10)

        # Spells
        from config import potions
        spellsX, spellsY = statsX, statsY + statsH + 40
        spellsW, spellsH = boxW - 40, self.tileSize + 25
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (80, 20, 20), pygame.Rect(spellsX, spellsY, spellsW, spellsH))  # debug rect
        self.drawBar(spellsX, spellsY, len(potions), self.drawPotion, spellsW, spellsH, nbCol=len(potions), sizeImage=self.tileSize)

        # Inventory
        inventoryX, inventoryY = spellsX, spellsY + spellsH + 40
        inventoryW = spellsW
        inventoryColumns = max(int(inventoryW / (self.tileSize + 20)), 1)
        inventoryLines = math.ceil(self.game.hero.inventorySize / inventoryColumns)
        inventoryH = self.tileSize * inventoryLines + 20 * (inventoryLines - 1)
        if debug:  # debug rects
            pygame.draw.rect(self.screen, (80, 80, 20), pygame.Rect(inventoryX, inventoryY, inventoryW, inventoryH))
        self.drawBar(inventoryX, inventoryY, self.game.hero.inventorySize,
                     lambda x, y, w, h, i: self.drawItem(self.game.hero.inventory[i] if i < len(self.game.hero.inventory) else None, x, y,
                                                         action=lambda elem, hero: hero.use(elem),
                                                         rightAction=lambda elem, hero: hero.inventory.remove(elem)),
                     inventoryW, inventoryH, nbCol=inventoryColumns, sizeImage=self.tileSize)

        # Messages
        messagesX, messagesY = inventoryX, inventoryY + inventoryH + 40
        messagesW, messagesH = inventoryW, 100
        messagesFont = pygame.font.SysFont('comicsansms', int(boxW * 0.03))
        pygame.draw.rect(screen, (55, 55, 55), pygame.Rect(messagesX, messagesY, messagesW, messagesH))
        self.screen.blit(messagesFont.render(str(printMsg(self.game)), True, (255, 255, 255)), (messagesX, messagesY, messagesW, messagesH))

        # Controls
        controlsX, controlsY = messagesX, messagesY + messagesH + 40
        controlsW, controlsH = messagesW, 200
        screen.blit(font.render("move:", True, (255, 255, 255)), (20 * tileSize + boxW * (0.5 / 5), self.h * (7.7 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterZ.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (20 * tileSize + boxW * (1.25 / 5), self.h * (7.4 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterQ.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (20 * tileSize + boxW * (1.25 / 5) - tileSize * 0.75, self.h * (7.7 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterS.png"), (tileSize * 0.7, tileSize * 0.71)),
                    (20 * tileSize + boxW * (1.25 / 5), self.h * (7.7 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterD.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (20 * tileSize + boxW * (1.5 / 5) + tileSize * 0.09, self.h * (7.7 / 10)))
        screen.blit(font.render("skip one turn:", True, (255, 255, 255)), (20 * tileSize + boxW * (2.7 / 5), self.h * (9.3 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/spaceBar .png"), (tileSize * 2.7, tileSize * 0.9)),
                    (20 * tileSize + boxW * (3.7 / 5), self.h * (9.2 / 10)))
        screen.blit(font.render("destroy an object: right click", True, (255, 255, 255)), (20 * tileSize + boxW * (2.7 / 5), self.h * (8.8 / 10)))
        screen.blit(font.render("suicide:", True, (255, 255, 255)), (20 * tileSize + boxW * (0.5 / 5), self.h * (9.3 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterK.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (20 * tileSize + boxW * (1.25 / 5), self.h * (9.25 / 10)))
        screen.blit(font.render("use an object: left click", True, (255, 255, 255)), (20 * tileSize + boxW * (2.7 / 5), self.h * (8.3 / 10)))
        screen.blit(font.render("get 5 hp for 10 turns:", True, (255, 255, 255)), (20 * tileSize + boxW * (0.5 / 5), self.h * (8.5 / 10)))
        screen.blit(pygame.transform.scale(pygame.image.load("assets/other/letterR.png"), (tileSize * 0.7, tileSize * 0.7)),
                    (self.w * (3.75 / 5), self.h * (8.5 / 10)))

    def drawEquipment(self, x, y, w, h):
        equipmentTileGap = 15
        equipmentTileW, equipmentTileH = self.tileSize, self.tileSize + equipmentTileGap

        equipmentLeftTiles = [self.game.hero.helmet, self.game.hero.chestplate, self.game.hero.legs, self.game.hero.boots]
        equipmentTileLeftW, equipmentTileLeftH = equipmentTileW, equipmentTileH * len(equipmentLeftTiles) - equipmentTileGap
        equipmentTileLeftX, equipmentTileLeftY = x, y + (h - equipmentTileLeftH) / 2
        for equipmentI in range(len(equipmentLeftTiles)):
            self.drawItem(equipmentLeftTiles[equipmentI], equipmentTileLeftX, equipmentTileLeftY + equipmentTileH * equipmentI)

        # Image of the hero
        heroX = equipmentTileLeftX + equipmentTileW + 20
        heroY = y
        heroW = w - (equipmentTileW + 20) * 2
        heroH = h - 50
        heroImgX, heroImgY, heroImgW, heroImgH = drawImage(self.screen, "assets/hero/frontHero.png", heroX, heroY, heroW, heroH)

        # XP bar
        xpH = 15
        xpY = heroImgY - 20
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(heroX, xpY, heroW, xpH))
        pygame.draw.rect(self.screen, (25, 172, 38), pygame.Rect(heroX, xpY, heroW * (self.game.hero.xp / self.game.hero.lvlSup()), xpH))
        font = pygame.font.SysFont('comicsansms', int(xpH * 0.75))
        self.screen.blit(font.render("lvl:" + str(self.game.hero.lvl), True, (255, 255, 255)), (heroX + 5, xpY))
        xpTxt = font.render(str(self.game.hero.xp) + "/" + str(self.game.hero.lvlSup()), True, (255, 255, 255))
        self.screen.blit(xpTxt, (heroX + heroW - xpTxt.get_width() - 5, xpY))

        equipmentRightTiles = [self.game.hero.weapon, self.game.hero.shield, self.game.hero.amulet]
        equipmentTileRightW, equipmentTileRightH = equipmentTileW, equipmentTileH * len(equipmentRightTiles) - equipmentTileGap
        equipmentTileRightX, equipmentTileRightY = heroX + heroW + 20, y + (h - equipmentTileRightH) / 2
        for equipmentI in range(len(equipmentRightTiles)):
            self.drawItem(equipmentRightTiles[equipmentI], equipmentTileRightX, equipmentTileRightY + equipmentTileH * equipmentI)

        # caractéristiques du héros
        statsX, statsY = heroX, heroImgY + heroImgH + 5
        statsW, statsH = heroW / 2 - 20, 30
        statsFont = pygame.font.SysFont('comicsansms', 20)
        drawImage(self.screen, "assets/hero equipment/sword/sword1.png", statsX, statsY, statsW, statsH)
        strengthTxt = statsFont.render(str(self.game.hero.strengthTot()), True, (255, 255, 255))
        self.screen.blit(strengthTxt, (statsX + (statsW - strengthTxt.get_width()) / 2, statsY + statsH))
        drawImage(self.screen, "assets/hero equipment/shield/shield2.png", statsX + statsW + 40, statsY, statsW, statsH)
        resistanceTxt = statsFont.render(str(self.game.hero.resistance()), True, (255, 255, 255))
        self.screen.blit(resistanceTxt, (statsX + statsW + 40 + (statsW - resistanceTxt.get_width()) / 2, statsY + statsH))

    def drawBarImage(self, x, y, valueMax, image, width, height=None, nbCol=5, padding=5, sizeImage=None):
        self.drawBar(x, y, valueMax,
                     lambda _x, _y, w, h, i: self.screen.blit(pygame.transform.scale(pygame.image.load(image(i)), (max(w, 0), max(h, 0))), (_x, _y)),
                     width, height, nbCol, padding, sizeImage)

    def drawBar(self, x, y, valueMax, drawFct, width, height=None, nbCol=5, padding=5, sizeImage=None):
        gapX = width / nbCol
        gapY = gapX if height is None else height / math.ceil(valueMax / nbCol)
        size = gapX - padding if sizeImage is None else min(sizeImage, gapX - padding)
        x += abs(gapX - size) / 2  # Center the bar
        for nbr in range(valueMax):
            drawFct(x + (nbr - int(nbr / nbCol) * nbCol) * gapX, y + int(nbr / nbCol) * gapY, size, size, nbr)

    def endScreen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    import sys
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.updateScreenSize(event.size[0], event.size[1])
            buttonsY = self.h / 1.3
            close_button = Button(20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.7 / 5), buttonsY, pygame.image.load("assets/other/exitButton.png"),
                                  (self.w - 20 * self.tileSize) * (1.5 / 5), self.h * (1 / 10))
            replay_button = Button(20 * self.tileSize + (self.w - 20 * self.tileSize) * (2.8 / 5), buttonsY, pygame.image.load("assets/other/restartButton.png"),
                                   (self.w - 20 * self.tileSize) * (1.5 / 5), self.h * (1 / 10))
            font = pygame.font.SysFont('comicsansms', int((self.w - 20 * self.tileSize) * 0.05))
            font1 = pygame.font.SysFont('comicsansms', int((self.w - 20 * self.tileSize) * 0.07))
            posHero = self.game.floor.pos(self.game.hero)
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/ground.png"), self.getTileSurface(self.game.hero)),
                             self.getTilePos(posHero.x, posHero.y, self.game.hero))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/graveHero.png"), self.getTileSurface(self.game.hero)),
                             self.getTilePos(posHero.x, posHero.y, self.game.hero))
            self.game.hero.image = "assets/other/graveHero.png"
            pygame.draw.rect(self.screen, (0, 0, 0),
                             pygame.Rect(self.tileSize * self.game.floor.size + 20, 20, self.w - self.tileSize * self.game.floor.size - 40, self.h - 40))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/other/gameOver.png"),
                                                    (self.w - self.tileSize * self.game.floor.size - 40, self.h * (1 / 3))),
                             (self.tileSize * self.game.floor.size + 20, 20))
            self.screen.blit(font1.render("SCORE:", True, (255, 255, 255)),
                             (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (0.9 / 3)))
            self.screen.blit(font.render("hero level: " + str(self.game.hero.lvl), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.3 / 3)))
            self.screen.blit(font.render("rooms visited: " + str(self.game.level), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.6 / 3)))
            self.screen.blit(font.render("monsters killed: " + str(self.game.hero.monstersKilled), True, (255, 255, 255)),
                             (20 * self.tileSize + (self.w - 20 * self.tileSize) * (0.5 / 5), self.h * (1.9 / 3)))
            close_button.draw(self.screen)
            replay_button.draw(self.screen)
            pygame.display.flip()

            if close_button.clicked:
                pygame.quit()
                import sys
                sys.exit()
            if replay_button.clicked:
                self.game.__init__()
                self.game.buildFloor()
                self.main()
                break
