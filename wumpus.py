#!/usr/bin/python

from math import *
import random

dstrings = [
    "You feel a cold wind.",
    "You smell a terrible stench.",
    "You hear flapping noises.",
    "The following exits are available:",
    "North",
    "South",
    "West",
    "East",
    "Available actions:",
    "Shoot an arrow",
    "Will you (m)ove, (s)hoot, or e(x)it? ",
    "Direction? "
    ]

class Room(object):
    def __init__(self):
        self.haspit = False
        self.hasbat = False
        self.haswumpus = False
        self.randsetting()

    def randsetting(self):
        random.seed()
        x = random.randint(1,10000)
        if x % 20 == 0:
            self.haspit = True
        elif x % 15 == 0:
            self.hasbat = True

    def SetWump(self):
        self.haswumpus = True

class WumpusGame(object):
    xlen = 10
    ylen = 10
    xchar = 0
    ychar = 0
    xwump = 0
    ywump = 0
    arrowcount = 5
    playerdead = False
    wumpusdead = False


    gamegrid = [[]]

    def __init__(self):
        self.gamegrid = [[0 for x in range(self.xlen)] for x in range(self.ylen)]
        self.GenerateMaze()
        self.SetWumpus()
        self.GameLoop()

    def GenerateMaze(self):
        for lx in range(self.xlen):
            for ly in range(self.ylen):
                # print("row:", lx, ly)
                self.gamegrid[lx][ly] = Room()

    def ShootArrow(self, direction):
        print("Wumpus location:", self.xwump, self.ywump)
        print("Your location:", self.xchar, self.ychar)
        print("You unlimber your bow and shoot a crooked arrow in that direction.")
        if direction == "n" and self.xchar ==self.xwump and self.ychar > self.ywump:
            self.wumpusdead = True
        elif direction =="s" and  self.xchar == self.xwump and self.ychar < self.ywump:
            self.wumpusdead = True
        elif direction == "e" and self.ychar == self.ywump and self.xchar < self.xwump:
            self.wumpusdead = True
        elif direction == "w" and self.ychar == self.ywump and self.xchar > self.xwump:
            self.wumpusdead = True
        if self.wumpusdead == True:
            print("You hear a roar that turns into a scream, and a sickening ")
            print("wet crunch as your arrow finds its living heart.")

    def BatMoved(self):
        self.xchar = random.randint(0, self.xlen-1)
        self.ychar = random.randint(0, self.ylen-1)

    def SetWumpus(self):
        self.xwump = random.randint(0,self.xlen-1)
        self.ywump = random.randint(0, self.ylen-1)
        vwumproom = self.gamegrid[self.xwump][self.ywump]
        vwumproom.SetWump()
        # must prevent wumpus from being set at 0,0.
        print("Wumpus set at:", self.xwump, self.ywump)

    def GetAction(self):
        return raw_input( dstrings[10] )

    def GetDirection(self):
        return raw_input( dstrings[11] )

    def IsMoveValid(self, action, direction):
        isvalid = False
        if action == "m":

            if direction == "n":
                if self.ychar > 0:
                    isvalid = True
                else:
                    print("You have hit the north wall.")
            elif direction == "w":
                if self.xchar > 0:
                    isvalid = True
                else:
                    print("You have hit the west wall.")

            elif direction == "s":
                if self.ychar< (self.ylen-1):
                    isvalid = True
                else:
                    print("You have hit the south wall.")
            elif direction == "e":
                if self.xchar <  (self.xlen-1):
                    isvalid = True
                else:
                    print("You have hit the east wall.")

        elif action == "s":
            if self.arrowcount > 0:
                isvalid = True
            else:
                print("You are out of arrows")

        elif action == "x":
            isvalid = True

        return isvalid

    def DoMove(self, action, direction):

        if action == "m":

            if direction == "n":
                self.ychar = self.ychar -1
            elif direction == "s":
                self.ychar = self.ychar + 1
            elif direction == "w":
                self.xchar = self.xchar - 1
            elif direction == "e":
                self.xchar = self.xchar + 1

        elif action == "s":
            # iterate along the x / y axis of game grid and look
            # for the wumpus
            self.arrowcount = self.arrowcount - 1
            self.ShootArrow(direction)

        return False

    def SenseAdjacentRooms(self):
        #check for presence of wumpus, bat, and pit.
        adjrooms = []
        adjpit = False
        adjbat = False
        adjwump = False
        adjdesc = ""
        if self.xchar > 0:
            adjrooms.append (self.gamegrid[self.xchar-1][self.ychar])

        if self.xchar < self.xlen -1:
            adjrooms.append( self.gamegrid[self.xchar+1][self.ychar] )

        if self.ychar > 0:
            adjrooms.append (self.gamegrid[self.xchar][self.ychar-1] )

        if self.ychar < self.ylen-1:
            adjrooms.append( self.gamegrid[self.xchar][self.ychar+1] )
        for room in adjrooms:
            if room.haspit:
                adjpit = True
            if room.hasbat:
                adjbat = True
            if room.haswumpus:
                adjwump = True
        if adjwump:
            adjdesc = adjdesc + "You smell a horrible stench. It's close."
        if adjpit:
            adjdesc = adjdesc + "You feel a cold draft."
        if adjbat:
            adjdesc = adjdesc + "You hear a flapping sound."

        return adjdesc

    def GetRoomDescription(self):
        roomdesc = "You are in a cold, dark cave."
        roomdesc = roomdesc + self.SenseAdjacentRooms()
        return roomdesc

    def GameLoop(self):
        # start character at 0,0.
        # make sure 0,0 is safe.
        action = ""
        direction = ""
        currentroom = self.gamegrid[self.xchar][self.ychar]
        print self.GetRoomDescription()

        currentroom.hasbat = False
        currentroom.haspit = False
        while (self.wumpusdead==False and self.playerdead == False and action != "x"):

            if currentroom.hasbat:
                print "You see a flapping vampire bat!"
                print "The bat picks you up and carries you to another room."
                self.BatMoved()
                currentroom = self.gamegrid[self.xchar][self.ychar]
                print self.GetRoomDescription()
            elif currentroom.haspit:
                self.playerdead = True
                print "You fall into a bottomless pit!"
            elif currentroom.haswumpus:
                self.playerdead = True
                print "THE WUMPUS IS HERE. It tears off your arms and"
                print "legs!!!!!"
            else:

                # is the player dead?
                # is the wumpus dead?
                # show description of current location
                action = self.GetAction()
                # move to next room based on direction
                if action == "m":
                    direction = self.GetDirection()
                elif action == "s":
                    direction = self.GetDirection()

                if action != "x" and self.IsMoveValid(action, direction):
                    self.DoMove(action, direction)
                    if self.playerdead == False and self.wumpusdead == False:
                        print self.GetRoomDescription()
                        currentroom = self.gamegrid[self.xchar][self.ychar]

        if self.wumpusdead:
            print "You have killed the wumpus!"
        elif self.playerdead:
            print "You are dead!! Maggots eat your brain! RIP!!!"


# start loop
# describe room - check for wumpus in room. if wumpus, you are dead.
# find all adjacent rooms. add flapping, breeze, smell descriptors
# ask for a move
# get move
#

print "Wumpus implementation"
print "Written by Jeff Craton"

gm = WumpusGame()




