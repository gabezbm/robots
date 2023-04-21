from utils import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.surface = pygame.display.set_mode(WINDOW_SIZE.get())
        self.running = True
        self.player = Player(
            self.surface,
            MAP_SIZE.width // 2,
            MAP_SIZE.height // 2
        )

    def drawBg(self) -> None:
        for x in range(MAP_SIZE.width):
            for y in range(MAP_SIZE.height):
                pygame.draw.rect(
                    self.surface,
                    COLORS["tileBg0"] if isOdd(x + y) else COLORS["tileBg1"],
                    (x * TILE_SIZE.width, y * TILE_SIZE.height, TILE_SIZE.width, TILE_SIZE.height)
                )

    def movePlayer(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in KEYS["north"]:
                    self.player.move("N")
                elif event.key in KEYS["south"]:
                    self.player.move("S")
                elif event.key in KEYS["west"]:
                    self.player.move("W")
                elif event.key in KEYS["east"]:
                    self.player.move("E")
                elif event.key in KEYS["north-west"]:
                    self.player.move("NW")
                elif event.key in KEYS["north-east"]:
                    self.player.move("NE")
                elif event.key in KEYS["south-west"]:
                    self.player.move("SW")
                elif event.key in KEYS["south-east"]:
                    self.player.move("SE")

    def main(self) -> None:
        while self.running:
            self.drawBg()
            self.player.draw()
            self.movePlayer()
            pygame.display.update()
        pygame.quit()
