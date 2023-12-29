from cmu_graphics import *
from PIL import Image
class Platform:
    # static
    allPlatforms = []
    distBetweenPlats = 250
    platformCount = 0
    platTotal=100
    platLength=700
    platX=0


    landed=Image.open('assets/bluePlat.png')
    landed=CMUImage(landed)


    def __init__(self, height):  # platHeight measures from top of platform
        self.height = height
        self.width = 40
        normal=Image.open('assets/pinkPlat.png')
        self.color=CMUImage(normal)
        self.number = Platform.platformCount
        Platform.platformCount += 1

    def changeColor(self, image):
        self.color=image

    def getPlatInfo(self):
        return self.height, self.width, self.color, self.number

    def getPlatTop(self):
        return self.height

    def getPlatNum(self):
        return self.number

class ScrollingPlat(Platform):
    def __init__(self, height):
        super().__init__(height)
        scrolling=Image.open('assets/purplePlat.png')
        self.color=CMUImage(scrolling)
        self.scrollMargin=300
    def getMargin(self):
        return self.scrollMargin

class ShieldPlat(Platform):
    def __init__(self, height):
        super().__init__(height)
        shield=Image.open('assets/greenPlat.png')
        self.color=CMUImage(shield)
