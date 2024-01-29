import pygame
from random import shuffle
from time import sleep


class Card(pygame.sprite.Sprite):

    back_im = pygame.image.load("card_back.png")

    def __init__(self, img, x, y):
        super().__init__(all_sprites)
        self.front = pygame.image.load(img)
        self.back = Card.back_im
        self.image = self.back
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_flipped = False
        self.image_name = img

    def flip(self):
        self.is_flipped = not self.is_flipped
        if self.is_flipped:
            self.image = self.front
        else:
            self.image = self.back

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if not self.is_flipped:
                self.flip()


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0


all_sprites = pygame.sprite.Group()

# Создание списка карточек
images = ["arthur_fish.png", "igla.png", "igla.png", "konok.png", "konok.png", "money.png", "ne_pila.png",
          "ne_pila.png", "pila.png", "pila.png", "rock.png", "sguch.png", "sguch.png",
          "smuch.png", "smuch.png", "sword.png"]

shuffle(images)
x_l, y_l = 30, 30
for i in range(4):
    for j in range(4):
        Card(images[(i * 4) + j - 1], x_l, y_l)
        x_l += 130
    x_l = 30
    y_l += 180


player1 = Player("Игрок 1")
player2 = Player("Игрок 2")
current_player = player1

# Основной игровой цикл
if __name__ == '__main__':
    pygame.init()
    size = width, height = 550, 720
    screen = pygame.display.set_mode(size)
    running = True
    cards = []
    color = (250, 199, 185)
    print(current_player.name)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if len(cards) == 2:
                sleep(2)
                if cards[0].image_name == "rock.png":
                    current_player.score -= 1
                    cards[0].kill()
                if cards[1].image_name == "rock.png":
                    current_player.score -= 1
                    cards[1].kill()
                if cards[0].image_name == "money.png":
                    current_player.score += 1
                    cards[0].kill()
                if cards[1].image_name == "money.png":
                    current_player.score += 1
                    cards[1].kill()
                if cards[0].image_name == cards[1].image_name or \
                        {cards[0].image_name, cards[1].image_name} == {"arthur_fish.png", "sword.png"}:
                    cards[0].kill()
                    cards[1].kill()
                    current_player.score += 1
                else:
                    for card in all_sprites:
                        if card.is_flipped:
                            card.flip()
                    current_player = player1 if current_player == player2 else player2
                cards = []
                print("1: " + str(player1.score))
                print("2: " + str(player2.score))
                print(current_player.name)
                if current_player == player2:
                    color = (185, 239, 250)
                else:
                    color = (250, 199, 185)
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
                pos = pygame.mouse.get_pos()
                for card in all_sprites:
                    if card.rect.collidepoint(pos):
                        cards.append(card)

        screen.fill(color)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
