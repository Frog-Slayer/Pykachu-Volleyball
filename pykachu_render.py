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
        self.position = position

    def update(self):
        self.index = (self.index + 1) % len(self.images);
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def set_position(self, x, y):
        self.position = (x, y)


class PlayerAnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position):
            super(PlayerAnimatedSprite, self).__init__()

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
            self.position = position

            self.scale.x = 1
            self.scale.y = 1

    def update(self):
        self.index = (self.index + 1) % len(self.images);
        self.image = pygame.transform.scale_by(self.images[self.index], (self.scale.x, self.scale.y))
        self.rect = self.image.get_rect()
        self.rect.center = self.position

class SpriteWithAnchor(pygame.sprite.Sprite):

    def __init__(self, path, position):
        self.image = Texture.getCroppedImage(path) 
        self.position = position
        self.scale.x = 1
        self.scale.y = 1

    def update(self):
        self.image = pygame.transform.scale_by(self.image, (self.scale.x, self.scale.y))
        self.rect = self.image.get_rect()
        self.rect.center = self.position

class GameViewDrawer:
    
    def __init__(self):
        self.player1 = PlayerAnimatedSprite((0, 0))
        self.player2 = PlayerAnimatedSprite((0, 0))
        self.ball = BallAnimatedSprite((0, 0))
        self.ballTrail = SpriteWithAnchor(Texture.BALL_TRAIL, (0.5, 0.5))
        self.ballHyper = SpriteWithAnchor(Texture.BALL_HYPER, (0.5, 0.5))
        self.punch = SpriteWithAnchor(Texture.BALL_PUNCH, (0.5, 0.5))
    
    def draw_players_and_ball(self, physics):
        player1 = physics.player1
        player2 = physics.player2
        ball = physics.ball

        self.player1.position = (player1.x, player1.y)

        if player1.state == 3 or player1.state == 4:
            self.player1.scale.x = -1 if player1.divingDirection == -1 else 1 
        else:
            self.player1.scale.x = 1

        self.player2.x = player2.x
        self.player2.y = player2.y

        if player2.state == 3 or player2.state == 4:
            self.player2.scale.x = 1 if player2.divingDirection == 1 else -1 
        else:
            self.player2.scale.x = -1

        self.ball.position = (ball.x, ball.y)

        if ball.punchEffectRadius > 0:
            ball.punchEffectRadius -= 2
            self.punch.scale= (2 * ball.punchEffectRadius, 2 * ball.punchEffectRadius)
            self.punch.position = (ball.punchEffectX, ball.punchEffectY)
            self.punch.visible = True
        else:
            self.punch.visible = False
        
        if ball.isPowerHit:
            self.ballHyper.position = (ball.previousX, ball.previousY)
            self.ballTrail.position = (ball.previousPreviousX, ball.previousPreviousY)
            
            self.ballHyper.visible = True
            self.ballTrail.visible = True
        else:
            self.ballHyper.visible = False
            self.ballTrail.visible = False
