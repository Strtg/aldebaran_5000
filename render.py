from __future__ import print_function
import pygame
import os

import config  # for configurations (resolutions, fullscreen and mod paths for image load
import const  # for game name in window caption
import classes
import layer
import utils

pause_fps = 0  # fps when pause
used_fps = 0  # current fps
screen = None  # display screen surface
rect = None  # display screen surface rect
fpsclock = None  # fps displayer and counter
image_paths = {}  # name without ext is key, full path is value
font_paths = {}
sound_paths = {}  # same as image_paths but for sound
images = {}  # loaded images
fonts = {}
hud_container = None  # group for all sprites
onmap_container = None  # group for all sprites
renderable_container = None  # group for all sprites
offmap_container = None

def setup():  # initialize all global variables
    pygame.init()
    global pause_fps, used_fps, screen, image_paths, rect, hud_container, onmap_container, renderable_container, offmap_container
    pause_fps = config.config_dict['pause_fps']
    used_fps = config.config_dict['maxfps']

    if config.config_dict['fullscreen']:
        pygame.display.set_mode(config.config_dict['resolution'], pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(config.config_dict['resolution'])
    pygame.display.set_caption(const.GAME_NAME)
    screen = pygame.display.get_surface()
    rect = screen.get_rect()
    hud_container = SpriteManager()
    onmap_container = SpriteManager()
    renderable_container = SpriteManager()
    offmap_container = SpriteManager()


def reconfigure():
    global pause_fps, used_fps, screen, rect
    pause_fps = config.config_dict['pause_fps']
    used_fps = config.config_dict['maxfps']

    if config.config_dict['fullscreen']:
        pygame.display.set_mode(config.config_dict['resolution'], pygame.FULLSCREEN)
    else:
        pygame.display.set_mode(config.config_dict['resolution'])
    pygame.display.set_caption(const.GAME_NAME)
    screen = pygame.display.get_surface()
    rect = screen.get_rect()


def setup_fps():
    global fpsclock
    fpsclock = classes.FpsClock()
    background = classes.HUD_Sprite(pygame.Surface(rect.size), rect.topleft, layer.background)
    background.image.convert()
    background.visible =1
    background.image.fill((50, 0, 0))


def load_resources():
    global image_paths, font_paths, sound_paths, images, fonts
    image_paths = do_resource_paths_dict('.png')
    font_paths = do_resource_paths_dict('tf')
    sound_paths = do_resource_paths_dict('.ogg')
    images = load_images(image_paths)


def load_images(dict):
    images = {}
    for name, path in dict.items():
        if '-t-' in name:
            images.update({name: utils.load_image(path)})
        else:
            images.update({name: utils.load_image(path, None)})
    return images


def do_resource_paths_dict(ext):
    images = {}
    for path in config.mods_paths:
        for item in os.listdir(path):
            if os.path.isfile(path + os.sep + item):
                if item.lower().endswith(ext):
                    images.update({item.rsplit('.',1)[0]: path+'/'+item})
                    print(path+'/'+item, 'loaded.')
                    print(item.rsplit(ext,1)[0])

    for n, p in images.items():
        print(n, '\t', p)
    return images


def set_pause(bool):
    global  used_fps
    if bool:
        used_fps = pause_fps
    else:
        used_fps = config.config_dict['maxfps']


def render():
    global screen
    renderable_container.update()
    rects = renderable_container.draw(screen)
    pygame.display.update(rects)





class SpriteManager(pygame.sprite.LayeredDirty):
    def __init__(self):
        super(SpriteManager, self).__init__()

    def register(self, image):
        self.add(Sprite(image))


    def update(self):
        super(SpriteManager, self).update()





class Sprite(pygame.sprite.DirtySprite):
    def __init__(self, image):
        super(Sprite, self).__init__()
        self.pos = (image._pos.xy)
        self.plane = image.plane

    def update(self):

        self.dirty = 1
        for group in self.groups():
            group.change_layer(self, self.layer)
        if self.scroll:
            self.rect.x = self.pos[0]+self.plane.camera.pos[0]
            self.rect.y = self.pos[1]+self.plane.camera.pos[1]


if __name__ == '__main__':
    print(do_resource_paths_dict('.png'))