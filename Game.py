

import pygame
import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox

class cube(object): # create snakes body , the cubes
    rows = 20
    w = 500
    def __init__(self,start,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2, dis-2))

        #  eyes of the snake( the head )
        if eyes:
            centre = dis //2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis- radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0) , circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0) , circleMiddle2, radius)
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT] and self.dirnx != 1 and self.dirny != 0:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT] and self.dirnx != -1 and self.dirny != 0:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP] and self.dirnx != 0 and self.dirny != 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN] and self.dirnx != 0 and self.dirny != -1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # adding a cube to the end of snake
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0 :
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy ==0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0 :
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizebetween = w // rows

    x = 0
    y = 0
    for i in range (rows):
        x = x + sizebetween
        y = y + sizebetween

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y) , positions))) > 0:
            continue
        else:
            break

    return (x,y)

def message_box(subject, content, score):
    print (score)
    master = tk.Tk()
    master.title('Score')
    w = Label(master, text =" your score is :")
    w.place(x = 40, y = 50)
    l = Label(master, text = score)
    l.place(x=130, y=50)
    messagebox.showinfo(subject, content)
    mainloop()

def main():
    global width, rows, s, snack, score
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10,10))
    snack = cube(randomSnack(rows, s), color = (0,255,0))
    flag = True

    Clock = pygame.time.Clock()
    score = 0
    while flag:
        pygame.time.delay(50)
        Clock.tick(20)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range (len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('score: ', len(s.body))
                score = len(s.body)
                message_box('you lost', 'play again...', str(score))
                s.reset((10,10))
                break
        redrawWindow(win)

main()
