import pygame
import sqlite3

WIDTH = 1000
HEIGHT = 700
T_SIZE = 50

pygame.init()
FONT = pygame.font.Font('pixel_font.otf', 30)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Christmas game')

pygame.mixer.music.load('sounds/jingle-bells.mp3')
btn_sound = pygame.mixer.Sound('sounds/button_clicked.wav')

bg0 = pygame.image.load('images/bg/bg_1.png')
bg1 = pygame.image.load('images/bg/bg_2.png')
bg_win = pygame.image.load('images/bg/bg_win.png')
char0 = pygame.image.load('images/icons/christmaself/ce.png')
char1 = pygame.image.load('images/icons/santaclause/sc.png')

level_one = []
level_two = []

with open('level_one.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        level_one.append(line.rstrip('\n').split(', '))
    f.close()

with open('level_two.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        level_two.append(line.rstrip('\n').split(', '))
    file.close()

clock = pygame.time.Clock()

start = True
register = False
log_in = False
menu = False
win = False
again_log = False
level = 1
music_play = 1
sounds_play = 1
user_name = 'Гость'
check_in_again = False
successful_check_in = False
err_log_out = False
game_over = False
btns_1_clicked = False
btns_2_clicked = False
escape = False


pygame.mixer.music.set_volume(0.1)
if music_play == 1:
    pygame.mixer.music.play(-1)


class World(object):
    def __init__(self, data, cur_level):
        self.tiles = []

        ice = pygame.image.load('images/bg/ice.png')
        snow = pygame.image.load('images/bg/snow.png')
        dirt = pygame.image.load('images/bg/dirt.png')
        grass = pygame.image.load('images/bg/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == '1':
                    img = pygame.transform.scale(ice, (T_SIZE, T_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * T_SIZE
                    img_rect.y = row_count * T_SIZE
                    tile = (img, img_rect)
                    self.tiles.append(tile)
                elif tile == '2':
                    img = pygame.transform.scale(snow, (T_SIZE, T_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * T_SIZE
                    img_rect.y = row_count * T_SIZE
                    tile = (img, img_rect)
                    self.tiles.append(tile)
                elif tile == '3':
                    img = pygame.transform.scale(dirt, (T_SIZE, T_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * T_SIZE
                    img_rect.y = row_count * T_SIZE
                    tile = (img, img_rect)
                    self.tiles.append(tile)
                elif tile == '4':
                    snowman = Snowmen(col_count * T_SIZE, row_count * T_SIZE)
                    if cur_level == 1:
                        snowmen_group1.add(snowman)
                    else:
                        snowmen_group2.add(snowman)
                elif tile == '5':
                    wave0 = Water(col_count * T_SIZE, row_count * T_SIZE, 'images/bg/wave0.png')
                    if cur_level == 1:
                        water_group1.add(wave0)
                    else:
                        water_group2.add(wave0)
                elif tile == '6':
                    wave1 = Water(col_count * T_SIZE, row_count * T_SIZE, 'images/bg/wave1.png')
                    if cur_level == 1:
                        water_group1.add(wave1)
                    else:
                        water_group2.add(wave1)
                elif tile == '7':
                    btn = GameButton(col_count * T_SIZE, row_count * T_SIZE)
                    if cur_level == 1:
                        btn_group1.add(btn)
                    else:
                        btn_group2.add(btn)
                elif tile == '8':
                    img = pygame.transform.scale(grass, (T_SIZE, T_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * T_SIZE
                    img_rect.y = row_count * T_SIZE
                    tile = (img, img_rect)
                    self.tiles.append(tile)
                elif tile == '9':
                    esc = Escape(col_count * T_SIZE, row_count * T_SIZE)
                    if cur_level == 1:
                        escape_group1.add(esc)
                    else:
                        escape_group2.add(esc)

                col_count += 1
            row_count += 1

    def draw_world(self):
        for tile in self.tiles:
            screen.blit(tile[0], tile[1])


class Snowmen(pygame.sprite.Sprite):
    def __init__(self, x_snowman, y_snowman):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bg/snowman.png')
        self.rect = self.image.get_rect()
        self.x = self.rect.x = x_snowman
        self.y = self.rect.y = y_snowman
        self.direction = 1
        self.count = 0

    def update(self):
        self.rect.x += self.direction
        self.count += 1
        if abs(self.count) > 50:
            self.direction *= -1
            self.count *= -1


class Water(pygame.sprite.Sprite):
    def __init__(self, w_x, w_y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = w_x
        self.rect.y = w_y


class Player(object):
    def __init__(self, x_0, y_0, x_1, y_1):
        global level

        walk_r_0 = [pygame.image.load('images/icons/christmaself/cer0.png'),
                    pygame.image.load('images/icons/christmaself/cer1.png'),
                    pygame.image.load('images/icons/christmaself/cer2.png'),
                    pygame.image.load('images/icons/christmaself/cer3.png'),
                    pygame.image.load('images/icons/christmaself/cer4.png'),
                    pygame.image.load('images/icons/christmaself/cer5.png')]
        walk_l_0 = [pygame.image.load('images/icons/christmaself/cel0.png'),
                    pygame.image.load('images/icons/christmaself/cel1.png'),
                    pygame.image.load('images/icons/christmaself/cel2.png'),
                    pygame.image.load('images/icons/christmaself/cel3.png'),
                    pygame.image.load('images/icons/christmaself/cel4.png'),
                    pygame.image.load('images/icons/christmaself/cel5.png')]
        walk_r_1 = [pygame.image.load('images/icons/santaclause/scr0.png'),
                    pygame.image.load('images/icons/santaclause/scr1.png'),
                    pygame.image.load('images/icons/santaclause/scr2.png'),
                    pygame.image.load('images/icons/santaclause/scr3.png'),
                    pygame.image.load('images/icons/santaclause/scr4.png'),
                    pygame.image.load('images/icons/santaclause/scr5.png')]
        walk_l_1 = [pygame.image.load('images/icons/santaclause/scl0.png'),
                    pygame.image.load('images/icons/santaclause/scl1.png'),
                    pygame.image.load('images/icons/santaclause/scl2.png'),
                    pygame.image.load('images/icons/santaclause/scl3.png'),
                    pygame.image.load('images/icons/santaclause/scl4.png'),
                    pygame.image.load('images/icons/santaclause/scl5.png')]
        self.walk_r_0 = [pygame.transform.scale(i, (50, 100)) for i in walk_r_0]
        self.walk_l_0 = [pygame.transform.scale(i, (50, 100)) for i in walk_l_0]
        self.walk_r_1 = [pygame.transform.scale(i, (50, 100)) for i in walk_r_1]
        self.walk_l_1 = [pygame.transform.scale(i, (50, 100)) for i in walk_l_1]
        self.index0 = 0
        self.index1 = 0
        self.counter0 = 0
        self.counter1 = 0
        self.image0 = pygame.transform.scale(self.walk_r_0[self.index0], (50, 100))
        self.image1 = pygame.transform.scale(self.walk_r_1[self.index0], (50, 100))
        self.rect0 = self.image0.get_rect()
        self.rect1 = self.image1.get_rect()
        self.rect0.x = x_0
        self.rect0.y = y_0
        self.rect1.x = x_1
        self.rect1.y = y_1
        self.width = self.image0.get_width()
        self.height = self.image0.get_height()
        self.delta_jump_y_0 = 0
        self.delta_jump_y_1 = 0
        self.jumping_0 = False
        self.jumping_1 = False
        self.direction_0 = 0
        self.direction_1 = 0
        self.jump_count0 = 0
        self.jump_count1 = 0
        self.rect = self.rect0

    def update(self, world):
        global game_over
        global btns_1_clicked
        global btns_2_clicked
        global level
        global escape

        delta_x = 0
        delta_y = 0
        walk_cooldown = 6

        key = pygame.key.get_pressed()

        if key[pygame.K_UP] and not self.jumping_0 and self.jump_count0 == 0:
            self.delta_jump_y_0 = -15
            self.jumping_0 = True
            self.jump_count0 += 1

        if not key[pygame.K_UP]:
            self.jumping_0 = False

        if key[pygame.K_LEFT]:
            delta_x -= 5
            self.counter0 += 1
            self.direction_0 = -1

        if key[pygame.K_RIGHT]:
            delta_x += 5
            self.counter0 += 1
            self.direction_0 = 1

        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.counter0 = 0
            self.index0 = 0

        if self.direction_0 == 1:
            self.image0 = self.walk_r_0[self.index0]
        if self.direction_0 == -1:
            self.image0 = self.walk_l_0[self.index0]

        if self.counter0 > walk_cooldown:
            self.counter0 = 0
            self.index0 += 1
        if self.index0 >= len(self.walk_r_0):
            self.index0 = 0
        if self.direction_0 == 1:
            self.image0 = self.walk_r_0[self.index0]
        if self.direction_0 == -1:
            self.image0 = self.walk_l_0[self.index0]

        self.delta_jump_y_0 += 1
        if self.delta_jump_y_0 > 10:
            self.delta_jump_y_0 = 10
        delta_y += self.delta_jump_y_0

        for tile in world.tiles:
            if tile[1].colliderect(self.rect0.x + delta_x, self.rect0.y, self.width, self.height):
                delta_x = 0
            if tile[1].colliderect(self.rect0.x, self.rect0.y + delta_y, self.width, self.height):
                if self.delta_jump_y_0 < 0:
                    delta_y = tile[1].bottom - self.rect0.top
                    self.delta_jump_y_0 = 0
                elif self.delta_jump_y_0 >= 0:
                    delta_y = tile[1].top - self.rect0.bottom
                    self.delta_jump_y_0 = 0
            if self.rect0.bottom == tile[1].top and ((tile[1].left <= self.rect0.left <= tile[1].right) or
                                                     (tile[1].left <= self.rect0.right <= tile[1].right)):
                self.jump_count0 = 0

        self.rect0.x += delta_x
        self.rect0.y += delta_y

        if self.rect0.bottom > HEIGHT:
            self.rect0.bottom = HEIGHT

        screen.blit(self.image0, self.rect0)

        if level == 1:
            self.rect = self.rect0
            if pygame.sprite.spritecollide(self, water_group1, False):
                game_over = True
                self.rect0.x = 50
                self.rect0.y = 600
                self.rect1.x = 100
                self.rect1.y = 600
                btns_1_clicked = False
                btns_2_clicked = False
        else:
            self.rect = self.rect0
            if pygame.sprite.spritecollide(self, water_group2, False):
                game_over = True
                self.rect0.x = 50
                self.rect0.y = 500
                self.rect1.x = 100
                self.rect1.y = 500
                btns_1_clicked = False
                btns_2_clicked = False

        delta_x = 0
        delta_y = 0
        walk_cooldown = 6

        key = pygame.key.get_pressed()

        if key[pygame.K_w] and not self.jumping_1 and self.jump_count1 == 0:
            self.delta_jump_y_1 = -15
            self.jumping_1 = True
            self.jump_count1 += 1

        if not key[pygame.K_w]:
            self.jumping_1 = False

        if key[pygame.K_a]:
            delta_x -= 5
            self.counter1 += 1
            self.direction_1 = -1

        if key[pygame.K_d]:
            delta_x += 5
            self.counter1 += 1
            self.direction_1 = 1

        if not key[pygame.K_a] and not key[pygame.K_d]:
            self.counter1 = 0
            self.index1 = 0

        if self.direction_1 == 1:
            self.image1 = self.walk_r_1[self.index1]
        if self.direction_1 == -1:
            self.image1 = self.walk_l_1[self.index1]

        if self.counter1 > walk_cooldown:
            self.counter1 = 0
            self.index1 += 1
        if self.index1 >= len(self.walk_r_1):
            self.index1 = 0
        if self.direction_1 == 1:
            self.image1 = self.walk_r_1[self.index1]
        if self.direction_1 == -1:
            self.image1 = self.walk_l_1[self.index1]

        self.delta_jump_y_1 += 1
        if self.delta_jump_y_1 > 10:
            self.delta_jump_y_1 = 10
        delta_y += self.delta_jump_y_1

        for tile in world.tiles:
            if tile[1].colliderect(self.rect1.x + delta_x, self.rect1.y, self.width, self.height):
                delta_x = 0
            if tile[1].colliderect(self.rect1.x, self.rect1.y + delta_y, self.width, self.height):
                if self.delta_jump_y_1 < 0:
                    delta_y = tile[1].bottom - self.rect1.top
                    self.delta_jump_y_1 = 0
                elif self.delta_jump_y_1 >= 0:
                    delta_y = tile[1].top - self.rect1.bottom
                    self.delta_jump_y_1 = 0
            if self.rect1.bottom == tile[1].top and ((tile[1].left <= self.rect1.left <= tile[1].right) or
                                                     (tile[1].left <= self.rect1.right <= tile[1].right)):
                self.jump_count1 = 0

        self.rect1.x += delta_x
        self.rect1.y += delta_y

        if self.rect1.bottom > HEIGHT:
            self.rect1.bottom = HEIGHT

        screen.blit(self.image1, self.rect1)

        if level == 1:
            self.rect = self.rect1
            if pygame.sprite.spritecollide(self, water_group1, False):
                game_over = True
                self.rect0.x = 50
                self.rect0.y = 600
                self.rect1.x = 100
                self.rect1.y = 600
                btns_1_clicked = False

            if pygame.sprite.spritecollide(self, btn_group1, False):
                self.rect = self.rect0
                if pygame.sprite.spritecollide(self, btn_group1, False):
                    if not self.rect1.colliderect(self.rect0):
                        btns_1_clicked = True
                        btn_group1.update()

            self.rect = self.rect0
            if pygame.sprite.spritecollide(self, escape_group1, False):
                self.rect = self.rect1
                if pygame.sprite.spritecollide(self, escape_group1, False):
                    escape = True
        else:
            self.rect = self.rect1
            if pygame.sprite.spritecollide(self, water_group2, False):
                game_over = True
                self.rect0.x = 50
                self.rect0.y = 500
                self.rect1.x = 100
                self.rect1.y = 500
                btns_2_clicked = False

            if pygame.sprite.spritecollide(self, btn_group2, False):
                self.rect = self.rect0
                if pygame.sprite.spritecollide(self, btn_group2, False):
                    if not self.rect1.colliderect(self.rect0):
                        btns_2_clicked = True
                        btn_group2.update()

            self.rect = self.rect0
            if pygame.sprite.spritecollide(self, escape_group2, False):
                self.rect = self.rect1
                if pygame.sprite.spritecollide(self, escape_group2, False):
                    escape = True


class Button(object):
    def __init__(self,  btn_x, btn_y, btn_width, btn_height, btn_text, font_size, color_0, color_1):
        self.btn_x = btn_x
        self.btn_y = btn_y
        self.btn_width = btn_width
        self.btn_height = btn_height
        self.text = btn_text
        self.font_size = font_size
        self.color_0 = color_0
        self.color_1 = color_1

    def draw_btn(self, scr):
        pygame.draw.rect(scr, pygame.Color(self.color_0),
                         (self.btn_x, self.btn_y, self.btn_width, self.btn_height))
        pygame.draw.rect(scr, pygame.Color(self.color_1),
                         (self.btn_x, self.btn_y, self.btn_width, self.btn_height), 10)

        font = pygame.font.Font('pixel_font.otf', self.font_size)

        b_text = font.render(self.text, True, (0, 0, 0))
        text_rect = b_text.get_rect(center=(self.btn_x + self.btn_width // 2, self.btn_y + self.btn_height // 2))
        scr.blit(b_text, text_rect)


class Escape(pygame.sprite.Sprite):
    def __init__(self, w_x, w_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/bg/escape.png')
        self.rect = self.image.get_rect()
        self.rect.x = w_x
        self.rect.y = w_y


class GameButton(pygame.sprite.Sprite):
    def __init__(self, w_x, w_y):
        pygame.sprite.Sprite.__init__(self)
        self.btn0 = pygame.image.load('images/bg/btn_0.png')
        self.btn1 = pygame.image.load('images/bg/btn_2.png')
        self.image = self.btn0
        self.rect = self.image.get_rect()
        self.rect.x = w_x
        self.rect.y = w_y

    def update(self):
        global level
        global btns_1_clicked
        global btns_2_clicked
        if level == 1:
            if btns_1_clicked:
                self.image = self.btn1
            else:
                self.image = self.btn0
        if level == 2:
            if btns_2_clicked:
                self.image = self.btn1
            else:
                self.image = self.btn0


class Input(object):
    def __init__(self, box_number, *args: int, log=False, checkin=False, user_text=''):
        self.log = log
        self.checkin = checkin
        self.font = pygame.font.Font(None, 30)
        self.rects = []
        for i in range(0, box_number * 4 - 3, 4):
            self.rects.append(pygame.Rect(args[i], args[i + 1], args[i + 2], args[i + 3]))
        self.color = (255, 255, 255)
        self.border_color = (75, 0, 130)
        self.texts = [user_text] * box_number
        self.surfaces = []
        for i in range(box_number):
            self.surfaces.append(self.font.render(self.texts[i], True, (0, 0, 0)))
        self.active = [False] * box_number
        self.answers = [''] * box_number

    def input_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(self.rects)):
                if self.rects[i].x <= e.pos[0] <= self.rects[i].x + self.rects[i].width and \
                        self.rects[i].y <= e.pos[1] <= self.rects[i].y + self.rects[i].height:
                    self.active[i] = not self.active[i]
                else:
                    self.active[i] = False

        if e.type == pygame.KEYDOWN:
            if self.active:
                x_m, y_m = pygame.mouse.get_pos()
                if e.key == pygame.K_RETURN:
                    for i in range(len(self.answers)):
                        self.answers[i] = self.texts[i]
                        self.texts[i] = ''
                elif e.key == pygame.K_BACKSPACE:
                    for i in range(len(self.rects)):
                        if self.rects[i].collidepoint(x_m, y_m):
                            self.texts[i] = self.texts[i][:-1]
                else:
                    for i in range(len(self.rects)):
                        if self.rects[i].collidepoint(x_m, y_m):
                            self.texts[i] += e.unicode

                for i in range(len(self.surfaces)):
                    self.surfaces[i] = self.font.render(self.texts[i], True, 'black')

    def new_size(self):
        for i in range(len(self.rects)):
            old = self.rects[i].width
            width = max(self.rects[i].width, self.surfaces[i].get_width() + 40)
            self.rects[i].x -= (width - old) // 2
            self.rects[i].width = width

    def draw_input_box(self, scr):
        for i in range(len(self.rects)):
            pygame.draw.rect(scr, self.color, self.rects[i])
            pygame.draw.rect(scr, self.border_color, self.rects[i], 10)
            scr.blit(self.surfaces[i], (self.rects[i].x + 20, self.rects[i].y + 44))

        return self.answers


water_group1 = pygame.sprite.Group()
snowmen_group1 = pygame.sprite.Group()
btn_group1 = pygame.sprite.Group()
escape_group1 = pygame.sprite.Group()

water_group2 = pygame.sprite.Group()
snowmen_group2 = pygame.sprite.Group()
btn_group2 = pygame.sprite.Group()
escape_group2 = pygame.sprite.Group()

characters_0 = Player(50, 600, 100, 600)
characters_1 = Player(50, 600, 100, 600)

btn_start = Button(250, 183, 500, 100, "Играть без регистрации", 30, (30, 144, 255), (65, 105, 225))
btn_register = Button(250, 313, 500, 100, "Зарегистрироваться", 30, (30, 144, 255), (65, 105, 225))
btn_log_in = Button(250, 443, 500, 100, "Войти", 30, (30, 144, 255), (65, 105, 225))

btn_levels = Button(880, 630, 100, 50, "Меню", 15, (30, 144, 255), (65, 105, 225))

btn_level1 = Button(100, 240, 300, 100, "Уровень 1", 30, (30, 144, 255), (65, 105, 225))
btn_level2 = Button(100, 360, 300, 100, "Уровень 2", 30, (30, 144, 255), (65, 105, 225))
btn_m_log_in = Button(500, 183, 400, 100, "Войти", 30, (30, 144, 255), (65, 105, 225))
btn_m_register = Button(500, 313, 400, 100, "Зарегистрироваться", 30, (30, 144, 255), (65, 105, 225))
btn_log_out = Button(500, 443, 400, 100, "Выйти из аккаунта", 30, (30, 144, 255), (65, 105, 225))
music_on = Button(100, 480, 140, 63, "Музыка", 20, (30, 144, 255), (65, 105, 225))
sounds_on = Button(260, 480, 140, 63, "Звуки", 20, (30, 144, 255), (65, 105, 225))

btn_err_log_out = Button(250, 300, 500, 100, "Меню", 30, (240, 145, 255), (123, 145, 255))

btn_next = Button(250, 300, 500, 100, "Следующий уровень", 30, (255, 127, 80), (255, 69, 0))
btn_again = Button(250, 420, 500, 100, "Сыграть еще раз", 30, (255, 127, 80), (255, 69, 0))

btn_to_menu = Button(250, 300, 500, 100, "Меню", 30, (0, 0, 139), (176, 224, 230))

btn_reg = Button(575, 600, 350, 50, "Нет аккаунта? Зарегистрируйся!", 15, (250, 216, 147), (240, 200, 65))
btn_play = Button(75, 600, 350, 50, "Играть", 15, (250, 216, 147), (240, 200, 65))

btn_log_again = Button(250, 450, 500, 100, "Попробовать еще раз", 30, (0, 128, 0), (0, 100, 0))

btn_log = Button(575, 600, 350, 50, "Есть аккаунт? Войди!", 15, (250, 216, 147), (240, 200, 65))

btn_log_inn = Button(250, 443, 500, 100, "Войти в аккаунт", 30, (199, 21, 133), (255, 105, 180))

btn_check_again = Button(250, 450, 500, 100, "Попробовать еще раз", 30, (224, 255, 255), (127, 255, 212))

btn_play_again = Button(250, 350, 500, 100, "Попробовать еще раз", 30, (255, 0, 0), (0, 0, 0))

world_1 = World(level_one, 1)
world_2 = World(level_two, 2)


def check_check_in_data(data: list) -> bool:
    login, password0, password1 = data[0], data[1], data[2]
    if password0 == password1 and password0 != '' and login != '' and login != 'Гость':
        con = sqlite3.connect('christmas_game.bd')
        cursor = con.cursor()
        data = cursor.execute("""SELECT * FROM User WHERE login=?""", (login,)).fetchone()
        con.commit()
        con.close()

        if not data:
            return True
    return False


def check_in(data: list) -> None:
    login, password = data[0], data[1]
    con = sqlite3.connect('christmas_game.bd')
    cursor = con.cursor()
    cursor.execute(f"""INSERT INTO User VALUES ('{login}', '{password}', 1, 1, 1)""")
    con.commit()
    con.close()


def check_log_pass(data: list) -> (bool, int, int, int):
    login, password = data[0], data[1]
    con = sqlite3.connect('christmas_game.bd')
    cursor = con.cursor()
    data = cursor.execute("""SELECT * FROM User WHERE login=?""", (login,)).fetchone()
    con.commit()
    con.close()

    if data:
        if password == data[1]:
            return False, data[2], data[3], data[4]
    return True, None, None, None


def absolute_winner_window():
    global running
    global level
    global menu

    screen.fill((152, 251, 152))

    ttext = FONT.render("Это последний уровень!", True, (0, 0, 0))
    text_rect = ttext.get_rect(center=(500, 250))
    screen.blit(ttext, text_rect)

    btn_to_menu.draw_btn(screen)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            btn_sound.play()

            if 250 <= m_x <= 750 and 300 <= m_y <= 400:
                menu = True
                level = 1

    pygame.display.update()


def draw_level_1():
    global win
    global escape

    screen.blit(bg0, (0, 0))

    world_1.draw_world()

    snowmen_group1.update()
    snowmen_group1.draw(screen)

    escape_group1.draw(screen)

    btn_group1.draw(screen)

    water_group1.draw(screen)

    characters_0.update(world_1)
    btn_levels.draw_btn(screen)

    if btns_1_clicked and escape:
        win = True

    pygame.display.update()


def draw_level_2():
    global win
    global escape

    screen.blit(bg1, (0, 0))

    world_2.draw_world()

    snowmen_group2.update()
    snowmen_group2.draw(screen)

    escape_group2.draw(screen)

    btn_group2.draw(screen)

    water_group2.draw(screen)

    characters_1.update(world_2)
    btn_levels.draw_btn(screen)

    while level > 2:
        absolute_winner_window()

    if btns_2_clicked and escape:
        win = True

    pygame.display.update()


def start_window():
    global register
    global log_in
    global start
    global running

    screen.fill((135, 206, 250))

    btn_start.draw_btn(screen)
    btn_register.draw_btn(screen)
    btn_log_in.draw_btn(screen)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            if 250 <= m_x <= 750 and 183 <= m_y <= 283:
                start = False
            elif 250 <= m_x <= 750 and 313 <= m_y <= 413:
                register = True
                start = False
            elif 250 <= m_x <= 750 and 443 <= m_y <= 543:
                log_in = True
                start = False

    pygame.display.update()


def register_window():
    global register
    global running
    global log_in
    global check_in_again
    global successful_check_in

    reg = Input(3, 250, 150, 500, 100, 250, 300, 500, 100, 250, 450, 500, 100)

    in_progress = True

    while in_progress:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                exit()

            reg.input_event(e)

            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if sounds_play == 1:
                    btn_sound.play()

                if 575 <= mouse_x <= 925 and 600 <= mouse_y <= 650:
                    log_in = True
                    register = False
                    in_progress = False

                elif 75 <= mouse_x <= 425 and 600 <= mouse_y <= 650:
                    register = False
                    in_progress = False

        reg.new_size()

        screen.fill((147, 112, 219))

        text_l = FONT.render("Введите логин:", True, (0, 0, 0))
        text_rect = text_l.get_rect(center=(500, 125))
        screen.blit(text_l, text_rect)

        text_l = FONT.render("Введите пароль:", True, (0, 0, 0))
        text_rect = text_l.get_rect(center=(500, 275))
        screen.blit(text_l, text_rect)

        text_l = FONT.render("Повторите пароль:", True, (0, 0, 0))
        text_rect = text_l.get_rect(center=(500, 425))
        screen.blit(text_l, text_rect)

        btn_log.draw_btn(screen)
        btn_play.draw_btn(screen)

        user_data = reg.draw_input_box(screen)
        if user_data[0] != '' or user_data[1] != '' or user_data[2] != '':
            if not check_check_in_data(user_data):
                check_in_again = True
                in_progress = False
                register = False
            else:
                check_in(user_data)
                successful_check_in = True
                register = False
                in_progress = False

        pygame.display.flip()
        clock.tick(30)


def menu_window():
    global menu
    global running
    global level
    global log_in
    global register
    global start
    global err_log_out
    global user_name
    global music_play
    global sounds_play

    screen.fill((135, 206, 250))

    btn_level1.draw_btn(screen)
    btn_level2.draw_btn(screen)
    btn_m_log_in.draw_btn(screen)
    btn_m_register.draw_btn(screen)
    btn_log_out.draw_btn(screen)
    music_on.draw_btn(screen)
    sounds_on.draw_btn(screen)

    font = pygame.font.Font('pixel_font.otf', 20)

    text_l = font.render("ВКЛ", True, (0, 0, 0)) if music_play == 1 else font.render("ВЫКЛ", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(170, 560))
    screen.blit(text_l, text_rect)

    text_l = font.render("ВКЛ", True, (0, 0, 0)) if sounds_play == 1 else font.render("ВЫКЛ", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(330, 560))
    screen.blit(text_l, text_rect)

    text_l = FONT.render(f"Привет, {user_name}!", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(250, 200))
    screen.blit(text_l, text_rect)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            if 100 <= m_x <= 400 and 240 <= m_y <= 340:
                level = 1
                menu = False
            elif 100 <= m_x <= 400 and 360 <= m_y <= 460:
                level = 2
                menu = False
            elif 500 <= m_x <= 900 and 183 <= m_y <= 283:
                log_in = True
                menu = False
            elif 500 <= m_x <= 900 and 313 <= m_y <= 413:
                register = True
                menu = False
            elif 500 <= m_x <= 900 and 443 <= m_y <= 543:
                if user_name != 'Гость':
                    user_name = 'Гость'
                    level = 1
                    music_play = 1
                    sounds_play = 1
                    start = True
                    menu = False
                else:
                    err_log_out = True
                    menu = False
            elif 260 <= m_x <= 400 and 480 <= m_y <= 543:
                sounds_play = 1 - sounds_play
            elif 100 <= m_x <= 240 and 480 <= m_y <= 543:
                music_play = 1 - music_play
                if music_play == 0:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    pygame.display.update()


def check_in_again_window():
    global register
    global running
    global check_in_again

    screen.fill((102, 205, 170))

    text_l = FONT.render("Либо пользователем с таким логином уже", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 150))
    screen.blit(text_l, text_rect)

    text_l = FONT.render("существует, либо пароли, которые вы ввели,", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 200))
    screen.blit(text_l, text_rect)

    text_l = FONT.render("не совпадают, либо вы что-то не ввели.", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 250))
    screen.blit(text_l, text_rect)

    btn_check_again.draw_btn(screen)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            if 250 <= m_x <= 750 and 450 <= m_y <= 550:
                register = True
                check_in_again = False

    pygame.display.update()


def again_log_window():
    global log_in
    global running
    global again_log

    screen.fill((173, 255, 47))

    text_l = FONT.render("Либо вы допустили ошибку", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 150))
    screen.blit(text_l, text_rect)

    text_l = FONT.render("при вводе логина или пароля,", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 200))
    screen.blit(text_l, text_rect)

    text_l = FONT.render("либо такого аккаунта не существует.", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 250))
    screen.blit(text_l, text_rect)

    btn_log_again.draw_btn(screen)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            if 250 <= m_x <= 750 and 450 <= m_y <= 550:
                log_in = True
                again_log = False

    pygame.display.update()


def log_in_window():
    global register
    global log_in
    global running
    global level
    global user_name
    global music_play
    global sounds_play
    global again_log

    login_password = Input(2, 250, 175, 500, 100, 250, 400, 500, 100)

    in_progress = True

    while in_progress:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                exit()

            login_password.input_event(e)

            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if sounds_play == 1:
                    btn_sound.play()

                if 575 <= mouse_x <= 925 and 600 <= mouse_y <= 650:
                    register = True
                    log_in = False
                    in_progress = False

                elif 75 <= mouse_x <= 425 and 600 <= mouse_y <= 650:
                    log_in = False
                    in_progress = False

        login_password.new_size()

        screen.fill((147, 112, 219))

        text_l = FONT.render("Введите логин:", True, (0, 0, 0))
        text_rect = text_l.get_rect(center=(500, 125))
        screen.blit(text_l, text_rect)

        text_l = FONT.render("Введите пароль:", True, (0, 0, 0))
        text_rect = text_l.get_rect(center=(500, 350))
        screen.blit(text_l, text_rect)

        btn_reg.draw_btn(screen)
        btn_play.draw_btn(screen)

        user_data = login_password.draw_input_box(screen)
        if user_data[0] != '' or user_data[1] != '':
            not_correct, curr_level, music, sounds = check_log_pass(user_data)

            if not not_correct:
                level = curr_level
                music_play = music
                sounds_play = sounds
                user_name = user_data[0]
                in_progress = False
                log_in = False
            else:
                again_log = True
                log_in = False
                in_progress = False

        pygame.display.flip()
        clock.tick(30)


def win_window():
    global running
    global win
    global level
    global escape
    global btns_1_clicked
    global btns_2_clicked

    screen.blit(bg_win, (0, 0))

    btn_next.draw_btn(screen)
    btn_again.draw_btn(screen)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            btns_2_clicked = False
            btns_1_clicked = False
            btn_group1.update()
            btn_group2.update()
            escape = False
            characters_0.rect0.x = 50
            characters_0.rect0.y = 500
            characters_0.rect1.x = 100
            characters_0.rect1.y = 500
            characters_1.rect0.x = 50
            characters_1.rect0.y = 500
            characters_1.rect1.x = 100
            characters_1.rect1.y = 500

            if 250 <= m_x <= 750 and 300 <= m_y <= 400:
                level += 1
                win = False
            elif 250 <= m_x <= 750 and 420 <= m_y <= 520:
                win = False

    pygame.display.update()


def err_log_out_window():
    global err_log_out
    global running
    global menu

    screen.fill((112, 85, 255))

    text_l = FONT.render("Вы и так не авторизированы.", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 200))
    screen.blit(text_l, text_rect)

    btn_err_log_out.draw_btn(screen)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            if 250 <= m_x <= 750 and 300 <= m_y <= 400:
                menu = True
                err_log_out = False

    pygame.display.update()


def successful_check_in_window():
    global running
    global log_in
    global successful_check_in

    screen.fill((230, 180, 60))

    btn_log_inn.draw_btn(screen)

    text_l = FONT.render("Регистрация прошла успешно!", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 200))
    screen.blit(text_l, text_rect)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            if 250 <= m_x <= 750 and 443 <= m_y <= 543:
                log_in = True
                successful_check_in = False

    pygame.display.update()


def game_over_window():
    global running
    global game_over
    screen.fill((255, 127, 80))

    btn_play_again.draw_btn(screen)

    text_l = FONT.render("GAME OVER", True, (0, 0, 0))
    text_rect = text_l.get_rect(center=(500, 200))
    screen.blit(text_l, text_rect)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            if 250 <= m_x <= 750 and 350 <= m_y <= 450:
                game_over = False

    pygame.display.update()


running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if sounds_play == 1:
                btn_sound.play()

            if 880 <= x <= 980 and 630 <= y <= 680:
                menu = True

    while start:
        start_window()

    while log_in:
        log_in_window()

    while again_log:
        again_log_window()

    while register:
        register_window()

    while menu:
        menu_window()

    while win:
        win_window()

    while check_in_again:
        check_in_again_window()

    while successful_check_in:
        successful_check_in_window()

    while err_log_out:
        err_log_out_window()

    while game_over:
        game_over_window()

    if not start and not log_in and not again_log and not register and not menu and not win and not game_over \
            and not check_in_again and not successful_check_in and not err_log_out:
        if level == 1:
            draw_level_1()
        else:
            draw_level_2()


if __name__ == '__main__':
    pygame.init()
    pygame.quit()
