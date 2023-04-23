from utils import *


class Game:
    def __init__(self):
        print("\nGame started.\n" + "-" * 30)
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.surface = pygame.display.set_mode(WINDOW_SIZE.sizeTuple)
        self.running = True
        self.player = Player(
            self.surface,
            MAP_SIZE.width // 2,
            MAP_SIZE.height // 2
        )
        self.enemies: list[Enemy] = []
        self.explosions: list[Explosion] = []
        validGrids = [(x + 1, y + 1) for x in range(MAP_SIZE.width) for y in range(MAP_SIZE.height) if Position(x + 1, y + 1) != self.player.pos]
        for x, y in random.sample(validGrids, k=ENEMY_NUMBER):
            self.enemies.append(Enemy(self.surface, x, y))
        self.score = 0

    def updateScore(self) -> None:
        self.score += 1
        print("Score:", self.score)

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
                else:
                    for action in VALID_ACTIONS:
                        if event.key in ACTION_KEYS[action]:
                            self.player.move(action)
                            self.updateScore()
                            if isOnObjects(self.player, self.explosions) != -1:
                                self.running = False
                            self.moveEnemies()
                            break

    def moveEnemies(self) -> None:
        for enemy in self.enemies:
            if action := enemy.chase(self.player):
                enemy.move(action)
            if enemy.pos == self.player.pos:
                self.running = False
        explodeIndices: set[int] = set()
        for i, enemy in enumerate(self.enemies):
            if isOnObjects(enemy, self.explosions) != -1:
                explodeIndices.add(i)
            else:
                if (j := isOnObjects(enemy, self.enemies[i + 1:])) != -1:
                    explodeIndices |= {i, j + i + 1}
        for i in explodeIndices:
            self.explosions.append(self.enemies[i].explode())
        self.enemies = [enemy for i, enemy in enumerate(self.enemies) if i not in explodeIndices]
        if len(self.enemies) == 0:
            print("You win!")
            self.running = False


    def main(self) -> None:
        while self.running:
            # Todo: how to updateScore here rather than in movePlayer?
            # self.updateScore()
            self.drawBg()
            self.player.draw()
            for enemy in self.enemies:
                enemy.draw()
            for explosion in self.explosions:
                explosion.draw()
            self.movePlayer()
            # Todo: how to moveEnemies here rather than in movePlayer?
            # self.moveEnemies()
            pygame.display.update()
        pygame.quit()
        print("\nQuiting Game:\n" + "-" * 30)
