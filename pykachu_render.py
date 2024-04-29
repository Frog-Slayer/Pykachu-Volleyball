import pygame
import json
from PIL import Image

ASSETS_PATH = 'assets'
IMAGE_PATH = ASSETS_PATH + '/images'
SOUND_PATH = ASSETS_PATH + '/sounds'

with open(IMAGE_PATH+ '/sprite_sheet.json') as f:
    sprite_json = json.load(f)


class Scale:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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

        self.sheet = None

    def getPikachuTexture(i ,j):
        return f'pikachu/pikachu_{i}_{j}.png'

    def getBallTexture(i):
        return f'ball/ball_{i}.png'

    def getNumberTexture(i):
        return f'number/number_{i}.png'

    def getCroppedImage(self, path): #works well
        if self.sheet is None: 
            self.sheet= pygame.image.load(IMAGE_PATH + '/sprite_sheet.png').convert()

        frame = sprite_json['frames'][path]['frame']
        rect = (frame['x'], frame['y'], frame['w'], frame['h']) 
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image

class BallAnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, position, texture):
        super(BallAnimatedSprite, self).__init__()
        self.texture = texture

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
            images.append(self.texture.getCroppedImage(_))
        
        self.images = images
        self.index = 0
        self.image = self.images[self.index]
        self.position = position
        self.rect = None

    def update(self):
        self.index = (self.index + 1) % len(self.images);
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        pygame.display.get_surface().blit(self.image, self.rect)

    def set_position(self, x, y):
        self.position = (x, y)


class PlayerAnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position, texture):
            super(PlayerAnimatedSprite, self).__init__()
            self.texture = texture

            images = []
            path_array = []
            for i in range(7):
                if i == 3:
                    path_array.append(Texture.getPikachuTexture(i, 0))
                    path_array.append(Texture.getPikachuTexture(i, 1))
                elif i == 4:
                    path_array.append(Texture.getPikachuTexture(i, 0))
                else:
                    for j in range(5):
                        path_array.append(Texture.getPikachuTexture(i, j))
            
            for _ in path_array:
                images.append(self.texture.getCroppedImage(_))

            self.images = images
            self.index = 0
            self.image = self.images[self.index]
            self.position = position
            self.scale = Scale(1, 1) 

    def update(self):
        self.index = (self.index + 1) % len(self.images);
        self.image = pygame.transform.flip(self.images[self.index], False, True if self.scale.x == -1 else 1)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        pygame.display.get_surface().blit(self.image, self.rect)

class SpriteWithAnchor(pygame.sprite.Sprite):

    def __init__(self, path, position, texture):
        self.position = position
        self.texture = texture
        self.image = self.texture.getCroppedImage(path) 
        self.scale = Scale(1, 1) 

    def update(self):
        self.image = pygame.transform.flip(self.image, False, True if self.scale.x == -1 else 1)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        pygame.display.get_surface().blit(self.image, self.rect)

class GameViewDrawer:
    
    def __init__(self, texture):
        self.texture = texture

        self.player1 = PlayerAnimatedSprite((0, 0), texture)
        self.player2 = PlayerAnimatedSprite((0, 0), texture)
        self.ball = BallAnimatedSprite((0, 0), texture)
        self.ballTrail = SpriteWithAnchor(self.texture.BALL_TRAIL, (0.5, 0.5), texture)
        self.ballHyper = SpriteWithAnchor(self.texture.BALL_HYPER, (0.5, 0.5), texture)
        self.punch = SpriteWithAnchor(self.texture.BALL_PUNCH, (0.5, 0.5), texture)
    
    def draw_players_and_ball(self, physics):
        player1 = physics.player1
        player2 = physics.player2
        ball = physics.ball

        self.player1.position = (player1.x, player1.y)
        print("player1:" + str(self.player1.position))

        if player1.state == 3 or player1.state == 4:
            self.player1.scale.x = -1 if player1.divingDirection == -1 else 1 
        else:
            self.player1.scale.x = 1

        self.player2.position = (player2.x, player2.y)
        print("player2:" + str(self.player2.position))

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

        self.ball.update()
        self.player1.update()
        self.player2.update()

        print(self.ball.position)

