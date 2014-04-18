#!/usr/bin/env python

import sys
import random
import math

# Zone info
# width: 4000
# height: 1800
# 0,0 is top-left

class Point:
  def __init__(self, x, y):
    self._x = x
    self._y = y
  
  def set(self, x, y):
    self._x = x
    self._y = y
    
  def get(self):
    return (self._x, self._y)
  
  def __repr__(self):
    return "Point(%s,%s)" % (self._x, self._y)
  
  def __eq__(self, other):
    if isinstance(other, Point):
      if other._x == self._x and other._y == self._y:
        return True
      return False
    return NotImplemented
  
  def printClean(self):
    return "%s %s" % (self._x, self._y)

class Zone(Point):
  def __init__(self, x, y, controller):
    Point.__init__(self, x, y)
    self._controller = controller
    
  def updateController(self, newController):
    self._controller = newController
    
  def __repr__(self):
    return "Zone(ctrl: %s, %s, %s)" % (self._controller, self._x, self._y)

class Player:
  def __init__(self, playerId, numDrones):
    self._numDrones = numDrones
    self._id = playerId
    self._droneCoords = []
    self._requestedDroneCoords = []
    self.init()
  
  def dronesLoaded(self):
    if self._droneCoords[0] == Point(-1,-1):
      return False
    else:
      return True
    
  def init(self):
    # Default all drones to -1,-1
    self._droneCoords = [Point(-1,-1) for x in xrange(self._numDrones)]
    # Default all requested drone coords to -1,-1
    self._requestedDroneCoords = [Point(-1,-1) for x in xrange(self._numDrones)]

  def setDroneXY(self, x, y, droneId):
    self._droneCoords[droneId].set(x, y)

  def setRequestedDroneXY(self, point, droneId):
    if isinstance(point, Point):
      self._requestedDroneCoords[droneId].set(point._x, point._y)
      
  def getDroneList(self):
    return self._droneCoords
  
  def getRequestedDroneXYList(self):
    return self._requestedDroneCoords
  
  def __repr__(self):
    return "Player(%s) %s\n\tdrones: %s\n\trequested: %s" % (self._id, self._numDrones, self._droneCoords, self._requestedDroneCoords)

class AI:
  def __init__(self, numPlayers, numDronesPerPlayer, numZones, myPlayerId):
    self._numPlayers = numPlayers
    self._numDronesPerPlayer = numDronesPerPlayer
    self._numZones = numZones
    self._myPlayerId = myPlayerId
  
  def printNextMove(self, playerList, zoneList):
    # Calculate next move and update playerList::requestedDroneXYList
    self.divideEqually(playerList, zoneList)
        
    # Print next move
    for droneId in xrange(self._numDronesPerPlayer):
      print playerList[self._myPlayerId].getRequestedDroneXYList()[droneId].printClean()
    
  def divideEqually(self, playerList, zoneList):
    for droneId in xrange(self._numDronesPerPlayer):
      targetZone = zoneList[droneId % len(zoneList)]
      playerList[self._myPlayerId].setRequestedDroneXY(targetZone, droneId)

## Test drivers ##
# p1 = Point(0,1)
# p2 = Point(1,1)
# p3 = Point(0,1)
# print >> sys.stderr, "p1 == p2: %s" % (p1 == p2)
# print >> sys.stderr, "p1 == p3: %s" % (p1 == p3)
# sys.exit(0)

# testDrones = 10
# player = Player(0,testDrones)
# print >> sys.stderr, "dronesLoaded(): %s" % player.dronesLoaded()
# print >> sys.stderr, "Loading drones..."
# for drone in xrange(testDrones):
#   randX = random.randrange(100)
#   randY = random.randrange(100)
#   player.setDroneXY(randX, randY, drone)
# print >> sys.stderr, "dronesLoaded(): %s" % player.dronesLoaded()
# print >> sys.stderr, "Player: %s" % player
# sys.exit(0)
##################

zoneList = []

# Initialization
(numPlayers,myPlayerId,numDronesPerPlayer,numZones) = \
  map(int, raw_input().split())
for index in xrange(numZones):
  (zoneX, zoneY) = map(int, raw_input().split())
  zoneList.append(Zone(zoneX, zoneY, -1))

# Init player list with correct number of drones
playerList = [Player(x, numDronesPerPlayer) for x in xrange(numPlayers)]

ai = AI(numPlayers, numDronesPerPlayer, numZones, myPlayerId)

while 1:
  # Update controllers for each zone
  for index in xrange(numZones):
    zoneList[index].updateController(int(raw_input()))
    
  # Read all drone coords
  for playerId in xrange(numPlayers):
    for droneId in xrange(numDronesPerPlayer):
      (droneX, droneY) = map(int, raw_input().split())
      playerList[playerId].setDroneXY(droneX, droneY, droneId)
      
  print >> sys.stderr, "My Drones: %s" % playerList[myPlayerId]
  ai.printNextMove(playerList, zoneList)
  print >> sys.stderr, "My Drones: %s" % playerList[myPlayerId]
