import pygame

pygame.init()
WIDTH = 1400
HEIGHT = 800

black= (0,0,0)
white = (255,255,255)
grey = (128,128,128)

screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('BEAT MAKER')
label_font = pygame.font.Font('./fonts/Roboto-Bold.ttf', 32)

fps = 60
timer = pygame.time.Clock()
drums = ['Hi Hat','Snare','Kick','Crash','Clap','Floor Tom']
beats = 16
boxes = []
active = []

def draw_grid():
    left_box = pygame.draw.rect(screen ,grey , [0,0,200,HEIGHT-200],5)
    bottom_box = pygame.draw.rect(screen ,grey , [0,HEIGHT - 200,WIDTH,200],5)

    
    colours = [grey, white, grey]

    x = 0

    for drum in drums:
        screen.blit(label_font.render(drum, True, white), (30,30+x))
        x+=(HEIGHT-200)//len(drums)
        pygame.draw.line(screen, grey, (0,x),(200,x),5)

    for i in range(beats):
        for j in range(len(drums)):
            rect = pygame.draw.rect(screen ,grey ,[(i*((WIDTH-200)//beats)+200),(j*100),((WIDTH-200)//beats),((HEIGHT-200)//len(drums))],5,5)
            boxes.append((rect,(i,j)))
    return boxes

run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for box in boxes:
                if box[0].colliderect(event.pos):
                    coords = box[1]
        pygame.display.flip()

pygame.quit()