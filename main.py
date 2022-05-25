import pygame
from pygame import mixer

#Colours and Display settings
pygame.init()
WIDTH = 1400
HEIGHT = 800
black= (0,0,0)
white = (255,255,255)
grey = (128,128,128)
grey_disabled = (220,220,220)
dark_grey = (208,208,208)
green = (0,255,0)
green_disabled = (181,255,181)
red = (255, 0 ,0)
gold = (212,175,55)
blue = (0, 255,255)

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('BEAT MAKER')
label_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 32)
sub_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 32)


#create sounds class
class Sound:
    def __init__(self,name,sound):
        self.name = name
        self.sound = sound
        self.active = True

    def play(self):
        self.sound.play()

    def toggle_active(self):
        self.active = not self.active

#Import sounds
sounds = []
sounds.append(Sound("Hi Hat", mixer.Sound('./sounds/hi hat.WAV')))
sounds.append(Sound("Snare", mixer.Sound('./sounds/snare.WAV')))
sounds.append(Sound("Crash", mixer.Sound('./sounds/crash.WAV')))
sounds.append(Sound("Clap", mixer.Sound('./sounds/clap.WAV')))
sounds.append(Sound("Kick", mixer.Sound('./sounds/kick.WAV')))
sounds.append(Sound("Tom", mixer.Sound('./sounds/tom.WAV')))
mixer.set_num_channels(len(sounds)*3)

#Init variables
fps = 60
timer = pygame.time.Clock()
beats = 8
boxes = []
active = [[False for i in sounds] for j in range(beats)]
bpm = 168
playing = False
active_legnth = 0
active_beat = 0
beat_changed = True

#Play sounds
def play_notes():
    for i in range(len(active[active_beat])):
        if active[active_beat][i] and sounds[i].active:
            sounds[i].play()

#Draws main grid
def draw_grid(active,beat):
    left_box = pygame.draw.rect(screen ,grey , [0,0,200,HEIGHT-200],5)
    
    colours_label = [grey, white]

    x = 0
    boxes = []

    #Label for sounds
    for sound in sounds:
        screen.blit(label_font.render(sound.name, True, colours_label[sound.active]), (30,30+x))
        x+=(HEIGHT-200)//len(sounds)
        pygame.draw.line(screen, grey, (0,x),(200,x),5)

    border = 3

    colours_active = [green_disabled, green]
    colours_not_active = [grey_disabled,grey]
    #Draws grid of beats and sounds
    for i in range(beats):
        for j in range(len(sounds)):
            if active[i][j]:
                rect = pygame.draw.rect(screen , colours_active[sounds[j].active], [(i*((WIDTH-200)//beats)+200)+border,(j*100)+border,((WIDTH-200)//beats)-2*border,((HEIGHT-200)//len(sounds)-2*border)],0,3)
            else:
                rect = pygame.draw.rect(screen ,colours_not_active[sounds[j].active] ,[(i*((WIDTH-200)//beats)+200)+border,(j*100)+border,((WIDTH-200)//beats)-2*border,((HEIGHT-200)//len(sounds)-2*border)],0,3)
            pygame.draw.rect(screen ,gold ,[(i*((WIDTH-200)//beats)+200),(j*100),((WIDTH-200)//beats),((HEIGHT-200)//len(sounds))],5,5)
            boxes.append((rect,(i,j)))

        current = pygame.draw.rect(screen, blue, [beat*((WIDTH-200)//beats)+200, 0, ((WIDTH-200)//beats), HEIGHT-200],3,3)
    return boxes

#Run Pygame
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

    #Save
    save_rect = pygame.draw.rect(screen ,grey , [900,HEIGHT - 150,200,48],5,5)
    save_text = label_font.render('Save', True, white)
    screen.blit(save_text, (920, HEIGHT-145))

    #Load
    load_rect = pygame.draw.rect(screen ,grey , [900,HEIGHT - 100,200,48],5,5)
    load_text = label_font.render('Load', True, white)
    screen.blit(load_text, (920, HEIGHT-95))

    #Clear
    clear_rect = pygame.draw.rect(screen ,red , [1150,HEIGHT - 150,200,100],0,5)
    clear_text = label_font.render('Clear', True, white)
    screen.blit(clear_text, (1170, HEIGHT-115))

    #Toggle sound
    x=0
    sound_toggles = []
    for drum in sounds:
        rect = pygame.rect.Rect((0,x),(200,(HEIGHT-200)//len(sounds)))
        x+=(HEIGHT-200)//len(sounds)
        sound_toggles.append(rect)

    #Calls play note when progressed to next beat
    if beat_changed:
        play_notes()
        beat_changed = False

    #Event handler
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
                active.append([False for i in sounds])
            elif beats_minus_rect.collidepoint(event.pos):
                beats -= 1
                active.pop()
            elif clear_rect.collidepoint(event.pos):
                active = [[False for i in sounds] for j in range(beats)]
            for i in range(len(sounds)):
                if sound_toggles[i].collidepoint(event.pos):
                    sounds[i].toggle_active()
            
    #Beat progession
    beat_legnth = 3600//bpm

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