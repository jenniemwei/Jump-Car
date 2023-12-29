from cmu_graphics import *
import os

def checkHighScore(currScore):
    if os.path.exists('highscore.txt'):
        if getHighScore()<currScore:
            return True
        else: return False
    resetHighScore()

def getHighScore():
    with open("highscore.txt","r") as highScore:
        data=highScore.read()
        score=int(data[:data.find(',')])
        return score

def getHighScoreUser():
     with open("highscore.txt","r") as highScore:
        data=highScore.read()
        user=data[data.find(',')+1:]
        return user

def setHighScore(newHigh, user):
    with open("highscore.txt",'w') as highScore:
        highScore.write(str(newHigh)+','+user)


def resetHighScore():
    with open('highscore.txt','w') as highScore:
        highScore.write('0,NoUser')