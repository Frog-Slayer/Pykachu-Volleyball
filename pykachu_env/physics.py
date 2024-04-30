import random as random
import math

from constants import (
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

class PikaPhysics:
    def __init__(self, isPlayer1Computer, isPlayer2Computer):
        self.player1 = Player(isPlayer2= False, isComputer= isPlayer1Computer)
        self.player2 = Player(isPlayer2= True, isComputer= isPlayer2Computer)
        self.ball = Ball(False)
        return
    
    def runEngineForNextFrame(self, userInputArray):
        isBallTouchingGround = physicsEngine(self.player1, self.player2, self.ball, userInputArray)
        return isBallTouchingGround

    def reset(self, isPlayer2Serve = False):
        self.player1.initializeForNewRound()
        self.player2.initializeForNewRound()
        self.ball.initializeForNewRound(isPlayer2Serve)

class UserInput:
    def __init__(self, action = None):
        if action is None:
            self.xDirection = 0
            self.yDirection = 0
            self.powerHit = 0
        else : 
            self.yDirection = action[0]
            self.xDirection = action[1]
            self.powerHit   = action[2]
        return
    
class Player:
    def __init__(self, isPlayer2, isComputer):
        self.isPlayer2  = isPlayer2
        self.isComputer = isComputer
        self.initializeForNewRound()
        
        self.divingDirection        = 0
        self.lyingDownDurationLeft  = -1
        self.isWingger              = False
        self.gameEnded              = False
        self.computerWhereToStandBy = 0
        
        #self.sound
        return
    
    def initializeForNewRound(self):

        self.x = 3
        if (self.isPlayer2):
            self.x = GROUND_WIDTH - 36
        
        self.y = PLAYER_TOUCHING_GROUND_Y_COORD
        self.yVelocity = 0
        self.isCollisionWithBallHappened = False
        
        self.state = 0 
        self.frameNumber = 0
        self.normalStatusArmSwingDirection  = 1
        self.delayBeforeNextFrame = 0
        
        self.computerBoldness = rand() % 5
        return
    
class Ball:
    def __init__(self, isPlayer2Serve):
        self.initializeForNewRound(isPlayer2Serve)
        self.expectedLandingPointX = 0
        self.rotation       = 0
        self.fineRotation   = 0
        self.punchEffectX   = 0
        self.punchEffectY   = 0

        # for ball trail
        self.previousX      = 0
        self.previousPreviousX = 0
        self.previousY      = 0
        self.previousPreviousY = 0
        
        #self.sound 
        return

    def initializeForNewRound(self, isPlayer2Serve):
        self.x = 56
        if (isPlayer2Serve):
            self.x = GROUND_WIDTH - 56
        
        self.y = 0
        self.xVelocity = 0
        self.yVelocity = 0
        self.punchEffectRadius = 0
        self.isPowerHit = False    
        return

class CopyBall:
    def __init__(self, x, y, xVelocity, yVelocity):
        self.x = x
        self.y = y
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity

def rand():
    return math.floor(32768 * random.random())

def physicsEngine(player1, player2, ball, userInputArray):
    isBallTouchingGround = processCollisionBetweenBallAndWorldAndSetBallPosition(ball)

    for i in range(2):
        if (i == 0):
            player = player1
            theOtherPlayer = player2
        else:
            player = player2
            theOtherPlayer = player1
    
        calculateExpectedLandingPointXFor(ball)
    
        processPlayerMovementAndSetPlayerPosition(
            player,
            userInputArray[i],
            theOtherPlayer,
            ball
        )
        
    
    for i in range(2):
        if (i == 0):
            player = player1
        else:
            player = player2
        
        isHappened = isCollisionBetweenBallAndPlayerHappened(
            ball,
            player.x,
            player.y
        )
        
        if (isHappened):
            if (player.isCollisionWithBallHappened == False):
                processCollisionBetweenBallAndPlayer(
                    ball,
                    player.x,
                    userInputArray[i],
                    player.state
                )
            player.isCollisionWithBallHappened = True
            print("collision")
        else:
            player.isCollisionWithBallHappened = False
                
    return isBallTouchingGround
    

def isCollisionBetweenBallAndPlayerHappened(ball, playerX, playerY):
    diff = ball.x - playerX
    if (abs(diff) <= PLAYER_HALF_LENGTH):
        diff = ball.y - playerY
        if (abs(diff) <= PLAYER_HALF_LENGTH):
            return True
        
    return False
        
def processCollisionBetweenBallAndWorldAndSetBallPosition(ball):
    ball.previousPreviousX  = ball.previousX
    ball.previousPreviousY  = ball.previousY
    ball.previousX          = ball.x
    ball.previousY          = ball.y
        
    futureFineRotation = ball.fineRotation + int(ball.xVelocity / 2)

    if (futureFineRotation < 0):
        futureFineRotation += 50
    elif (futureFineRotation > 50):
        futureFineRotation -= 50
        
    ball.fineRotation       = futureFineRotation
    ball.rotation           = int(ball.fineRotation / 10)

    futureBallX             = ball.x + ball.xVelocity
    if (futureBallX < BALL_RADIUS or futureBallX > GROUND_WIDTH):
        ball.xVelocity      = -ball.xVelocity
        
    futureBallY             = ball.y + ball.yVelocity
    if (futureBallY < 0):
        ball.yVelocity      = 1
        
    if (abs(ball.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and \
        ball.y > NET_PILLAR_TOP_TOP_Y_COORD):
        if (ball.y <= NET_PILLAR_TOP_BOTTOM_Y_COORD):
            if (ball.yVelocity > 0):
                ball.yVelocity = -ball.yVelocity
        else:
            if (ball.x < GROUND_HALF_WIDTH):
                ball.xVelocity = -abs(ball.xVelocity)
            else:
                ball.xVelocity = abs(ball.xVelocity)
                    
                
    futureBallY = ball.y + ball.yVelocity
    if (futureBallY > BALL_TOUCHING_GROUND_Y_COORD):
        #ball.sound.ballTouchesGround    = True
        ball.yVelocity                  = -ball.yVelocity
        ball.punchEffectX               = ball.x
        ball.y                          = BALL_TOUCHING_GROUND_Y_COORD
        ball.punchEffectRadius          = BALL_RADIUS
        ball.punchEffectY               = BALL_TOUCHING_GROUND_Y_COORD + BALL_RADIUS
        return True
    
    ball.y          = futureBallY
    ball.x          = ball.x + ball.xVelocity
    ball.yVelocity  += 1
    
    return False

def processPlayerMovementAndSetPlayerPosition(player, userInput, theOtherPlayer, ball):
    if (player.isComputer):
        letComputerDecideUserInput(player, ball, theOtherPlayer, userInput)
    
    if (player.state == 4):
        player.lyingDownDurationLeft += -1
        if (player.lyingDownDurationLeft < -1):
            player.state = 0
        return
    
    playerVelocityX = 0
    if (player.state < 5):
        if (player.state < 3):
            playerVelocityX = userInput.xDirection * 6
        else:
            playerVelocityX = player.divingDirection * 8
            
    futurePlayerX = player.x + playerVelocityX
    player.x = futurePlayerX
    
    if (player.isPlayer2 == False):
        if (futurePlayerX < PLAYER_HALF_LENGTH):
            player.x = PLAYER_HALF_LENGTH
        elif (futurePlayerX > GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH):
            player.x = GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH
    else:
        if (futurePlayerX < GROUND_HALF_WIDTH + PLAYER_HALF_LENGTH):
            player.x = GROUND_HALF_WIDTH + PLAYER_HALF_LENGTH
        elif (futurePlayerX > GROUND_HALF_WIDTH - PLAYER_HALF_LENGTH):
            player.x = GROUND_WIDTH - PLAYER_HALF_LENGTH
    
    if (player.state < 3 and userInput.yDirection == -1 and player.y == PLAYER_TOUCHING_GROUND_Y_COORD):
        player.yVelocity    = -16
        player.state        = 1
        player.frameNumber  = 0
        #player.sound.chu   = True
        
    futurePlayerY   = player.y + player.yVelocity
    player.y        = futurePlayerY
    if (futurePlayerY < PLAYER_TOUCHING_GROUND_Y_COORD):
        player.yVelocity    += 1
    elif (futurePlayerY > PLAYER_TOUCHING_GROUND_Y_COORD):
        player.yVelocity    = 0
        player.y            = PLAYER_TOUCHING_GROUND_Y_COORD
        player.frameNumber  = 0
        if (player.state == 3):
            player.state    = 4
            player.frameNuber = 0
            player.lyingDownDurationLeft = 3
        else:
            player.state    = 0
            
    if (userInput.powerHit == 1):
        if (player.state == 1):
            player.delayBeforeNextFrame = 5
            player.frameNumber  = 0
            player.state        = 2
            #player.sound.pika = True
        elif (player.state == 0 and userInput.xDirection != 0):
            player.state        = 3
            player.frameNumber  = 0
            player.divingDirection = userInput.xDirection
            player.yVelocity    = -5
            #player.sound.chu   = True
            
    if (player.state == 1):
        player.frameNumber = (player.frameNumber + 1) % 3
    elif (player.state == 2):
        if (player.delayBeforeNextFrame < 1):
            player.frameNumber += 1
            if (player.frameNumber > 4):
                player.frameNumber = 0
                player.state = 1
        else:
            player.delayBeforeNextFrame -= 1
    elif (player.state == 0):
        player.delayBeforeNextFrame += 1
        if (player.delayBeforeNextFrame > 3):
            player.delayBeforeNextFrame = 0
            futureFrameNumber = player.frameNumber + player.normalStatusArmSwingDirection
            if (futureFrameNumber < 0 or futureFrameNumber > 4):
                player.normalStatusArmSwingDirection = -player.normalStatusArmSwingDirection
            player.frameNumber = player.frameNumber + player.normalStatusArmSwingDirection
    
    if (player.gameEnded == True):
        if (player.state == 0):
            if (player.isWinner == True):
                player.state = 5
                #player.sound.pipikachu = True
            else:
                player.state = 6
            player.delayBeforeNExtFrame = 0
            player.frameNumber = 0
        processGameEndFrameFor(player)    
    return
        
def processGameEndFrameFor(player):
    if (player.gameEnded == True and player.frameNumber < 4):
        player.delayBeforeNextFrame += 1
        if (player.delayBeforeNextFrame > 4):
            player.delayBeforeNextFrame = 0
            player.frameNumber += 1  
    return


def processCollisionBetweenBallAndPlayer(ball, playerX, userInput, playerState):
    if (ball.x < playerX):
        ball.xVelocity = -int(abs(ball.x - playerX) / 3)
    elif (ball.x > playerX):
        ball.xVelocity = int(abs(ball.x - playerX) / 3)
    
    if (ball.xVelocity == 0):
        ball.xVelocity = (rand() % 3) - 1
    
    ballAbsYVelocity = abs(ball.yVelocity)
    ball.yVelocity = -ballAbsYVelocity
    
    if (ballAbsYVelocity < 15):
        ball.yVelocity = -15
        
    if (playerState == 2):
        if (ball.x < GROUND_HALF_WIDTH):
            ball.xVelocity = (abs(userInput.xDirection) + 1) * 10
        else:
            ball.xVelocity = -(abs(userInput.xDirection) + 1) * 10
        
        ball.punchEffectX = ball.x
        ball.punchEffectY = ball.y
        
        ball.yVelocity = abs(ball.yVelocity) * userInput.yDirection * 2
        ball.punchEffectRadius  = BALL_RADIUS
        #ball.sound.powerHit    = True
        ball.isPowerHit         = True
    else:
        ball.isPowerHit         = False
        
    calculateExpectedLandingPointXFor(ball)
    return

def calculateExpectedLandingPointXFor(ball):
    copyBall = CopyBall(ball.x, ball.y, ball.xVelocity, ball.yVelocity)
    
    loopCounter = 0
    while (True):
        loopCounter += 1
        
        futureCopyBallX = copyBall.xVelocity + copyBall.x
        if (futureCopyBallX < BALL_RADIUS or futureCopyBallX > GROUND_WIDTH):
            copyBall.xVelocity = -copyBall.xVelocity
        if (copyBall.y + copyBall.yVelocity < 0):
            copyBall.yVelocity = 1
        
        if (abs(copyBall.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and \
            copyBall.y > NET_PILLAR_TOP_TOP_Y_COORD):
            if (copyBall.y < NET_PILLAR_TOP_BOTTOM_Y_COORD):
                if (copyBall.yVelocity > 0):
                    copyBall.yVelocity = -copyBall.yVelocity
            else:
                if (copyBall.x < GROUND_HALF_WIDTH):
                    copyBall.xVelocity = -abs(copyBall.xVelocity)
                else:
                    copyBall.xVelocity = abs(copyBall.xVelocity)
        
        copyBall.y = copyBall.y + copyBall.yVelocity
        
        if (copyBall.y > BALL_TOUCHING_GROUND_Y_COORD or \
            loopCounter >= INFINITE_LOOP_LIMIT):
            break
        
        copyBall.x = copyBall.x = copyBall.xVelocity
        copyBall.yVelocity += 1
    
    ball.expectedLandingPointX = copyBall.x
    return

def letComputerDecideUserInput(player, ball, theOtherPlayer, userInput):
    userInput.xDirection    = 0
    userInput.yDirection    = 0
    userInput.powerHit      = 0
    
    virtualExpectedLandingPointX    = ball.expectedLandingPointX
    if (abs(ball.x - player.x) > 100 and \
        abs(ball.xVelocity) < player.computerBoldness + 5):

        leftBoundary    =   (player.isPlayer2) * GROUND_HALF_WIDTH      

        if (ball.expectedLandingPointX <= leftBoundary or\
            (ball.expectedLandingPointX >= (player.isPlayer2) * GROUND_WIDTH + GROUND_HALF_WIDTH and\
            player.computerWhereToStandBy == 0)
            ):
            virtualExpectedLandingPointX = leftBoundary + int(GROUND_HALF_WIDTH / 2)
    
    if (abs(virtualExpectedLandingPointX - player.x) > player.computerBoldness + 8):
        if (player.x < virtualExpectedLandingPointX):
            userInput.xDirection = 1
        else:
            userInput.xDirection = -1
    elif (rand() % 20 == 0):
        player.computerWhereToStandBy = rand() % 2
        
    if (player.state == 0):
        if (abs(ball.xVelocity) < player.computerBoldness + 3   and\
            abs(ball.x - player.x) < PLAYER_HALF_LENGTH         and\
            ball.y > -36                                        and\
            ball.y < 10 * player.computerBoldness + 84          and\
            ball.yVelocity > 0            
            ):
            userInput.yDirection = -1
        
        leftBoundary = player.isPlayer2 * GROUND_HALF_WIDTH
        rightBoundary = (player.isPlayer2 + 1) * GROUND_HALF_WIDTH
        
        if (ball.expectedLandingPointX > leftBoundary                               and\
            ball.expectedLandingPointX < rightBoundary                              and\
            abs(ball.x - player.x) > player.computerBoldness * 5 + PLAYER_LENGTH    and\
            ball.x > leftBoundary                                                   and\
            ball.y < rightBoundary                                                  and\
            ball.y > 174
            ):
            userInput.powerHit  = 1
            if (player.x < ball.x):
                userInput.xDirection = 1
            else:
                userInput.xDirection = -1
    elif (player.state == 1 or player.state == 2):
        if (abs(ball.x - player.x) > 8):
            userInput.xDirection = 1
        else:
            userInput.xDirection = -1
        
        if (abs(ball.x - player.x) < 48 and abs(ball.y - player.y) < 48):
            willInputPowerHit = decideWhetherInputPowerHit(player, ball, theOtherPlayer, userInput)
            if (willInputPowerHit):
                userInput.powerHit = 1
                if (abs(theOtherPlayer.x - player.x) < 80           and\
                    userInput.yDirection != -1):
                    userInput.yDirection = -1
    return                


def decideWhetherInputPowerHit(player, ball, theOtherPlayer, userInput):
    if (rand() % 2 == 0):
        for xDirection in range(1, -1):
            for yDirection in range(-1, 2):
                expectedLandingPointX = expectedLandingPointXWhenPowerHit(xDirection, yDirection, ball)
                if ((expectedLandingPointX <= player.isPlayer2 * GROUND_HALF_WIDTH or\
                    expectedLandingPointX >= player.isPlayer2 * GROUND_WIDTH + GROUND_HALF_WIDTH) and\
                    abs(expectedLandingPointX - theOtherPlayer.x) > PLAYER_LENGTH   
                ):
                    userInput.xDirection = xDirection
                    userInput.yDIrection = yDirection
                    return True
    else:
        for xDirection in range(1, -1):
            for yDirection in range(1, -2):
                expectedLandingPointX = expectedLandingPointXWhenPowerHit(xDirection, yDirection, ball)
                if ((expectedLandingPointX <= player.isPlayer2 * GROUND_HALF_WIDTH or\
                    expectedLandingPointX >= player.isPlayer2 * GROUND_WIDTH + GROUND_HALF_WIDTH) and\
                    abs(expectedLandingPointX - theOtherPlayer.x) > PLAYER_LENGTH   
                ):
                    userInput.xDirection = xDirection
                    userInput.yDIrection = yDirection
                    return True
    return False


def expectedLandingPointXWhenPowerHit(userInputXDirection, userInputYDirection, ball):
    copyBall = CopyBall(ball.x, ball.y, ball.xVelocity, ball.yVelocity)
    if (copyBall.x < GROUND_HALF_WIDTH):
        copyBall.xVelocity = abs(userInputXDirection + 1) * 10
    else:
        copyBall.xVelocity = -abs(userInputXDirection + 1) * 10

    copyBall.yVelocity = abs(copyBall.yVelocity) * userInputYDirection * 2
    
    loopCounter = 0
    while (True):
        loopCounter += 1
        
        futureCopyBallX = copyBall.x + copyBall.xVelocity
        if (futureCopyBallX < BALL_RADIUS or futureCopyBallX > GROUND_WIDTH):
            copyBall.xVelocity = -copyBall.xVelocity
        if (copyBall.y + copyBall.yVelocity < 0):
            copyBall.yVelocity = 1
        if (abs(copyBall.x - GROUND_HALF_WIDTH) < NET_PILLAR_HALF_WIDTH and\
            copyBall.y > NET_PILLAR_TOP_TOP_Y_COORD
            ):
            if (copyBall.yVelocity > 0):
                copyBall.yVelocity = -copyBall.yVelocity
        copyBall.y = copyBall.y + copyBall.yVelocity
        if (
            copyBall.y > BALL_TOUCHING_GROUND_Y_COORD or\
            loopCounter >= INFINITE_LOOP_LIMIT
        ):
            return copyBall.x
        
        copyBall.x = copyBall.x + copyBall.xVelocity
        copyBall.yVelocity += 1