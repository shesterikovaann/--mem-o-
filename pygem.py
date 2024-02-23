import pygame
from random import shuffle
from time import sleep
import os
import sys


class Card(pygame.sprite.Sprite):

    back_im = pygame.image.load("data/card_back.png")

    def __init__(self, img: str, x: int, y: int):
        super().__init__(all_sprites)
        self.front = load_image(img)
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns: int, rows: int):
        # обрезаем и нарезку делаем
        self.rect = pygame.Rect(0, 0, 5422 // columns,
                                830 // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        # обновление картинки
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name: str):  # загрузка картинки
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

# группа спрайтов
all_sprites = pygame.sprite.Group()

# игроки
player1 = Player("Игрок 1")
player2 = Player("Игрок 2")
current_player = player1

# Основной игровой цикл
if __name__ == '__main__':
    pygame.init()
    size = width, height = 750, 720
    screen = pygame.display.set_mode(size)
    running = True
    cards = []
    # фон
    color = (250, 199, 185)
    pygame.display.set_caption("Рыбное мемо")
    icon = load_image("icon.png")
    # открываем бд
    with open("бд.txt", "r", encoding="utf-8") as menu:
        menu = menu.readlines()[-1].strip().split()
        score1, score2 = int(menu[0]), int(menu[1])

    # задаём тексты
    f1 = pygame.font.Font(None, 36)
    p1 = f1.render('Игрок 1:', True,
                      (180, 0, 0))
    p2 = f1.render('Игрок 2:', True,
                   (0, 0, 180))
    c1 = f1.render('0', True,
                   (180, 0, 0))
    c2 = f1.render('0', True,
                   (0, 0, 180))
    # для окон
    finish = False
    start = True
    hello = f1.render('Привет! Это рыбное мемо - Выбери уровень', True, (100, 0, 0))
    # кнопки уровней
    button1 = pygame.Rect(550, 100, 150, 50)
    button2 = pygame.Rect(550, 200, 150, 50)
    easy = f1.render('Легкий', True, (100, 0, 0))
    hard = f1.render('Сложный', True, (100, 0, 0))

    score1_text = f1.render(f'Игрок 1: {score1} побед', True, (100, 0, 0))
    score2_text = f1.render(f'Игрок 2: {score2} побед', True, (100, 0, 0))

    level_1, level_2 = False, False
    # чтобы включить уровень
    s = True
    # дебаг
    print(current_player.name)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # выбор уровня
                if start:
                    if button1.collidepoint(event.pos):
                        start = False
                        level_1 = True
                    elif button2.collidepoint(event.pos):
                        start = False
                        level_2 = True

            if level_1:  # лёгкий уровень
                if s:
                    images = ["arthur_fish.png", "konok.png", "konok.png", "money.png",
                              "ne_pila.png", "ne_pila.png", "sguch.png", "sguch.png", "sword.png"]

                    # добавляем спрайты в группу
                    shuffle(images)
                    x_l, y_l = 30, 30
                    for i in range(3):
                        for j in range(3):
                            Card(images[(i * 3) + j - 1], x_l, y_l)
                            x_l += 130
                        x_l = 30
                        y_l += 180
                    s = False
                # проверка для финиша
                if player1.score + player2.score == 5:
                    if not finish:
                        cuzya = AnimatedSprite(load_image("molodec.png"), 5, 1, 0, 40)
                        finish = True
                        # добавляем в бд
                        if player1.score > player2.score:
                            score1 += 1
                        elif player1.score < player2.score:
                            score2 += 1

                    if player1.score > player2.score:
                        final = f1.render('Игрок 1 победил', True, (0, 0, 180))
                    elif player1.score < player2.score:
                        final = f1.render('Игрок 2 победил!', True, (0, 0, 180))
                    else:
                        final = f1.render('Ничья', True, (0, 0, 0))

                # гадание на картах
                if len(cards) == 2:
                    sleep(2)
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
                    # счёт
                    c1 = f1.render(str(player1.score), True,
                                   (180, 0, 0))
                    c2 = f1.render(str(player2.score), True,
                                   (0, 0, 180))
                    print(current_player.name)
                    if current_player == player2:
                        color = (185, 239, 250)
                    else:
                        color = (250, 199, 185)
                # обновочка
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event)
                    pos = pygame.mouse.get_pos()
                    for card in all_sprites:
                        if card.rect.collidepoint(pos):
                            cards.append(card)
            elif level_2:  # сложный уровень
                if s:
                    images = ["arthur_fish.png", "igla.png", "igla.png", "konok.png", "konok.png", "money.png",
                              "ne_pila.png",
                              "ne_pila.png", "pila.png", "pila.png", "rock.png", "sguch.png", "sguch.png",
                              "smuch.png", "smuch.png", "sword.png"]
                    # создаём группу спрайтов
                    shuffle(images)
                    x_l, y_l = 30, 30
                    for i in range(4):
                        for j in range(4):
                            Card(images[(i * 4) + j - 1], x_l, y_l)
                            x_l += 130
                        x_l = 30
                        y_l += 180
                    s = False

                if player1.score + player2.score == 7:  # финал
                    if not finish:
                        cuzya = AnimatedSprite(load_image("molodec.png"), 5, 1, 0, 40)
                        finish = True
                        # добавляем в бд
                        if player1.score > player2.score:
                            score1 += 1
                        elif player1.score < player2.score:
                            score2 += 1

                    if player1.score > player2.score:
                        final = f1.render('Игрок 1 победил', True, (0, 0, 180))
                    elif player1.score < player2.score:
                        final = f1.render('Игрок 2 победил!', True, (0, 0, 180))
                    else:
                        final = f1.render('Ничья', True, (0, 0, 0))

                # шуры муры с картами
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
                    c1 = f1.render(str(player1.score), True,
                                   (180, 0, 0))
                    c2 = f1.render(str(player2.score), True,
                                   (0, 0, 180))
                    print(current_player.name)
                    if current_player == player2:
                        color = (185, 239, 250)
                    else:
                        color = (250, 199, 185)

                # обновление
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event)
                    pos = pygame.mouse.get_pos()
                    for card in all_sprites:
                        if card.rect.collidepoint(pos):
                            cards.append(card)
        # цвет
        screen.fill(color)
        if finish:
            cuzya.update()
            screen.blit(final, (10, 10))
        if start:
            screen.fill((240, 208, 93))
            screen.blit(hello, (20, 20))
            pygame.draw.rect(screen, (255, 130, 130), button1)
            pygame.draw.rect(screen, (200, 40, 40), button2)

            screen.blit(easy, (550, 70))
            screen.blit(hard, (550, 170))
            screen.blit(icon, (20, 60, 450, 450))

            screen.blit(score1_text, (50, 550))
            screen.blit(score2_text, (50, 600))
        else:  # основная игра
            screen.blit(p1, (550, 100))
            screen.blit(p2, (550, 200))
            screen.blit(c1, (670, 100))
            screen.blit(c2, (670, 200))
            all_sprites.draw(screen)
        pygame.display.flip()
        pygame.display.update()

    # добавляем результат в бд
    with open("бд.txt", "w", encoding="utf-8") as menu:
        print(f"{score1} {score2}", file=menu)
    pygame.quit()
