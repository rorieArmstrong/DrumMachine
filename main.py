from marshal import load
import pygame
from pygame import mixer
from os import walk

#get history
saved_beats =[]
file = open('./history.txt','r')
for line in file:
    saved_beats.append(line)

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

drum_kit = 'kit3'
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('BEAT MAKER')
label_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 32)
sub_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 21)
index = 100


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
def get_sounds(drum_kit):
    sounds = []
    for (dirpath, dirnames, filenames) in walk('./sounds/'+ drum_kit):
        for sound in filenames:
            sounds.append(Sound(sound[:-4], mixer.Sound('./sounds/'+ drum_kit +'/' + sound)))
    mixer.set_num_channels(len(sounds)*3)
    return sounds
sounds = get_sounds(drum_kit)

#Init variables
fps = 60
timer = pygame.time.Clock()
beats = 8
boxes = []
active = [[False for i in sounds] for j in range(beats)]
bpm = 128
playing = False
active_legnth = 0
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False
beat_name, typing = '', False

#Save menu
def draw_save_menu(beat_name, typing):
    #Cover Screen
    pygame.draw.rect(screen, black , [0,0,WIDTH,HEIGHT])
    save_menu_text = label_font.render('SAVE MENU: Enter a name for your file.', True, white)
    screen.blit(save_menu_text, (400, 40))
    #Save Button
    save_file_button = pygame.draw.rect(screen, grey, [WIDTH//2-200, HEIGHT*0.75, 400,90],0,5)
    save_file_text = label_font.render('Save', True, white)
    screen.blit(save_file_text, (WIDTH//2-40, HEIGHT*0.75+30))
    #Text Box
    text_box = pygame.draw.rect(screen, grey , [400,200,600,200],5,5)
    entry_text = label_font.render(beat_name, True, white)
    screen.blit(entry_text,(430,250))
    #Exit Button
    exit_text = label_font.render('Close', True, white)
    exit_button = pygame.draw.rect(screen, grey, [WIDTH-200, 50, 180,90],0,5)
    screen.blit(exit_text, (WIDTH-180, 70))
    return exit_button, save_file_button, text_box
   
#Load menu
def draw_load_menu(index):
    #Cover Screen
    pygame.draw.rect(screen, black , [0,0,WIDTH,HEIGHT])
    save_menu_text = label_font.render('LOAD MENU: Select a beat to load.', True, white)
    screen.blit(save_menu_text, (400, 40))
    #Load Button
    load_file_button = pygame.draw.rect(screen, grey, [WIDTH//2-400, HEIGHT*0.75, 400,90],0,5)
    load_file_text = label_font.render('Load', True, white)
    screen.blit(load_file_text, (WIDTH//2-240, HEIGHT*0.75+30))
    #Delete Button
    delete_file_button = pygame.draw.rect(screen, red, [WIDTH//2, HEIGHT*0.75, 400,90],0,5)
    delete_file_text = label_font.render('Delete', True, white)
    screen.blit(delete_file_text, (WIDTH//2+160, HEIGHT*0.75+30))
    #Exit button
    exit_button = pygame.draw.rect(screen, grey, [WIDTH-200, 50, 180,90],0,5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH-180, 70))
    #Files
    files_rect = pygame.draw.rect(screen, grey, [190,200,1000,HEIGHT*0.75-200], 5,5)
    if 0 <= index < len(saved_beats):
        pygame.draw.rect(screen, grey, [190,200+index*(HEIGHT*0.75-200)//10,1000,(HEIGHT*0.75-200)/10], 0,5)

    loaded_data = []
    for x in range(0,min(10,len(saved_beats))):
        beat = saved_beats[x]
        name_of_beat = beat[beat.index('name: ')+6:beat.index(', beats:')]
        row_text = sub_font.render(name_of_beat, True, white)
        screen.blit(row_text, (200, 210 + (HEIGHT*0.75-200)//10*x))
        if 0 <= index < len(saved_beats) and x == index:
            loaded_beats = int(beat[beat.index(', beats:')+8:beat.index(', bpm:')])
            loaded_bpm = int(beat[beat.index(', bpm:')+6:beat.index(', selected:')])
            active_sting = beat[beat.index(', selected:')+13:beat.index(', drumkit:')-2]
            active_list = [i.split(', ') for i in active_sting.split('], [')]
            for i in range(len(active_list)):
                for j in range(len(active_list[0])):
                    if active_list[i][j] == 'True':
                        active_list[i][j] = True
                    else:
                        active_list[i][j] = False
            loaded_drumkit = beat[beat.index(', drumkit:')+10:].strip('\n')
            loaded_data = [loaded_beats, loaded_bpm, active_list, loaded_drumkit]
    return exit_button, delete_file_button, load_file_button, files_rect, loaded_data


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
        screen.blit(sub_font.render(sound.name, True, colours_label[sound.active]), (10,30+x))
        x+=(HEIGHT-200)//len(sounds)
        pygame.draw.line(screen, grey, (0,x),(200,x),5)

    border = 3

    colours_active = [green_disabled, green]
    colours_not_active = [grey_disabled,grey]
    #Draws grid of beats and sounds
    for i in range(beats):
        for j in range(len(sounds)):
            if active[i][j]:
                rect = pygame.draw.rect(screen , colours_active[sounds[j].active], [(i*((WIDTH-200)//beats)+200)+border,j*(HEIGHT-200)//len(sounds)+border,((WIDTH-200)//beats)-2*border,((HEIGHT-200)//len(sounds)-2*border)],0,3)
            else:
                rect = pygame.draw.rect(screen ,colours_not_active[sounds[j].active] ,[(i*((WIDTH-200)//beats)+200)+border,j*(HEIGHT-200)//len(sounds)+border,((WIDTH-200)//beats)-2*border,((HEIGHT-200)//len(sounds)-2*border)],0,3)
            pygame.draw.rect(screen ,gold ,[(i*((WIDTH-200)//beats)+200),(j*(HEIGHT-200)//len(sounds)),((WIDTH-200)//beats),((HEIGHT-200)//len(sounds))],5,5)
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
    add_text = label_font.render('+', True, white)
    minus_text = label_font.render('-', True, white)
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

    #Save Menu button
    save_rect = pygame.draw.rect(screen ,grey , [900,HEIGHT - 150,200,48],5,5)
    save_text = label_font.render('Save', True, white)
    screen.blit(save_text, (920, HEIGHT-145))

    #Load Menu button
    load_rect = pygame.draw.rect(screen ,grey , [900,HEIGHT - 100,200,48],5,5)
    load_text = label_font.render('Load', True, white)
    screen.blit(load_text, (920, HEIGHT-95))

    #Clear
    clear_rect = pygame.draw.rect(screen ,red , [1150,HEIGHT - 150,200,100],0,5)
    clear_text = label_font.render('Clear', True, white)
    screen.blit(clear_text, (1170, HEIGHT-115))

    #Save Menu
    if save_menu:
        exit_button, save_file_button, text_box = draw_save_menu(beat_name, typing)

    #Load Menu
    if load_menu:
        exit_button, delete_file_button, load_file_button, files_rect, loaded_data = draw_load_menu(index)

    #Toggle sound
    x=0
    sound_toggles = []
    for sound in sounds:
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
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for box in boxes:
                if box[0].collidepoint(event.pos):
                    coords = box[1]
                    active[coords[0]][coords[1]] = not active[coords[0]][coords[1]]
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
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
            elif save_rect.collidepoint(event.pos):
                save_menu = True
                playing = False
            elif load_rect.collidepoint(event.pos):
                load_menu = True
                playing = False
            for i in range(len(sounds)):
                if sound_toggles[i].collidepoint(event.pos):
                    sounds[i].toggle_active()
        elif event.type == pygame.MOUSEBUTTONUP and not load_menu:
            if text_box.collidepoint(event.pos):
                typing = True
            elif save_file_button.collidepoint(event.pos):
                file = open('history.txt' , 'w')
                saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected:{active}, drumkit:{drum_kit}')
                for beat in saved_beats:
                    file.write(str(beat))
                file.close()
                save_menu = False
                typing = False
                beat_name = ''
            elif exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                typing = False
                beat_name = ''
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                typing = False
                beat_name = ''
            if files_rect.collidepoint(event.pos):
                index = max((event.pos[1]-200)//50,0)
            if load_file_button.collidepoint(event.pos):
                [beats, bpm, active, drum_kit] = loaded_data
                print( index, loaded_data)
                sounds = get_sounds(drum_kit)
                active_beat = 0 
                load_menu = False
            if delete_file_button.collidepoint(event.pos) and len(saved_beats):
                saved_beats.pop(index)
                file = open('history.txt' , 'w')
                for beat in saved_beats:
                    file.write(str(beat))
                file.close()
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name):
                beat_name = beat_name[:-1]
        

    
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