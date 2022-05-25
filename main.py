import pygame
from pygame import mixer

pygame.init()
WIDTH = 1400
HEIGHT = 800

black= (0,0,0)
white = (255,255,255)
grey = (128,128,128)
green = (0,255,0)
red = (255, 0 ,0)
gold = (212,175,55)
blue = (0, 255,255)


screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('BEAT MAKER')
label_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 32)

fps = 60
timer = pygame.time.Clock()
drums = ['Hi Hat','Snare','Kick','Crash','Clap','Floor Tom']
beats = 16
boxes = []
active = [[False for i in range(beats)] for j in drums]
bpm = 108
playing = True
active_legnth = 0
active_beat = 0
beat_changed = True

#sounds
clap = mixer.Sound('./sounds/clap.WAV')
crash = mixer.Sound('./sounds/crash.WAV')
hi_hat = mixer.Sound('./sounds/hi hat.WAV')
kick = mixer.Sound('./sounds/kick.WAV')
snare = mixer.Sound('./sounds/snare.WAV')
tom = mixer.Sound('./sounds/tom.WAV')
sounds = [hi_hat,snare,kick,crash,clap,tom]

def play_notes():
    for i in range(len(active)):
        if active[i][active_beat]:
            sounds[i].play()

def draw_grid(active,beat):
    left_box = pygame.draw.rect(screen ,grey , [0,0,200,HEIGHT-200],5)
    bottom_box = pygame.draw.rect(screen ,grey , [0,HEIGHT - 200,WIDTH,200],5)
    
    colours = [grey, white, grey]

    x = 0
    boxes = []

    for drum in drums:
        screen.blit(label_font.render(drum, True, white), (30,30+x))
        x+=(HEIGHT-200)//len(drums)
        pygame.draw.line(screen, grey, (0,x),(200,x),5)

    border = 3

    for i in range(beats):
        for j in range(len(drums)):
            if active[j][i]:
                rect = pygame.draw.rect(screen ,green ,[(i*((WIDTH-200)//beats)+200)+border,(j*100)+border,((WIDTH-200)//beats)-2*border,((HEIGHT-200)//len(drums)-2*border)],0,3)
            else:
                rect = pygame.draw.rect(screen ,grey ,[(i*((WIDTH-200)//beats)+200)+border,(j*100)+border,((WIDTH-200)//beats)-2*border,((HEIGHT-200)//len(drums)-2*border)],0,3)
            pygame.draw.rect(screen ,gold ,[(i*((WIDTH-200)//beats)+200),(j*100),((WIDTH-200)//beats),((HEIGHT-200)//len(drums))],5,5)
            boxes.append((rect,(i,j)))

        current = pygame.draw.rect(screen, blue, [beat*((WIDTH-200)//beats)+200, 0, ((WIDTH-200)//beats), HEIGHT-200],3,3)
    return boxes

run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(active,active_beat)

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in boxes:
                if box[0].collidepoint(event.pos):
                    coords = box[1]
                    active[coords[1]][coords[0]] = not active[coords[1]][coords[0]]
    
    beat_legnth = 3600 // bpm

    if playing:
        if active_legnth < beat_legnth:
            active_legnth += 1
        else:
            active_legnth = 0
            if active_beat< beats-1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 1
                beat_changed = True
    
    pygame.display.flip()

pygame.quit()