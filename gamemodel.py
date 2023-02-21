from math import sin,cos,radians
import random as rnd

#TODO: Deal with all TODOs in this file and also remove the TODO and HINT comments.

""" This is the model of the game"""
class Game:
    """ Create a game with a given size of cannon (length of sides) and projectiles (radius) """
    def __init__(self, cannonSize, ballSize):
        
        self.cannonSize = cannonSize
        self.ballSize = ballSize 

        player0 = Player(self, False, -90, 'blue')
        player1 = Player(self, True, 90, 'red')
        self.players = [player0, player1]
        self.turn = 0

        self.wind = 0#20 * rnd.random() - 10


    """ A list containing both players """
    def getPlayers(self):
        return self.players 

    """ The height/width of the cannon """
    def getCannonSize(self):
        return self.cannonSize

    """ The radius of cannon balls """
    def getBallSize(self):
        return self.ballSize


    """ The current player, i.e. the player whose turn it is """
    def getCurrentPlayer(self):
        return self.getPlayers()[self.turn] 

    """ The opponent of the current player """
    def getOtherPlayer(self):
        if self.turn == 0:
            return self.getPlayers()[1]
        else:
            return self.getPlayers()[0]
    
    """ The number (0 or 1) of the current player. This should be the position of the current player in getPlayers(). """
    def getCurrentPlayerNumber(self):
        return self.getPlayers().index(self.getCurrentPlayer()) #TODO: this is just a dummy value
    
    """ Switch active player """
    def nextPlayer(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0


    """ Set the current wind speed, only used for testing """
    def setCurrentWind(self, wind):
        self.wind = wind 
    
    def getCurrentWind(self):
        return self.wind 

    """ Start a new round with a random wind value (-10 to +10) """
    def newRound(self):
        
        self.wind = 20 * rnd.random() - 10

""" Models a player """
class Player:
    
    def __init__(self, game, isReversed, xPos, col):
        self.game = game
        self.isReversed = isReversed
        self.xPos = xPos
        self.yPos = self.game.getCannonSize()/2
        self.col = col
        self.Aim = (45, 40)
        self.Score = 0



    """ Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player. """
    def fire(self, angle, velocity):
        
        if self.isReversed:
            angle = 180-angle

        self.Aim = (angle, velocity)

        proj = Projectile(angle, velocity, Game.getCurrentWind(self.game), self.xPos, self.yPos, -110, 110)  # går ksk att göra direket i return? b
        return proj



    """ Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch (assuming the projectile is on the ground and factoring in both cannon and projectile size) this method should return 0"""
    def projectileDistance(self, proj):
        # HINT: both self (a Player) and proj (a Projectile) have getX()-methods.
        # HINT: This method should give a negative value if the projectile missed to the left and positive if it missed to the right.
        # The distance should be how far the projectile and cannon are from touching, not the distance between their centers.
        # You probably need to use getCannonSize and getBallSize from Game to compensate for the size of cannons/cannonballs
        playerXPos = self.getX()
        ballXPos = proj.getX()
        cannonSize = self.game.getCannonSize()
        ballSize = self.game.getBallSize()

        if (ballXPos + ballSize)-(playerXPos - cannonSize/2) < 0:
            distance = (ballXPos + ballSize) - (playerXPos - cannonSize/2)

        elif (ballXPos - ballSize)-(playerXPos + cannonSize/2) > 0:
            distance = (ballXPos - ballSize) - (playerXPos + cannonSize/2)

        else:
            distance = 0
        return distance

    """ The current score of this player """
    def getScore(self):
        return self.Score

    """ Increase the score of this player by 1."""
    def increaseScore(self):
        self.Score = self.Score + 1

    """ Returns the color of this player (a string)"""
    def getColor(self):
        return self.col 

    """ The x-position of the centre of this players cannon """
    def getX(self):
        return self.xPos 

    """ The angle and velocity of the last projectile this player fired, initially (45, 40) """
    def getAim(self):
        return self.Aim  



""" Models a projectile (a cannonball, but could be used more generally) """
class Projectile:
    """
        Constructor parameters:
        angle and velocity: the initial angle and velocity of the projectile 
            angle 0 means straight east (positive x-direction) and 90 straight up
        wind: The wind speed value affecting this projectile
        xPos and yPos: The initial position of this projectile
        xLower and xUpper: The lowest and highest x-positions allowed
    """
    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity*cos(theta)
        self.yvel = velocity*sin(theta)
        self.wind = wind


    """ 
        Advance time by a given number of seconds
        (typically, time is less than a second, 
         for large values the projectile may move erratically)
    """
    def update(self, time):
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8*time
        xvel1 = self.xvel + self.wind*time
        
        # Move based on the average velocity in the time period 
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0
        
        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)
        
        # Make sure xLower <= xPos <= mUpper   
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)
        
        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1
        
    """ A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits """
    def isMoving(self):
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    """ The current y-position (height) of the projectile". Should never be below 0. """
    def getY(self):
        return self.yPos
