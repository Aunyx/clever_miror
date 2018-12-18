#!/usr/bin/env python
import os
import sys
import time
#import path
#import basic pygame modules
import pygame
from pygame.locals import *

#Constants :
main_dir = os.path.split(os.path.abspath(__file__))[0]

HEIGHT = 640
WIDTH = 960
FONT_SIZE = 30
SCREENRECT = Rect(0, 0, WIDTH, HEIGHT)
logfile=open('log.txt','a')
logfile.write('\nINFO : openned at ' + str(time.time()) )

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs



class TextSurface(pygame.sprite.Sprite):
    def __init__(self, name, area_x=0, area_y=0 ,color='white'):
        global logfile
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        self.font = pygame.font.Font(None, FONT_SIZE)# TODO : change the font
        self.color = Color(color)#Color of the font
        self.init_text="Init surface text"
        self.changeText(self.init_text)
        self.rect = self.image.get_rect().move(area_x, area_y)
        logfile.write("\nINFO : created new TextSurface" + str(name))
        #self.parentSurface=

    def changeText(self,txt):
        self.image = self.font.render(txt, 0, self.color)

    def update(self):#needed when using sprites
        pass



def main(winstyle = 0):
 # Initialize pygame
    if pygame.get_sdl_version()[0] == 2:
        pygame.mixer.pre_init(44100, 32, 2, 1024)
    pygame.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        logfile.write('\nWARNING : no sound')
        pygame.mixer = None


    clock = pygame.time.Clock()

    # Set the display mode
    winstyle = 0
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #load images


    #Customize the window
    pygame.display.set_caption('Clever mirror display')
    pygame.mouse.set_visible(0)


    #create the background, tile the bgd image
    background = pygame.Surface(SCREENRECT.size)
    background.fill([0,0,0])#Black

    #for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    #    background.blit(bgdtile, (x, 0))

    screen.blit(background, (0,0))
    pygame.display.flip()

    #Initialize groups
    answer = pygame.sprite.Group()
    weather = pygame.sprite.Group()
    speech_recognition_ouput = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()

    #Assign default groups to sprite classes
    TextSurface.containers=all


    debug_surface= TextSurface('debug display')
    debug_surface.changeText('Test text')
    all.add(debug_surface)

    speech_recog_surface = TextSurface('debug display',area_x=WIDTH-FONT_SIZE*20,area_y=HEIGHT-FONT_SIZE*2)
    speech_recog_surface.changeText('Speech recognition output')
    all.add(speech_recog_surface)


    all.update()
    while 1:

        #clear/erase the last drawn sprites
        all.clear(screen, background)

        #update all the sprites
        all.update()

        #update the display
        pygame.display.update(all.draw(screen))


        clock.tick(40)

if __name__ == '__main__':
    main()

    logfile.write('\nINFO : closed at ' + str(time.time()) )
    logfile.close()
