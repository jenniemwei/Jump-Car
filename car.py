from cmu_graphics import *
from Platforms import *
from PIL import Image
import time


class Car:
    # static
    allCars = []
    length = 70
    height = 50

    def __init__(self, carX, carY, distance):
        self.distance = distance
        self.direction = True  # True=Right False=Left
        self.carX = carX
        self.carY = carY 
        self.dx = 6
        self.dy = 15
        self.ddy = -0.8
        self.shortJumpdy = 15
        self.shortJumpddy = -0.4

    def getCarInfo(self):
        return (self.carX, self.carY)

    def startJump(self):
        self.dy = 25
        self.shortJumpdy = 25

    def startFall(self):
        self.dy = 2

    def getDy(self):
        return self.dy

    def addDx(self, n):
        self.dx += n

    def subtractDx(self, n):
        self.dx -= n

    def getDx(self):
        return self.dx
    
    def getImage(self):
        return None

    def move(self):
        if self.direction:  # moving right
            if self.carX + Car.length <= self.distance:  # can still move right
                self.carX += self.dx  # moves right
            else:  # cant move right & turns
                self.direction = not self.direction
        else:  # moving left
            if self.carX - self.dx >= 0:  # can still move left
                self.carX -= self.dx  # moves left
            else:  # cant move left & turns
                self.direction = not self.direction

    @staticmethod
    def moveAllCars():
        for car in Car.allCars:
            if car != None:
                car.move()

    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5


class PlayerCar(Car):
    # static
    isFalling = False
    isJumping = False
    playerPlat = None
    isShortJump = False
    isShield=False
    #images
    Rightimage=Image.open('assets/PlayerCar2.png')
    Leftimage=Image.open('assets/PlayerCar2.png')
    Leftimage= Leftimage.transpose(Image.FLIP_LEFT_RIGHT)
    Leftimage=CMUImage(Leftimage)
    Rightimage= CMUImage(Rightimage)
    def getImage(self):
        if self.direction:
            return PlayerCar.Rightimage
        else:
            return PlayerCar.Leftimage
        
    def __init__(self, carX, carY, distance):
        super().__init__(carX, carY, distance)
        self.dx = 8

    def jump(self):
        self.carY -= self.dy
        if self.dy + self.ddy >= 0:
            self.dy += self.ddy

    def shortJump(self):
        if (
            PlayerCar.playerPlat.getPlatTop() - Car.height
        ) - self.carY <= 130:  # height cap for short jumps
            if self.direction: #increasing horizontal speed during jumps so it travels further(better UX)
                self.carX+=2
            else:
                self.carX-=2
            self.carY -= self.shortJumpdy
            if self.shortJumpdy + self.shortJumpddy >= 0:
                self.shortJumpdy += self.shortJumpddy

    def collision(self, other):
        leftX0, rightX0, topY0, bottomY0 = (
            self.carX,
            self.carX + Car.length,
            self.carY,
            self.carY + Car.height)  # Player location
        leftX1, rightX1, topY1, bottomY1 = (
            other.carX,
            other.carX + Car.length,
            other.carY,
            other.carY + Car.height)  # NPC location
        # collision from left/top
        if (leftX1 <= rightX0
            and rightX0 <= rightX1
            and bottomY0 >= topY1
            and topY0 <= bottomY1):
     
            return True
        # collision from right/top
        elif (leftX1 <= leftX0
            and leftX0 <= rightX1
            and bottomY0 >= topY1
            and topY0 <= bottomY1):
    
            return True
        return False
    # def

    def fall(self, landing):
        if self.carY - self.dy > landing - Car.height:
            self.carY = landing - Car.height
        else:
            self.carY -= self.dy
            self.dy += self.ddy

    def getPlayerY(self):
        return self.carY

    def getPlayerX(self):
        return self.carX

    def onPlatform(self, platformTop):
        if self.carY <= platformTop - (Car.height):  # higher than next platform top
            return True


class NormalCar(Car):  # slower than player, basic back and forth movement
    Rightimage=Image.open('assets/NormalCar.png')
    Leftimage=Image.open('assets/NormalCar.png')
    Leftimage=Leftimage.transpose(Image.FLIP_LEFT_RIGHT)
    Leftimage=CMUImage(Leftimage)
    Rightimage= CMUImage(Rightimage)
    
    def __init__(self, carX, carY, distance):
        super().__init__(carX, carY, distance)
        self.dx = 6

    def getImage(self):
        if self.direction:
            return NormalCar.Rightimage
        else:
            return NormalCar.Leftimage

class FastCar(Car):  # fastest car, basic back and forth movement
    Rightimage=Image.open('assets/FastCar2.png')
    Leftimage=Image.open('assets/FastCar2.png')
    Leftimage= Leftimage.transpose(Image.FLIP_LEFT_RIGHT)
    Leftimage=CMUImage(Leftimage)
    Rightimage= CMUImage(Rightimage)

    def __init__(self, carX, carY, distance):
        super().__init__(carX, carY, distance)
        self.dx = 9
    
    def getImage(self):
        if self.direction:
            return FastCar.Rightimage
        else:
            return FastCar.Leftimage


class SlowCar(Car):  # slowest car, basic back and forth movement
    Rightimage=Image.open('assets/SlowCar.png')
    Leftimage=Image.open('assets/SlowCar.png')
    Leftimage= Leftimage.transpose(Image.FLIP_LEFT_RIGHT)
    Leftimage=CMUImage(Leftimage)
    Rightimage= CMUImage(Rightimage)
    def __init__(self, carX, carY, distance):
        super().__init__(carX, carY, distance)
        self.dx = 2
    
    def getImage(self):
        if self.direction:
            return SlowCar.Rightimage
        else:
            return SlowCar.Leftimage


class ChasingCar(Car):  # changes direction to face player car
    Rightimage=Image.open('assets/ChasingCar.png')
    Leftimage=Image.open('assets/ChasingCar.png')
    Leftimage= Leftimage.transpose(Image.FLIP_LEFT_RIGHT)
    Leftimage=CMUImage(Leftimage)
    Rightimage= CMUImage(Rightimage)

    def __init__(self, carX, carY, distance, player):
        super().__init__(carX, carY, distance)
        self.dx = 6
        self.player = player

    def getImage(self):
        if self.direction:
            return ChasingCar.Rightimage
        else:
            return ChasingCar.Leftimage

    def move(self):
        # check if black car and player car on the same platform
        if self.carY == PlayerCar.playerPlat.getPlatTop() - Car.height:
            playerX = self.player.getPlayerX()
            if (
                not PlayerCar.isJumping
                and not PlayerCar.isFalling
                and not PlayerCar.isShortJump
            ):
                if (
                    self.direction and playerX < self.carX
                ):  # black car is going right, player car is left of it
                    self.direction = not self.direction
                if (
                    not self.direction and playerX > self.carX
                ):  # black car is going left, player car is right of it
                    self.direction = not self.direction
        if self.direction:  # moving right
            if (
                self.carX + self.length + self.dx <= self.distance
            ):  # can still move right
                self.carX += self.dx  # moves right
            else:  # cant move right & turns
                self.direction = not self.direction
        else:  # moving left
            if self.carX - self.dx >= 0:  # can still move left
                self.carX -= self.dx  # moves left
            else:  # cant move left & turns
                self.direction = not self.direction
