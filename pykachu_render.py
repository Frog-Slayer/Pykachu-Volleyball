import pygame
import json
from PIL import Image

ASSETS_PATH = 'assets'
IMAGE_PATH = ASSETS_PATH + '/images'
SOUND_PATH = ASSETS_PATH + '/sounds'

with open(IMAGE_PATH+ '/sprite_sheet.json') as f:
    sprite_json = json.load(f)

sprite_png = Image.open(IMAGE_PATH + '/sprite_sheet.png') 

class Texture:
    def __init__(self) -> None:
        self.SKY_BLUE = 'objects/sky_blue.png';
        self.MOUNTAIN = 'objects/mountain.png';
        self.GROUND_RED = 'objects/ground_red.png';
        self.GROUND_LINE = 'objects/ground_line.png';
        self.GROUND_LINE_LEFT_MOST = 'objects/ground_line_leftmost.png';
        self.GROUND_LINE_RIGHT_MOST = 'objects/ground_line_rightmost.png';
        self.GROUND_YELLOW = 'objects/ground_yellow.png';
        self.NET_PILLAR_TOP = 'objects/net_pillar_top.png';
        self.NET_PILLAR = 'objects/net_pillar.png';
        self.SHADOW = 'objects/shadow.png';
        self.BALL_HYPER = 'ball/ball_hyper.png';
        self.BALL_TRAIL = 'ball/ball_trail.png';
        self.BALL_PUNCH = 'ball/ball_punch.png';
        self.CLOUD = 'objects/cloud.png';
        self.WAVE = 'objects/wave.png';
        self.BLACK = 'objects/black.png';

        self.SACHISOFT = 'messages/common/sachisoft.png';
        self.READY = 'messages/common/ready.png';
        self.GAME_END = 'messages/common/game_end.png';

        self.MARK = 'messages/ja/mark.png';
        self.POKEMON = 'messages/ja/pokemon.png';
        self.PIKACHU_VOLLEYBALL = 'messages/ja/pikachu_volleyball.png';
        self.FIGHT = 'messages/ja/fight.png';
        self.WITH_COMPUTER = 'messages/ja/with_computer.png';
        self.WITH_FRIEND = 'messages/ja/with_friend.png';
        self.GAME_START = 'messages/ja/game_start.png';
        self.SITTING_PIKACHU = 'sitting_pikachu.png';

    def getPikachuTexture(i ,j):
        return f'pikachu/pikachu_{i}_{j}.png'

    def getBallTexture(i):
        return f'ball/ball_{i}.png'

    def getNumberTexture(i):
        return f'number/number_{i}.png'

    def getCroppedImage(path): #works well
        frame = sprite_json['frames'][path]['frame']
        rect = (frame['x'], frame['y'], frame['x'] + frame['w'], frame['y'] + frame['h']) 
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(sprite_png, (0, 0), rect)

        return image

class BallAnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position):
        super(BallAnimatedSprite, self).__init__()

        images = []
        ballTextureArray = [
            Texture.getBallTexture(0),
            Texture.getBallTexture(1),
            Texture.getBallTexture(2),
            Texture.getBallTexture(3),
            Texture.getBallTexture(4),
            Texture.getBallTexture('hyper'),
        ]

        for _ in ballTextureArray:
            images.append(Texture.getCroppedImage(_))
        
            self.images = images
            self.index = 0
            self.image = self.images[self.index]

    def update(self):
        self.index = (self.index + 1) % len(self.images);
        self.image = self.images[self.index]

class PlayerAnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position):
            super(BallAnimatedSprite, self).__init__()

            images = []
            for i in range(7):
                if i == 3:
                    images.append(Texture.getCroppedImage(Texture.getPikachuTexture(i, 0)))
                    images.append(Texture.getCroppedImage(Texture.getPikachuTexture(i, 1)))
                elif i == 4:
                    images.append(Texture.getCroppedImage(Texture.getPikachuTexture(i, 0)))
                else:
                    for j in range(5):
                        images.append(Texture.getCroppedImage(Texture.getPikachuTexture(i, j)))

                self.images = images
                self.index = 0
                self.image = self.images[self.index]

    def update(self):
        self.index = (self.index + 1) % len(self.images);
        self.image = self.images[self.index]

