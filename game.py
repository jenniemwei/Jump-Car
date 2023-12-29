from car import *
from Platforms import *
from HighScore import *
from Assets import *
from PIL import Image
import random
import time


"""citations:
sidescrolling: https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html#sidescrollerExamples
gravity: bouncing balls demo
using PIL/images: images demo
fonts(found on https://www.dafont.com/):
'VCR OSD MONO' by Riciery Leal
'Superstar' by memesbruh03
'Minecraft' by Craftron Gaming
All Graphics: drawn by me (using Procreate + iPad)!

"""


def onAppStart(app):
    app.width = 700
    app.height = 1000
    reset(app)


def reset(app):
    app.isRecord=False
    app.username=''
    app.score=0
    app.gameOver = False
    app.showInstruction=True
    Platform.allPlatforms=[]
    Platform.platformCount=0
    Car.allCars=[]
    setupAssets(app)
    setupPlats(app)
    setupPlayer(app)
    setupCars(app)
    setupScrolling(app)
    setupSideScrolling(app) 
    keyPressSetup(app)
    shieldSetup(app)
    


def keyPressSetup(app):  # to distinguish keyPress vs keyHold
    app.keyPressStart = 0
    app.keyRelease = 50  # arbitrary default value that makes is short jump false
    app.stepCount = 0

def shieldSetup(app):
    app.shieldStepCount=0
    app.shieldCountdown=100


def setupPlats(app):
    for i in range(Platform.platTotal):  # create platform list
        if i==0: #first platform is normal
            Platform.allPlatforms.append(
                Platform(app.height - i * Platform.distBetweenPlats))
        else:
            platType = random.randint(1, 10)
            if platType ==10 and i <= 20:  # no more shields after 20 (increase difficulty)
                Platform.allPlatforms.append(
                    ShieldPlat(app.height - i * Platform.distBetweenPlats))
            elif platType==9:
                Platform.allPlatforms.append(
                    ScrollingPlat(app.height - i * Platform.distBetweenPlats))
            else:
                Platform.allPlatforms.append(
                    Platform(app.height - i * Platform.distBetweenPlats))
            
    Platform.allPlatforms[0].changeColor(Platform.landed)


def setupCars(app):
    carsInARow=0
    carsSoFar=0
    for i in range(len(Platform.allPlatforms)):  # create car list
        carY = Platform.allPlatforms[i].getPlatTop() - Car.height
        if carsSoFar==carsInARow:
            Car.allCars.append(None)
            carsInARow+=1
            carsSoFar=0
        else:
            carType = random.randint(1, 4)
            carStartX = random.randrange(0, Platform.platLength - Car.length, 20)
            if carType == 1:
                Car.allCars.append(NormalCar(carStartX, carY, Platform.platLength))
            elif carType == 2:
                Car.allCars.append(FastCar(carStartX, carY, Platform.platLength))
            elif carType == 3:
                Car.allCars.append(SlowCar(carStartX, carY, Platform.platLength))
            elif carType == 4:
                Car.allCars.append(
                    ChasingCar(carStartX, carY, Platform.platLength, app.player))
            carsSoFar+=1

def removeOldPlatsandCars(app):
    pass

# Scrolling
def setupScrolling(app):  # vertical game scrolling
    app.scrollY = 0
    app.topMargin = 300
    app.bottomMargin = 200


def setupSideScrolling(app):
    app.scrollX = 0
    app.scrollXMargin = 0
    app.platX = 0


def makePlayerVisible(app):
    #vertical
    if app.player.getPlayerY() < app.scrollY + app.topMargin:
        app.scrollY = app.player.getPlayerY() - app.topMargin
    if app.player.getPlayerY() > app.scrollY + app.height - app.bottomMargin:
        app.scrollY = app.player.getPlayerY() - app.height + app.bottomMargin

    #horizontal
    if app.player.getPlayerX() < app.scrollXMargin + app.scrollX: 
        app.scrollX = app.player.getPlayerX() - app.scrollXMargin

    if (
        app.player.getPlayerX() > app.width - app.scrollXMargin + app.scrollX
    ):  
        app.scrollX = app.player.getPlayerX() - app.width + app.scrollXMargin



def setupPlayer(app):
    PlayerCar.playerPlat = Platform.allPlatforms[0]
    startX, startY = 0, PlayerCar.playerPlat.getPlatTop() - Car.height
    app.player = PlayerCar(startX, startY, Platform.platLength)


def drawPlats(app):
    platX = Platform.platX
    platX -= app.scrollX
    for platform in Platform.allPlatforms:
        platHeight, platWidth, platColor, platNumber = platform.getPlatInfo()
        platHeight -= app.scrollY 
        drawImage(platColor, platX, platHeight)
        drawLabel(
            str(platNumber),
            app.width - 50,
            platHeight + (platWidth // 2),
            size=20,
            bold=True,
            fill="white",
            font='Minecraft')

def drawCars(app):
    for car in Car.allCars:
        if car != None:
            carX, carY= car.getCarInfo()
            carY -= app.scrollY 
            carX -= app.scrollX
            if car.getImage()!=None:
                carImage=car.getImage()
                drawImage(carImage, carX, carY)
 


def drawPlayer(app):
    carX, carY= app.player.getCarInfo()
    carY -= app.scrollY  # scroll
    carX -= app.scrollX  # side Scroll
    carImage=app.player.getImage()
    drawImage(carImage, carX, carY)
    
    #drawing Shield Elements
    if PlayerCar.isShield:
        drawImage(app.shieldImage, carX+(Car.length/2)+10,carY+(Car.height/2), align='center')
        drawImage(app.textBubble, 30, 30)
        drawLabel(app.shieldCountdown, 98, 98, size=40, fill='white', font='VCR OSD Mono')
        drawLabel('shield remaning:', 100, 30, size=20, fill='white', font='Superstar')

            


def onStep(app):
    if PlayerCar.isShortJump:
        app.stepCount += 1  # tracking steps while shortJumping
    if PlayerCar.isShield and not isinstance(PlayerCar.playerPlat,ShieldPlat): #shielding countdown begins once player leaves platform
        app.shieldStepCount+=1
        app.shieldCountdown-=1
    if not app.gameOver:
        Car.moveAllCars()
        scrollPlats(app)
        checkShield(app)
        checkCollisions(app)
        app.player.move()
        makePlayerVisible(app)
        playerActions(app)


def playerActions(app):
    scrollPlats(app)
    checkShortJump(app)
    landing = PlayerCar.playerPlat.getPlatTop()
    if (app.player.getPlayerY() >= landing - Car.height):  # player is on the platform, stop falling
        PlayerCar.isFalling = False
        if (PlayerCar.isJumping):  # long keyHold player does multiple platform jumps in a row
            app.player.startJump()
    if PlayerCar.isFalling:  # player is falling down to a platform(landing)
        app.player.fall(landing)
    if (PlayerCar.isShortJump):  # player is shortJumping(jump and land on the same platform)
        app.player.shortJump()
    if (PlayerCar.isJumping and not PlayerCar.isFalling):  # player can't initiate a new jump while in air falling
        app.player.jump()
    checkCollisions(app)


def scrollPlats(app):
    if isinstance(PlayerCar.playerPlat, ScrollingPlat):
        app.scrollXMargin = PlayerCar.playerPlat.getMargin()
    else:
        # creates a smooth transition back to normal platforms
        if app.scrollX < app.player.getDx() and app.scrollX > -(
            app.player.getDx()

    
        ):  # since car+=dx every step, scrollX doesn't precisely hit 0 every time so as long as the scroll is within one dx from the edge of app(0), scrollX returns back to 0
            app.scrollX = 0
            app.scrollXMargin = 0

def checkCollisions(app):
    otherCar = Car.allCars[PlayerCar.playerPlat.getPlatNum()]
    aboveCar = Car.allCars[PlayerCar.playerPlat.getPlatNum() + 1]
    if not PlayerCar.isShield:
        if otherCar != None and app.player.collision(otherCar):
            app.score=PlayerCar.playerPlat.getPlatNum()
            app.isRecord = checkHighScore(app.score)
            app.gameOver=True
        elif aboveCar != None and app.player.collision(aboveCar):
            app.score=PlayerCar.playerPlat.getPlatNum()
            app.isRecord = checkHighScore(app.score)
            app.gameOver=True


def checkShortJump(app):
    scrollPlats(app)
    if (app.keyRelease - app.keyPressStart < 0.2  # tracks if it's a short keyPress
        and app.keyRelease - app.keyPressStart > 0):
        PlayerCar.isShortJump = True
        app.keyRelease = 50  # arbitrary value so that isShortJump stays false
        app.keyPressStart = 0  # arbitrary value so that isShortJump stays false

    if app.stepCount >= 4:  # short jump stays in the air for 4 steps before falling(better UX)
        PlayerCar.isShortJump = False
        PlayerCar.isFalling = True
        app.player.startFall()
        app.stepCount = 0

def checkShield(app):
    if isinstance(app.player.playerPlat,ShieldPlat):
        PlayerCar.isShield=True
        shieldSetup(app)
    if app.shieldStepCount>=100: #shields for 100 steps
        PlayerCar.isShield=False
        shieldSetup(app)


def onKeyPress(app, key):
    if key == "space" and not PlayerCar.isFalling and not app.gameOver:
        app.keyPressStart = time.time()
        app.player.startJump()
    #get Username for highest score
    if app.gameOver and app.isRecord:        
        if key=='backspace':
            app.username=app.username[:-1]
        if key=='space':
            app.username+=' '
        if key.isalpha() and len(key)==1:
            app.username+=key
        if key=='enter' and app.isRecord:
            setHighScore(app.score, app.username)
            app.username='submitted!'
            app.isRecord=False
    #restart game
    if app.gameOver and key=='tab':
        reset(app)
    if key=='escape': #shortcut
        resetHighScore()


def onKeyHold(app, keys):
    if "space" in keys:
        PlayerCar.isJumping = True
        nextPlat = Platform.allPlatforms[PlayerCar.playerPlat.getPlatNum() + 1]
        if app.player.onPlatform(nextPlat.getPlatTop()):
            app.showInstruction=False
            PlayerCar.isFalling = True
            app.player.startFall()
            PlayerCar.playerPlat = nextPlat
            if not isinstance(nextPlat, ScrollingPlat) and not isinstance(nextPlat, ShieldPlat) :
                nextPlat.changeColor(Platform.landed)


def onKeyRelease(app, key):
    if key == "space":
        app.keyRelease = time.time()
        checkShortJump(app)
        if not PlayerCar.isFalling and not PlayerCar.isShortJump:
            app.player.startFall()
            PlayerCar.isFalling = True
    PlayerCar.isJumping = False


def drawScore(app):
    score=PlayerCar.playerPlat.getPlatNum()
    drawLabel(score, 350, 200, size=40, bold=True,fill='white', font='Minecraft')

def drawGameMessage(app):
    if app.gameOver:
        if app.isRecord:
            drawImage(app.bigTextBox, 350,380, align='center') 
            drawLabel('NEW HIGH SCORE !',350, 315, size=50, bold=True,fill='white', font='Minecraft')
            drawLabel(f'score: {app.score}', 350,380, size=60, fill='lightBlue', font='Superstar')
            drawLabel('NAME:', 245,440, size=25, fill='lightBlue', font='Minecraft')
            drawImage(app.roundedTextBox,390,440, align='center')
            drawLabel('press\'enter\'to submit', 350,490, size=20, fill='lightBlue', font='VCR OSD Mono')
            drawLabel(app.username,390,440, size=20,font='VCR OSD Mono')
            if app.username=='':
                drawLabel('start typing...',390,440, size=20, fill='grey', font='VCR OSD Mono')
    
        else:
            drawImage(app.bigTextBox, 350,380, align='center')   
            drawLabel('GAME OVER',350, 320, size=80, bold=True,fill='white', font='Minecraft')
            drawLabel(f'your score: {app.score}', 350,390, size=60, fill='lightBlue', font='Superstar')
            drawLabel(f'CURRENT HIGH SCORE:{getHighScore()}', 350,430, size=25, fill='lightBlue', font='VCR OSD Mono')
            drawLabel(f'HIGH SCORE PLAYER:{getHighScoreUser()}', 350,460, size=25, fill='lightBlue', font='VCR OSD Mono')
            drawLabel('press tab to play again', 350, 500, size=25, bold=True, fill='white', font='VCR OSD Mono')

    elif app.showInstruction:
        drawImage(app.instrImage, app.width//2,app.height//2-200, align='center')

    
def redrawAll(app):
    drawImage(app.gameBackground,0,0)
    user=getHighScoreUser()
    drawPlats(app)
    drawCars(app)
    drawPlayer(app)
    drawScore(app)
    drawGameMessage(app)


def main():
    runApp()


main()
