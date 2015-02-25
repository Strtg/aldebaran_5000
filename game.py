from __future__ import print_function
import pickle

from config import SAVES
import config
from config import Config as C
from render import Render as R
import render
import os
import datetime
import game_object
import layers
from debugator import debugator
import time


class Camera(object):
    pos = [0, 0]
    followed = None
    speed = 0
    render_camera = None

    is_moving_left = 0
    is_moving_right = 0
    is_moving_up = 0
    is_moving_down = 0

    @staticmethod
    @debugator
    def follow(something):
        Camera.followed = something

    @staticmethod
    @debugator
    def update():
        if Camera.is_moving_left:
            Camera.pos[0] += Camera.speed
        if Camera.is_moving_right:
            Camera.pos[0] -= Camera.speed
        if Camera.is_moving_up:
            Camera.pos[1] += Camera.speed
        if Camera.is_moving_down:
            Camera.pos[1] -= Camera.speed
        Camera.render_camera.pos = Camera.pos

    @staticmethod
    @debugator
    def init():
        Camera.speed = C.config_dict['camera_speed']
        Camera.render_camera = render.Camera

class Game(object):
    is_pause = False

    playing = None  #

    @staticmethod
    @debugator
    def new(name='New Game created by new_game() function!!!', difficulty='normal'):
        Game.is_pause = False
        Game.name = name
        Game.difficulty = difficulty
        Game.date_of_creating = datetime.datetime.now()
        Game.playing = Stage()  # object manager and game instance to save/load
        Game.current_stage = Game.playing
        Game.playing.create_object(game_object.Visible(l=90.100001, app='button01'))
        Game.playing.create_object(game_object.Visible(l=90.1, app='bubbles'))

        Camera.init()

        print ('NEW GAME!!!')

    @staticmethod
    @debugator
    def save():
        f = open(SAVES + os.sep + 'savedgame' + config.SAVE_EXT, 'wb')
        pickler = pickle.Pickler(f, 2)
        pickler.dump(Game.playing)
        f.close()
        del pickler

    @staticmethod
    @debugator
    def load():
        f = open(SAVES + os.sep + 'savedgame' + config.SAVE_EXT, 'rb')
        unpickler = pickle.Unpickler(f)
        Game.playing = unpickler.load()
        f.close()
        del unpickler


    @staticmethod
    # @debugator
    def update():
        Camera.update()
        if Game.is_pause:
            pass
        else:
            print('UPDATE {0:11.22f}'.format(time.time()))
            print(Camera.pos)

    @staticmethod
    @debugator
    def show_info():
        print (Game.playing.name)
        print (Game.playing.difficulty)
        print (Game.playing.date_of_creating)

    @staticmethod
    @debugator
    def switch_pause():
        if Game.is_pause:
            Game.is_pause = False
            R.set_pause(False)
        else:
            Game.is_pause = True
            R.set_pause(True)


class Stage(object):  # object manager

    @debugator
    def __init__(self):
        self.objects = {}
        self.name = None
        self.difficulty = None
        self.date_of_creating = datetime.datetime.now()
    def create_object(self, obj):
        self.objects.update({obj.id: obj})
        R.sprite_container.register(self, obj.id)

    def give_me_data(self, id):
        data = {}
        data.update({'id': self.objects[id].id})
        data.update({'appearance': self.objects[id].appearance})
        data.update({'layer': self.objects[id].layer})
        return data


