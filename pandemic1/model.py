import numpy as np
import random
import pandas as pd

params = {
          "fps":30,
          "width" : 1000,
          "height" : 700,
          "speed" : 5,
          "acc" : 2,
          "ill" : 100,
          "num" : 500,
          "days_contagious" : 40,
          "days_immune" : 20,
          "chance_of_death" : 5, #probability out of 1000
          "prob_stay_well" : 0.2,
          "distance" : 20,
          "close" : 400,
          "start_pandemic" : False}

class Model:

    def __init__(self,params):
        self.identity = 0
        self.sprites = []
        self.params = params
        self.make_sprites()


    def make_sprites(self):
        self.sprites = []
        self.identity = 0
        for i in range(self.params['ill']):
            self.sprites.append(Sprite(False, self.identity,self.params))
            self.identity += 1
        for i in range(self.params['ill'],self.params['num']):
            self.sprites.append(Sprite(True, self.identity,self.params))
            self.identity += 1


    def update_all(self):
        for sprite in self.sprites:
            sprite.update_sprite(self.sprites)
        self.sprites = [s for s in self.sprites if s.live]
        return pd.DataFrame([s.series()for s in self.sprites],
                            columns = ['x','y','well'])

class Sprite:

    def __init__(self,well, identity,params):
        self.identity = identity
        self.sprites = []
        self.well = well
        self.live = True
        self.params = params
        self.x = random.randint(1,self.params['width']-1)
        self.y = random.randint(1,self.params['height']-1)
        self.dx,self.dy = (np.random.randn(2)*
                           self.params['speed']).astype(int)
        if self.well:
            self.days_immune = 0
        else:
            self.days_contagious = self.params['days_contagious']

    def __repr__(self):
        return str(self.identity)

    def series(self):
        return pd.Series([self.x,self.y,self.well],
                        index = ['x','y','well'])

    def is_close(self,other):
        sq_distance =  ((self.x-other.x)**2
                    + (self.y-other.y)**2)
        return sq_distance < self.params['close']

    def update_sprite(self, sprites):
        self.sprites = sprites
        if self.well:
            if self.days_immune > 0:
                self.days_immune -= 1
            if self.days_immune == 0 and self.catch_virus():
                self.well = False
                self.days_contagious = self.params['days_contagious']

        elif not self.well:
            self.close = []
            self.days_contagious -= 1
            if self.days_contagious <= 0:
                self.well  = True
                self.days_immune = self.params['days_immune']
            elif random.randint(1,1000) < self.params['chance_of_death']:
                self.live = False

        self.update_position()

    def catch_virus(self):
        self.close = [sprite for sprite in self.sprites
                      if not sprite.well
                      if self.is_close(sprite)]
        n = len(self.close)
        if n == 0:
            return False
        else:
            return np.max(np.random.rand(n)) > self.params['prob_stay_well']

    def update_position(self):
        self.ddx , self.ddy = (np.random.randn(2)*
                               self.params['acc']).astype(int)
        self.x += self.dx + self.ddx
        self.y += self.dy + self.ddy
        self.adjust()

    def adjust(self):
        if self.x > self.params['width']:
            self.x = 0
        if self.x < 0:
            self.x = self.params['width']
        if self.y < 0:
            self.y = self.params['height']
        if self.y > self.params['height']:
            self.y = 0
