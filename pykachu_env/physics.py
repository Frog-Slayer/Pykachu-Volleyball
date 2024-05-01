import random as random

from .constants import (
    GROUND_WIDTH,
    GROUND_HALF_WIDTH,
    PLAYER_LENGTH,
    PLAYER_HALF_LENGTH,
    PLAYER_TOUCHING_GROUND_Y_COORD,
    BALL_RADIUS,
    BALL_TOUCHING_GROUND_Y_COORD,
    NET_PILLAR_HALF_WIDTH,
    NET_PILLAR_TOP_TOP_Y_COORD,
    NET_PILLAR_TOP_BOTTOM_Y_COORD,
    INFINITE_LOOP_LIMIT
)

class PykaPhysics:
    def __init__(self, is_player_2_computer):
        self.player1 = Player(is_player_2= False, is_computer= not is_player_2_computer)
        self.player2 = Player(is_player_2= True, is_computer= is_player_2_computer)
        self.ball = Ball(is_player_2_serve=False)
        return
    
    def run_engine(self, user_inputs):
        is_ball_touching_ground = physics_engine(self.player1, self.player2, self.ball, user_inputs)
        return is_ball_touching_ground

    def reset(self, is_player_2_serve = False):
        self.player1.init_new_round()
        self.player2.init_new_round()
        self.ball.init_new_round(is_player_2_serve)

class UserInput:
    def __init__(self, action = None):
        if action is None:
            self.x_direction = 0
            self.y_direction = 0
            self.power_hit = 0
        else : 
            self.x_direction = action[0] - 1 # down, noop, up
            self.y_direction = action[1] - 1 # down, noop, up
            self.power_hit   = action[2]
        return
    
class Player:
    def __init__(self, is_player_2, is_computer):
        self.is_player_2  = is_player_2
        self.is_computer = is_computer
        self.init_new_round()
        
        self.dive_direction        = 0
        self.lying_down_duration_left  = -1
        self.computer_stand_by_pos = 0
        
        #self.sound
        return
    
    def init_new_round(self):

        self.x = 3
        if (self.is_player_2):
            self.x = GROUND_WIDTH - 36
        
        self.y = PLAYER_TOUCHING_GROUND_Y_COORD
        self.y_velocity = 0
        self.is_ball_collision_happened = False
        
        """
        Player's state
        0: idle, 1: jumping, 2: jump and power hit, 3: diving, 4: lying down after diving
        """
        self.state = 0 
        self.frame_num = 0
        self.normal_status_arm_swing_direction  = 1
        self.next_frame_delay = 0
        
        self.computer_boldness = rand() % 5
        return
    
class Ball:
    def __init__(self, is_player_2_serve):
        self.init_new_round(is_player_2_serve)
        self.expected_landing_x = 0
        self.rotation       = 0
        self.fine_rotation   = 0
        self.punch_effect_x   = 0
        self.punch_effect_y   = 0

        # for ball trail
        self.previous_x      = 0
        self.pre_previous_x = 0
        self.previous_y      = 0
        self.pre_previous_y = 0
        
        #self.sound 
        return

    def init_new_round(self, is_player_2_serve):
        self.x = 56
        if (is_player_2_serve):
            self.x = GROUND_WIDTH - 56
        
        self.y = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.punch_effect_radius = 0
        self.is_power_hit = False    
        return

class CopyBall:
    def __init__(self, x, y, x_velocity, y_velocity):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

def rand():
    return int(32768 * random.random())

def physics_engine(player1, player2, ball, user_inputs):
    is_ball_touching_ground = process_ball_world_collision(ball)

    for i in range(2):
        if (i == 0):
            player = player1
            other = player2
        else:
            player = player2
            other = player1
    
        calculate_expected_landing_x(ball)
    
        process_player_movement(
            player,
            user_inputs[i],
            other,
            ball
        )
    
    for i in range(2):
        if (i == 0):
            player = player1
        else:
            player = player2
        
        is_happened = check_ball_player_collision(
            ball,
            player.x,
            player.y
        )
        
        if (is_happened):
            if (player.is_ball_collision_happened == False):
                process_ball_player_collision(
                    ball,
                    player.x,
                    user_inputs[i],
                    player.state
                )
            player.is_ball_collision_happened = True
        else:
            player.is_ball_collision_happened = False
                
    return is_ball_touching_ground
    

def check_ball_player_collision(ball, playerX, playerY):
    diff = ball.x - playerX
    if (abs(diff) <= PLAYER_HALF_LENGTH):
        diff = ball.y - playerY
        return abs(diff) <= PLAYER_HALF_LENGTH
        
    return False
        
def process_ball_world_collision(ball):
    ball.pre_previous_x = ball.previous_x
    ball.pre_previous_y = ball.previous_y
    ball.previous_x = ball.x
    ball.previous_y = ball.y
        
    future_fine_rotation = ball.fine_rotation + ball.x_velocity // 2

    if future_fine_rotation < 0:
        future_fine_rotation += 50
    elif future_fine_rotation > 50:
        future_fine_rotation -= 50
        
    ball.fine_rotation       = future_fine_rotation
    ball.rotation           = ball.fine_rotation // 10

    future_ball_x             = ball.x + ball.x_velocity
    if future_ball_x < BALL_RADIUS or future_ball_x > GROUND_WIDTH:
        ball.x_velocity      = -ball.x_velocity
        
    future_ball_y             = ball.y + ball.y_velocity
    if (future_ball_y < 0):
        ball.y_velocity      = 1
        
    if abs(ball.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and \
        ball.y > NET_PILLAR_TOP_TOP_Y_COORD:
        if ball.y <= NET_PILLAR_TOP_BOTTOM_Y_COORD:
            if ball.y_velocity > 0:
                ball.y_velocity = -ball.y_velocity
        else:
            if ball.x < GROUND_HALF_WIDTH:
                ball.x_velocity = -abs(ball.x_velocity)
            else:
                ball.x_velocity = abs(ball.x_velocity)
                    
                
    future_ball_y = ball.y + ball.y_velocity
    if future_ball_y > BALL_TOUCHING_GROUND_Y_COORD:
        #ball.sound.ballTouchesGround = True
        ball.y_velocity = -ball.y_velocity
        ball.punch_effect_x = ball.x
        ball.y = BALL_TOUCHING_GROUND_Y_COORD
        ball.punch_effect_radius = BALL_RADIUS
        ball.punch_effect_y = BALL_TOUCHING_GROUND_Y_COORD + BALL_RADIUS
        return True
    
    ball.y = future_ball_y
    ball.x = ball.x + ball.x_velocity
    ball.y_velocity += 1
    
    return False

def process_player_movement(player, user_input, other, ball):
    if (player.is_computer):
        let_computer_decide_user_input(player, ball, other, user_input)
    
    if (player.state == 4): #diving
        player.lying_down_duration_left += -1
        if (player.lying_down_duration_left < -1):
            player.state = 0
        return
    
    player_x_velocity = 0
    if (player.state < 5):
        if (player.state < 3):
            player_x_velocity = user_input.x_direction * 6
        else: # diving
            player_x_velocity = player.dive_direction * 8
            
    future_player_x = player.x + player_x_velocity
    player.x = future_player_x
    
    if (player.is_player_2 == False):
        if (future_player_x < PLAYER_HALF_LENGTH):
            player.x = PLAYER_HALF_LENGTH
        elif (future_player_x > GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH):
            player.x = GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH
    else:
        if (future_player_x < GROUND_HALF_WIDTH + PLAYER_HALF_LENGTH):
            player.x = GROUND_HALF_WIDTH + PLAYER_HALF_LENGTH
        elif (future_player_x > GROUND_WIDTH - PLAYER_HALF_LENGTH):
            player.x = GROUND_WIDTH - PLAYER_HALF_LENGTH
    
    if (player.state < 3 and user_input.y_direction == -1 and player.y == PLAYER_TOUCHING_GROUND_Y_COORD):
        player.y_velocity    = -16
        player.state        = 1
        player.frame_num  = 0
        #player.sound.chu   = True
        
    future_player_y   = player.y + player.y_velocity
    player.y        = future_player_y

    if (future_player_y < PLAYER_TOUCHING_GROUND_Y_COORD):
        player.y_velocity    += 1
    elif (future_player_y > PLAYER_TOUCHING_GROUND_Y_COORD):
        player.y_velocity    = 0
        player.y            = PLAYER_TOUCHING_GROUND_Y_COORD
        player.frame_num  = 0
        if (player.state == 3):
            player.state    = 4
            player.frame_num = 0
            player.lying_down_duration_left = 3
        else:
            player.state    = 0
            
    if (user_input.power_hit == 1):
        if (player.state == 1):
            player.next_frame_delay = 5
            player.frame_num  = 0
            player.state        = 2
            #player.sound.pika = True
        elif (player.state == 0 and user_input.x_direction != 0): # dive
            player.state        = 3
            player.frame_num  = 0
            player.dive_direction = user_input.x_direction
            player.y_velocity    = -5
            #player.sound.chu   = True
            
    if (player.state == 1):
        player.frame_num = (player.frame_num + 1) % 3
    elif (player.state == 2):
        if (player.next_frame_delay < 1):
            player.frame_num += 1
            if (player.frame_num > 4):
                player.frame_num = 0
                player.state = 1
        else:
            player.next_frame_delay -= 1
    elif (player.state == 0):
        player.next_frame_delay += 1
        if (player.next_frame_delay > 3):
            player.next_frame_delay = 0
            futureframe_num = player.frame_num + player.normal_status_arm_swing_direction
            if (futureframe_num < 0 or futureframe_num > 4):
                player.normal_status_arm_swing_direction = -player.normal_status_arm_swing_direction
            player.frame_num = player.frame_num + player.normal_status_arm_swing_direction
    
    return
        

def process_ball_player_collision(ball, playerX, user_input, playerState):
    if (ball.x < playerX):
        ball.x_velocity = -(abs(ball.x - playerX) // 3)
    elif (ball.x > playerX):
        ball.x_velocity = abs(ball.x - playerX) // 3
    
    if (ball.x_velocity == 0):
        ball.x_velocity = (rand() % 3) - 1
    
    ball_abs_yv = abs(ball.y_velocity)
    ball.y_velocity = -ball_abs_yv
    
    if (ball_abs_yv < 15):
        ball.y_velocity = -15
        
    if (playerState == 2):
        if (ball.x < GROUND_HALF_WIDTH):
            ball.x_velocity = (abs(user_input.x_direction) + 1) * 10
        else:
            ball.x_velocity = -(abs(user_input.x_direction) + 1) * 10
        
        ball.punch_effect_x = ball.x
        ball.punch_effect_y = ball.y
        
        ball.y_velocity = abs(ball.y_velocity) * user_input.y_direction * 2
        ball.punch_effect_radius  = BALL_RADIUS
        #ball.sound.power_hit    = True
        ball.is_power_hit         = True
    else:
        ball.is_power_hit         = False
        
    calculate_expected_landing_x(ball)
    return

def calculate_expected_landing_x(ball):
    copy_ball = CopyBall(ball.x, ball.y, ball.x_velocity, ball.y_velocity)
    
    loop_counter = 0
    while (True):
        loop_counter += 1
        future_copy_ball_x = copy_ball.x_velocity + copy_ball.x

        if future_copy_ball_x < BALL_RADIUS or future_copy_ball_x > GROUND_WIDTH:
            copy_ball.x_velocity = -copy_ball.x_velocity

        if copy_ball.y + copy_ball.y_velocity < 0:
            copy_ball.y_velocity = 1
        
        if abs(copy_ball.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and \
            copy_ball.y > NET_PILLAR_TOP_TOP_Y_COORD:
            if copy_ball.y < NET_PILLAR_TOP_BOTTOM_Y_COORD:
                if copy_ball.y_velocity > 0:
                    copy_ball.y_velocity = -copy_ball.y_velocity
            else:
                if copy_ball.x < GROUND_HALF_WIDTH:
                    copy_ball.x_velocity = -abs(copy_ball.x_velocity)
                else:
                    copy_ball.x_velocity = abs(copy_ball.x_velocity)
        
        copy_ball.y += copy_ball.y_velocity
        
        if (copy_ball.y > BALL_TOUCHING_GROUND_Y_COORD or \
            loop_counter >= INFINITE_LOOP_LIMIT):
            break
        
        copy_ball.x += copy_ball.x_velocity
        copy_ball.y_velocity += 1
    
    ball.expected_landing_x = copy_ball.x
    return

def let_computer_decide_user_input(player, ball, other, user_input):
    user_input.x_direction    = 0
    user_input.y_direction    = 0
    user_input.power_hit      = 0
    
    expected_landing_x = ball.expected_landing_x
    if (abs(ball.x - player.x) > 100 and \
        abs(ball.x_velocity) < player.computer_boldness + 5):

        left_boundary = (player.is_player_2) * GROUND_HALF_WIDTH      

        # computer wants to go to the middle of its side
        if ball.expected_landing_x <= left_boundary or\
            (ball.expected_landing_x >= player.is_player_2 * GROUND_WIDTH + GROUND_HALF_WIDTH and\
            player.computer_stand_by_pos == 0):
            expected_landing_x = left_boundary + GROUND_HALF_WIDTH // 2
    
    # set x direction
    if abs(expected_landing_x - player.x) > player.computer_boldness + 8:
        if (player.x < expected_landing_x):
            user_input.x_direction = 1
        else:
            user_input.x_direction = -1
    elif rand() % 20 == 0:
        player.computer_stand_by_pos = rand() % 2
        
    # if computer is on the ground
    if player.state == 0:
        if (abs(ball.x_velocity) < player.computer_boldness + 3   and\
            abs(ball.x - player.x) < PLAYER_HALF_LENGTH         and\
            ball.y > -36                                        and\
            ball.y < 10 * player.computer_boldness + 84          and\
            ball.y_velocity > 0):
            user_input.y_direction = -1
        
        left_boundary = player.is_player_2 * GROUND_HALF_WIDTH
        right_boundary = (player.is_player_2 + 1) * GROUND_HALF_WIDTH
        
        #dive
        if (ball.expected_landing_x > left_boundary                               and\
            ball.expected_landing_x < right_boundary                              and\
            abs(ball.x - player.x) > player.computer_boldness * 5 + PLAYER_LENGTH    and\
            ball.x > left_boundary                                                   and\
            ball.x < right_boundary                                                  and\
            ball.y > 174):
            user_input.power_hit  = 1
            if (player.x < ball.x):
                user_input.x_direction = 1
            else:
                user_input.x_direction = -1
    elif player.state == 1 or player.state == 2:# jumping
        if abs(ball.x - player.x) > 8:
            if player.x < ball.x:
                user_input.x_direction = 1
            else:
                user_input.x_direction = -1
        
        if abs(ball.x - player.x) < 48 and abs(ball.y - player.y) < 48:
            will_power_hit = decide_power_hit(player, ball, other, user_input)
            if will_power_hit:
                user_input.power_hit = 1
                if abs(other.x - player.x) < 80 and user_input.y_direction != -1:
                    user_input.y_direction = -1
    return                


def decide_power_hit(player, ball, other, user_input):
    if (rand() % 2 == 0):
        for x_direction in range(1, -1, -1):
            for y_direction in range(-1, 2):
                expected_landing_x = expected_power_hit_landing_x(x_direction, y_direction, ball)
                if ((expected_landing_x <= player.is_player_2 * GROUND_HALF_WIDTH or\
                    expected_landing_x >= player.is_player_2 * GROUND_WIDTH + GROUND_HALF_WIDTH) and\
                    abs(expected_landing_x - other.x) > PLAYER_LENGTH):
                    user_input.x_direction = x_direction
                    user_input.y_direction = y_direction
                    return True
    else:
        for x_direction in range(1, -1, -1):
            for y_direction in range(1, -2, -1):
                expected_landing_x = expected_power_hit_landing_x(x_direction, y_direction, ball)
                if ((expected_landing_x <= player.is_player_2 * GROUND_HALF_WIDTH or\
                    expected_landing_x >= player.is_player_2 * GROUND_WIDTH + GROUND_HALF_WIDTH) and\
                    abs(expected_landing_x - other.x) > PLAYER_LENGTH):
                    user_input.x_direction = x_direction
                    user_input.y_direction = y_direction
                    return True
    return False


def expected_power_hit_landing_x(user_inputx_direction, user_inputy_direction, ball):
    copy_ball = CopyBall(ball.x, ball.y, ball.x_velocity, ball.y_velocity)
    if (copy_ball.x < GROUND_HALF_WIDTH):
        copy_ball.x_velocity = (abs(user_inputx_direction) + 1) * 10
    else:
        copy_ball.x_velocity = -(abs(user_inputx_direction) + 1) * 10

    copy_ball.y_velocity = abs(copy_ball.y_velocity) * user_inputy_direction * 2
    
    loop_counter = 0
    while (True):
        loop_counter += 1
        future_copy_ball_x = copy_ball.x + copy_ball.x_velocity

        # side bounce
        if (future_copy_ball_x < BALL_RADIUS or future_copy_ball_x > GROUND_WIDTH):
            copy_ball.x_velocity = -copy_ball.x_velocity

        if (copy_ball.y + copy_ball.y_velocity < 0):
            copy_ball.y_velocity = 1

        if abs(copy_ball.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and\
            copy_ball.y > NET_PILLAR_TOP_TOP_Y_COORD:
            if copy_ball.y_velocity > 0:
                copy_ball.y_velocity = -copy_ball.y_velocity

        copy_ball.y += copy_ball.y_velocity

        if copy_ball.y > BALL_TOUCHING_GROUND_Y_COORD or\
            loop_counter >= INFINITE_LOOP_LIMIT:
            return copy_ball.x
        
        copy_ball.x = copy_ball.x + copy_ball.x_velocity
        copy_ball.y_velocity += 1