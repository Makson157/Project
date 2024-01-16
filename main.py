import pygame as pgm
import random
import time
import sys
from pygame.locals import *

fps = 25
window_we, window_he = 600, 500
block, pole_h, pole_w = 20, 20, 10
s_freq, d_freq = 0.15, 0.1  # передвижение в сторону и вниз
n_margin = int((window_we - pole_w * block) / 2)
t_margin = window_he - (pole_h * block) - 5
count = 0

colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0), (255, 20, 147), (0, 255, 255), (255, 255, 255), (154, 205, 50))  # синий, зеленый, красный, желтый и другие
colors1 = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30), (255, 20, 147), (0, 255, 255), (255, 255, 255), (154, 205, 50))  # светло-синий, светло-зеленый, светло-красный, светло-желтый и другие
wh, gray, bl = (255, 255, 255), (185, 185, 185), (0, 0, 0) # сокращённые цвета белый, серый и чёрный
brd_color, bg_color, txt_color, title_color, info_color = wh, bl, wh, colors[3], colors[0]
fig_we, fig_he = 5, 5
empty = 'o'

figures = {
    'S': [['ooooo',
           'ooooo',
           'ooxxo',
           'oxxoo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxxo',
           'oooxo',
           'ooooo']],
    'Z': [['ooooo',
           'ooooo',
           'oxxoo',
           'ooxxo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'oxxoo',
           'oxooo',
           'ooooo']],
    'J': [['ooooo',
           'oxooo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxxo',
           'ooxoo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'oooxo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxoo',
           'oxxoo',
           'ooooo']],
    'L': [['ooooo',
           'oooxo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxoo',
           'ooxxo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'oxooo',
           'ooooo'],
          ['ooooo',
           'oxxoo',
           'ooxoo',
           'ooxoo',
           'ooooo']],
    'I': [['ooxoo',
           'ooxoo',
           'ooxoo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'xxxxo',
           'ooooo',
           'ooooo']],
    'O': [['ooooo',
           'ooooo',
           'oxxoo',
           'oxxoo',
           'ooooo']],
    'T': [['ooooo',
           'ooxoo',
           'oxxxo',
           'ooooo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'ooxxo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooooo',
           'oxxxo',
           'ooxoo',
           'ooooo'],
          ['ooooo',
           'ooxoo',
           'oxxoo',
           'ooxoo',
           'ooooo']]
}


def Screenpause():
    pause = pgm.Surface((600, 500), pgm.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    dis_surf.blit(pause, (0, 0))


def main():
    global fps_clock, dis_surf, basic_fon, big_fon
    pgm.init()
    fps_clock = pgm.time.Clock()
    dis_surf = pgm.display.set_mode((window_we, window_he))
    basic_fon = pgm.font.SysFont('arial', 20)
    big_fon = pgm.font.SysFont('verdana', 45)
    pgm.display.set_caption('Прогаммка Тетрис')
    showText('Тетрис')
    while True:  # начинаем игру
        Tetris_run()
        Screenpause()
        showText('Игра окончена')


def Tetris_run():
    cup = emptycup()
    last_move_down = time.time()
    last_side_move = time.time()
    last_fall = time.time()
    going_d = False
    going_l = False
    going_r = False
    points = 0
    level, fall_speed = calcSpeed(points)
    fallingFig = getNewFig()
    nextFig = getNewFig()

    while True:
        if fallingFig == None:
            # если нет падающих фигур, генерируем новую
            fallingFig = nextFig
            nextFig = getNewFig()
            last_fall = time.time()

            if not checkPos(cup, fallingFig):
                return  # если на игровом поле нет свободного места - игра закончена
        quitGame()
        for events in pgm.event.get():
            if events.type == KEYUP:
                if events.key == K_SPACE:
                    Screenpause()
                    showText('Игра на паузе! ')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif events.key == K_LEFT:
                    going_l = False
                elif events.key == K_RIGHT:
                    going_r = False
                elif events.key == K_DOWN:
                    going_d = False

            elif events.type == KEYDOWN:
                # перемещение фигуры вправо и влево
                if events.key == K_LEFT and checkPos(cup, fallingFig, adjX=-1):
                    fallingFig['x'] -= 1
                    going_l = True
                    going_r = False
                    last_side_move = time.time()

                elif events.key == K_RIGHT and checkPos(cup, fallingFig, adjX=1):
                    fallingFig['x'] += 1
                    going_r = True
                    going_l = False
                    last_side_move = time.time()

                # поворачиваем фигуру, если есть место
                elif events.key == K_UP:
                    fallingFig['rotation'] = (fallingFig['rotation'] + 1) % len(figures[fallingFig['shape']])
                    if not checkPos(cup, fallingFig):
                        fallingFig['rotation'] = (fallingFig['rotation'] - 1) % len(figures[fallingFig['shape']])

                # ускоряем падение фигуры
                elif events.key == K_DOWN:
                    going_d = True
                    if checkPos(cup, fallingFig, adjY=1):
                        fallingFig['y'] += 1
                    last_move_down = time.time()

                # мгновенный сброс вниз
                elif events.key == K_RETURN:
                    going_d = False
                    going_l = False
                    going_r = False
                    for i in range(1, pole_h):
                        if not checkPos(cup, fallingFig, adjY=i):
                            break
                    fallingFig['y'] += i - 1

        # управление падением фигуры при удержании клавиш
        if (going_l or going_r) and time.time() - last_side_move > s_freq:
            if going_l and checkPos(cup, fallingFig, adjX=-1):
                fallingFig['x'] -= 1
            elif going_r and checkPos(cup, fallingFig, adjX=1):
                fallingFig['x'] += 1
            last_side_move = time.time()

        if going_d and time.time() - last_move_down > d_freq and checkPos(cup, fallingFig, adjY=1):
            fallingFig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:  # падение
            if not checkPos(cup, fallingFig, adjY=1):  # проверка касания фигурой пола
                addToCup(cup, fallingFig)  # фигура приземлилась добавляем
                points += clearCompleted(cup)
                level, fall_speed = calcSpeed(points)
                fallingFig = None
            else:  # фигура пока не приземлилась, движемся вниз
                fallingFig['y'] += 1
                last_fall = time.time()

        # рисуем окно игры со всеми надписями
        dis_surf.fill(bg_color)
        drawTitle()
        gamecup(cup)
        drawInfo(points, level)
        drawnewFig(nextFig)
        if fallingFig != None:
            drawFig(fallingFig)
        pgm.display.update()
        fps_clock.tick(fps)


def tуxtObjects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stop():
    pgm.quit()
    sys.exit()


def Keys_check():
    quitGame()

    for event in pgm.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showText(text):
    titleSurf, titleRect = tуxtObjects(text, big_fon, title_color)
    titleRect.center = (int(window_we / 2) - 3, int(window_he / 2) - 3)
    dis_surf.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = tуxtObjects('Нажмите любую клавишу клавиатуры для продолжения', basic_fon, title_color)
    pressKeyRect.center = (int(window_we / 2), int(window_he / 2) + 100)
    dis_surf.blit(pressKeySurf, pressKeyRect)

    while Keys_check() == None:
        pgm.display.update()
        fps_clock.tick()


def quitGame():
    for event in pgm.event.get(QUIT):  # проверка всех событий, приводящих к выходу из игры
        stop()
    for event in pgm.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stop()
        pgm.event.post(event)


def calcSpeed(points):
    # вычисляет уровень
    level = int(points / 3) + 1
    fall_speed = 0.27 - (level * 0.05)
    return level, fall_speed


def getNewFig():
    # возвращает новую фигуру со случайным цветом и углом поворота
    shape = random.choice(list(figures.keys()))
    newFigure = {'shape': shape,
                 'rotation': random.randint(0, len(figures[shape]) - 1),
                 'x': int(pole_w / 2) - int(fig_we / 2),
                 'y': -2,
                 'color': random.randint(0, len(colors) - 1)}
    return newFigure


def addToCup(cup, fig):
    for x in range(fig_we):
        for y in range(fig_he):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def emptycup():
    cup = []
    for i in range(pole_w):
        cup.append([empty] * pole_h)
    return cup


def incup(x, y):
    return x >= 0 and x < pole_w and y < pole_h


def checkPos(cup, fig, adjX=0, adjY=0):
    # проверяет, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами
    for x in range(fig_we):
        for y in range(fig_he):
            abovecup = y + fig['y'] + adjY < 0
            if abovecup or figures[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not incup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                return False
    return True


def zaversheno(pole, y):
    for x in range(pole_w):
        if pole[x][y] == empty:
            return False
    return True



def clearCompleted(cup):
    removed_lines = 0
    y = pole_h - 1
    while y >= 0:
        if zaversheno(cup, y):
            for pushDownY in range(y, 0, -1):
                for x in range(pole_w):
                    cup[x][pushDownY] = cup[x][pushDownY - 1]
            for x in range(pole_w):
                cup[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines



def convertCoords(block_x, block_y):
    return (n_margin + (block_x * block)), (t_margin + (block_y * block))


def drawBlock(block_x, block_y, color, pixelx=None, pixely=None):
    # отрисовка квадратных блоков, из которых состоят фигуры
    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(block_x, block_y)
    pgm.draw.rect(dis_surf, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pgm.draw.rect(dis_surf, colors1[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pgm.draw.circle(dis_surf, colors[color], (pixelx + block / 2, pixely + block / 2), 5)


def gamecup(pole):
    # граница игрового поля-стакана
    pgm.draw.rect(dis_surf, brd_color, (n_margin - 4, t_margin - 4, (pole_w * block) + 8, (pole_h * block) + 8),
                  5)

    # фон игрового поля
    pgm.draw.rect(dis_surf, bg_color, (n_margin, t_margin, block * pole_w, block * pole_h))
    for x in range(pole_w):
        for y in range(pole_h):
            drawBlock(x, y, pole[x][y])


def drawTitle():
    titleSurf = big_fon.render('Тетрис', True, title_color)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (window_we - 385, 30)
    dis_surf.blit(titleSurf, titleRect)


def drawInfo(points, level):
    pointsSurf = basic_fon.render(f'Очки: {points}', True, txt_color)
    pointsRect = pointsSurf.get_rect()
    pointsRect.topleft = (window_we - 550, 180)
    dis_surf.blit(pointsSurf, pointsRect)

    levelSurf = basic_fon.render(f'Уровень: {level}', True, txt_color)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (window_we - 550, 250)
    dis_surf.blit(levelSurf, levelRect)

    pausebSurf = basic_fon.render('Пауза: пробел', True, info_color)
    pausebRect = pausebSurf.get_rect()
    pausebRect.topleft = (window_we - 550, 420)
    dis_surf.blit(pausebSurf, pausebRect)

    escbSurf = basic_fon.render('Выход: Esc', True, info_color)
    escbRect = escbSurf.get_rect()
    escbRect.topleft = (window_we - 550, 450)
    dis_surf.blit(escbSurf, escbRect)
    level


def drawFig(fig, pixelx=None, pixely=None):
    figToDraw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertCoords(fig['x'], fig['y'])

    for x in range(fig_we):
        for y in range(fig_he):
            if figToDraw[y][x] != empty:
                drawBlock(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))


def drawnewFig(figure):  # превью следующей фигуры
    nextSurf = basic_fon.render('Следующая:', True, txt_color)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (window_we - 150, 180)
    dis_surf.blit(nextSurf, nextRect)
    drawFig(figure, pixelx=window_we - 150, pixely=230)


if __name__ == '__main__':
    main()