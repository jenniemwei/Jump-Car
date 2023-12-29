from cmu_graphics import *
from PIL import Image

def setupAssets(app):
    setupBackground(app)
    setupOtherImages(app)

def setupBackground(app):
    app.gameBackground=Image.open('assets/Background.png')
    app.gameBackground=CMUImage(app.gameBackground)

def setupOtherImages(app):
    app.shieldImage=Image.open('assets/Shield.png')
    app.shieldImage=CMUImage(app.shieldImage)

    app.instrImage=Image.open('assets/Instructions.png')
    app.instrImage=CMUImage(app.instrImage)

    app.textBubble=Image.open('assets/textBubble.png')
    app.textBubble=CMUImage(app.textBubble)

    app.bigTextBox= Image.open('assets/bigTextBox.png')
    app.bigTextBox=CMUImage(app.bigTextBox)

    app.roundedTextBox= Image.open('assets/RoundedTextBox.png')
    app.roundedTextBox=CMUImage(app.roundedTextBox)