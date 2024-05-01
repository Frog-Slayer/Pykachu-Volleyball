import pygame
import json

ASSETS_PATH = 'pykachu_env/assets'
IMAGE_PATH = ASSETS_PATH + '/images'
SPRITE_JSON = IMAGE_PATH + '/sprite_sheet.json'
SPIRTE_IMG = IMAGE_PATH + '/sprite_sheet.png'
SOUND_PATH = ASSETS_PATH + '/sounds'

with open(SPRITE_JSON) as f:
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
            self.sheet= pygame.image.load(SPIRTE_IMG).convert_alpha()

        frame = sprite_json['frames'][path]['frame']
        rect = (frame['x'], frame['y'], frame['w'], frame['h']) 
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
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
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        pygame.display.get_surface().blit(self.image, self.rect)


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
        self.image = pygame.transform.flip(self.images[self.index], True if self.scale.x == -1 else False, False)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        pygame.display.get_surface().blit(self.image, self.rect)
    
    def set_frame_num(self, state, frame_num):
        if (state < 4) :
            self.index =  5 * state + frame_num
        elif state == 4:
            self.index = 17 + frame_num 
        else:
            self.index = 18 + 5 * (state - 5) + frame_num

class BackgroundSprite(pygame.sprite.Sprite):

    def __init__(self, texture):
            super(BackgroundSprite, self).__init__()
            self.texture = texture

            # Sky
            self.sky = self.texture.getCroppedImage(self.texture.SKY_BLUE)

            # Mountain
            self.mountain = self.texture.getCroppedImage(self.texture.MOUNTAIN)

            # Ground Red
            self.ground_red = self.texture.getCroppedImage(self.texture.GROUND_RED)

            # Ground Line
            self.ground_line = self.texture.getCroppedImage(self.texture.GROUND_LINE)
            self.ground_line_left = self.texture.getCroppedImage(self.texture.GROUND_LINE_LEFT_MOST)
            self.ground_line_right = self.texture.getCroppedImage(self.texture.GROUND_LINE_RIGHT_MOST)

            # Ground Yellow
            self.ground_yellow = self.texture.getCroppedImage(self.texture.GROUND_LINE) 

            # Net Pillar
            self.pillar_top = self.texture.getCroppedImage(self.texture.NET_PILLAR_TOP) 
            self.pillar = self.texture.getCroppedImage(self.texture.NET_PILLAR) 


    def update(self):
        self.draw_sky()
        self.draw_mountain()
        self.draw_ground()
        self.draw_pillar()
    
    def draw_sky(self):
        for j in range(12):
            for i in range(27):
                self.draw(self.sky, 16 * i ,16 * j)
    
    def draw_mountain(self):
        self.draw(self.mountain, 0, 188)

    def draw_ground(self):
        # ground red
        for i in range(27):
            self.draw(self.ground_red, 16 * i, 248)
       
        # ground line
        for i in range(26):
            self.draw(self.ground_line, 16 * i, 264)

        self.draw(self.ground_line_left, 0, 264)

        self.draw(self.ground_line_right, 432 - 16, 264)

        # ground yellow
        for j in range(2):
            for i in range(27):
                self.draw(self.ground_yellow, 16 *i, 280 + 16 * j)

    def draw_pillar(self): 
        self.draw(self.pillar_top, 213, 176)

        for i in range(12):
            self.draw(self.pillar, 213, 184 + 8 * i)

    def draw(self, surface, x, y):
        rect = surface.get_rect()
        rect.x, rect.y = x, y 
        pygame.display.get_surface().blit(surface, rect)

class SingleSprite(pygame.sprite.Sprite):

    def __init__(self, path, position, texture):
        self.position = position
        self.texture = texture
        self.image = self.texture.getCroppedImage(path) 

        w = self.image.get_rect().w
        h = self.image.get_rect().h
        self.scale = Scale(w, h) 
        self.visible = False

    def update(self):
        image = pygame.transform.scale(self.image, (self.scale.x, self.scale.y))
        rect = image.get_rect()
        rect.center = self.position
        pygame.display.get_surface().blit(image, rect)

class GameViewDrawer:
    
    def __init__(self, texture):
        self.texture = texture

        self.background = BackgroundSprite(texture)
        self.player1 = PlayerAnimatedSprite((0, 0), texture)
        self.player2 = PlayerAnimatedSprite((0, 0), texture)
        self.ball = BallAnimatedSprite((0, 0), texture)
        self.ball_trail = SingleSprite(self.texture.BALL_TRAIL, (0, 0), texture)
        self.ball_hyper = SingleSprite(self.texture.BALL_HYPER, (0, 0), texture)
        self.punch = SingleSprite(self.texture.BALL_PUNCH, (0, 0), texture)
    
    def draw_players_and_ball(self, physics):
        player1 = physics.player1
        player2 = physics.player2
        ball = physics.ball

        self.player1.position = (player1.x, player1.y)
        self.player1.set_frame_num(player1.state, player1.frame_num)

        if player1.state == 3 or player1.state == 4:
            self.player1.scale.x = -1 if player1.dive_direction == -1 else 1 
        else:
            self.player1.scale.x = 1

        self.player2.position = (player2.x, player2.y)
        self.player2.set_frame_num(player2.state, player2.frame_num)

        if player2.state == 3 or player2.state == 4:
            self.player2.scale.x = 1 if player2.dive_direction == 1 else -1 
        else:
            self.player2.scale.x = -1

        self.ball.position = (ball.x, ball.y)
        self.ball.index = ball.rotation

        if ball.punch_effect_radius > 0:
            ball.punch_effect_radius -= 2
            self.punch.scale = Scale(2 * ball.punch_effect_radius, 2 * ball.punch_effect_radius)
            self.punch.position = (ball.punch_effect_x, ball.punch_effect_y)
            self.punch.visible = True
        else:
            self.punch.visible = False
        
        if ball.is_power_hit:
            self.ball_hyper.position = (ball.previous_x, ball.previous_y)
            self.ball_trail.position = (ball.pre_previous_x, ball.pre_previous_y)
            
            self.ball_hyper.visible = True
            self.ball_trail.visible = True
        else:
            self.ball_hyper.visible = False
            self.ball_trail.visible = False

        self.player1.update()
        self.player2.update()

        if self.ball_trail.visible:
            self.ball_trail.update()
    
        if self.ball_hyper.visible:
            self.ball_hyper.update()
 
        self.ball.update()

        if self.punch.visible:
            self.punch.update()
 
    def draw_background(self):
        self.background.update()
