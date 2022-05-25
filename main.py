import pygame
from pygame import mixer

pygame.init()
WIDTH = 1400
HEIGHT = 800

black= (0,0,0)
white = (255,255,255)
grey = (128,128,128)
dark_grey = (208,208,208)
green = (0,255,0)
red = (255, 0 ,0)
gold = (212,175,55)
blue = (0, 255,255)


screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('BEAT MAKER')
label_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 32)
sub_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 32)

fps = 60
timer = pygame.time.Clock()
drums = ['Hi Hat','Snare','Kick','Crash','Clap','Floor Tom']
beats = 16
boxes = []
active = [[False for i in drums] for j in range(beats)]
bpm = 168
playing = False
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
mixer.set_num_channels(len(sounds)*3)

def play_notes():
    for i in range(len(active[active_beat])):
        if active[active_beat][i]:
            sounds[i].play()

def draw_grid(active,beat):
    left_box = pygame.draw.rect(screen ,grey , [0,0,200,HEIGHT-200],5)
    
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
            if active[i][j]:
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

    #Menu
    bottom_box = pygame.draw.rect(screen ,grey , [0,HEIGHT - 200,WIDTH,200],5)

    #Play/Pause Button
    play_pause = pygame.draw.rect(screen ,grey , [50,HEIGHT - 150,200,100],5,5)
    if playing:
        play_text =label_font.render('Pause', True, white)
    else:
        play_text =label_font.render('Play', True, white)
    screen.blit(play_text, (70, HEIGHT-115))

    #BPM
    bpm_rect = pygame.draw.rect(screen ,grey , [300,HEIGHT - 150,200,100],5,5)
    bpm_text = label_font.render('BPM: '+str(bpm), True, white)
    screen.blit(bpm_text, (320, HEIGHT-115))
    bpm_plus_rect = pygame.draw.rect(screen ,green , [505,HEIGHT - 150,48,48],0,5)
    bpm_minus_rect = pygame.draw.rect(screen ,red , [505,HEIGHT - 100,48,48],0,5)
    add_text = sub_font.render('+', True, white)
    minus_text = sub_font.render('-', True, white)
    screen.blit(add_text, (520, HEIGHT-145))
    screen.blit(minus_text, (520, HEIGHT-95))

    #Beats
    beats_rect = pygame.draw.rect(screen ,grey , [600,HEIGHT - 150,200,100],5,5)
    beats_text = label_font.render('Beats: '+str(beats), True, white)
    screen.blit(beats_text, (620, HEIGHT-115))
    beats_plus_rect = pygame.draw.rect(screen ,green , [805,HEIGHT - 150,48,48],0,5)
    beats_minus_rect = pygame.draw.rect(screen ,red , [805,HEIGHT - 100,48,48],0,5)
    screen.blit(add_text, (820, HEIGHT-145))
    screen.blit(minus_text, (820, HEIGHT-95))

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
                    active[coords[0]][coords[1]] = not active[coords[0]][coords[1]]
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                playing = not playing
            elif bpm_plus_rect.collidepoint(event.pos):
                bpm += 1
            elif bpm_minus_rect.collidepoint(event.pos):
                bpm -= 1
            elif beats_plus_rect.collidepoint(event.pos):
                beats += 1
                active.append([False for i in drums])
            elif beats_minus_rect.collidepoint(event.pos):
                beats -= 1
                active.pop()
    
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
                active_beat = 0
                beat_changed = True
    
    pygame.display.flip()

pygame.quit()