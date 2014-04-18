#!/usr/bin/env python

import sys

# Read init information from standard input, if any
class TronBoard:
  ''' Maintains a game board
      9 = Undefined square
      x = Square is consumed by player x 
      8 = wall '''
  def __init__(self, maxX = 30, maxY = 20):
    self._boardArray = []
    self._maxX = maxX
    self._maxY = maxY
    self._freeSpaceNum = 9
    self._wallSpaceNum = 8
    self._maxFloodCheck = 200
    self.initBoard()
      
  def setBoardElement(self, x, y, playerNumber):
    self._boardArray[y][x] = playerNumber
    
  def isBoardElementFree(self, x, y):
    try:
      return self._boardArray[y][x] == self._freeSpaceNum
    except:
      return False
    
  def initBoard(self):
    self._boardArray = [[self._freeSpaceNum for i in xrange(0,self._maxX)] for j in xrange(0,self._maxY)]
    # Add top walls
    for x in xrange(self._maxX):
      self.setBoardElement(x, 0, self._wallSpaceNum)
    # Add left walls
    for y in xrange(self._maxY):
      self.setBoardElement(0, y, self._wallSpaceNum)
    # Add right walls
    for y in xrange(self._maxY):
      self.setBoardElement(29, y, self._wallSpaceNum)
    # Add bot walls
    for x in xrange(self._maxX):
      self.setBoardElement(x, 19, self._wallSpaceNum)
    
  def printBoard(self):
    for x,row in enumerate(self._boardArray):
      print >> sys.stderr, "[%02d]: %s" % (x,row)
    print >> sys.stderr
    
  def removeAllBoardElementsForPlayer(self, playerNumber):
    for x in xrange(self._maxX):
      for y in xrange(self._maxY):
        if self._boardArray[y][x] == playerNumber:
          self.setBoardElement(x, y, self._freeSpaceNum)
          
  def reachableTiles(self, x, y):
    checkedAndOpen = set()
    checked = set()
    toCheck = set()
    # Add my current to the toCheck queue
    toCheck.add((x,y))
    while len(toCheck) > 0 and len(checkedAndOpen) < self._maxFloodCheck:
      checking = toCheck.pop()      
      checkedAndOpen.add(checking)
      currX = checking[0]
      currY = checking[1]
      
      if self.isBoardElementFree(currX, currY+1):
        if not (currX,currY+1) in checkedAndOpen and \
           not (currX,currY+1) in checked:
          toCheck.add((currX,currY+1))
      if self.isBoardElementFree(currX, currY-1):
        if not (currX, currY-1) in checkedAndOpen and \
           not (currX, currY-1) in checked:
          toCheck.add((currX, currY-1))
      if self.isBoardElementFree(currX+1, currY):
        if not (currX+1, currY) in checkedAndOpen and \
           not (currX+1, currY) in checked:
          toCheck.add((currX+1, currY))
      if self.isBoardElementFree(currX-1, currY):
        if not (currX-1, currY) in checkedAndOpen and \
           not (currX-1, currY) in checked:
          toCheck.add((currX-1, currY))
    return len(checkedAndOpen)

class TronAI:
  def __init__(self, myPlayerNumber):
    self._myPlayerNumber = myPlayerNumber
    self._tb = TronBoard()
    #self._tb.printBoard()
    self._currentX = 0
    self._currentY = 0
    self._lastRot = 0
    
  def updateBoard(self, x, y, playerNumber):
    self._tb.setBoardElement(x, y, playerNumber)
    if playerNumber == self._myPlayerNumber:
      self._currentX = x
      self._currentY = y

  def getNextMove(self):
    return self.getNextMoveBasedOnFloodFill()
      
  def getNextMoveBasedOnFloodFill(self):
    moveDict = {"RIGHT":0,
                "UP":0,
                "LEFT":0,
                "DOWN":0}
    
    # Can I go right?
    if self._tb.isBoardElementFree(self._currentX + 1, self._currentY):
      moveDict['RIGHT'] = self._tb.reachableTiles(self._currentX + 1, self._currentY)
    # Can I go up?
    if self._tb.isBoardElementFree(self._currentX, self._currentY - 1):
      moveDict['UP'] = self._tb.reachableTiles(self._currentX, self._currentY - 1)
    # Can I go left?
    if self._tb.isBoardElementFree(self._currentX - 1, self._currentY):
      moveDict['LEFT'] = self._tb.reachableTiles(self._currentX - 1, self._currentY)
    # Can I go down?
    if self._tb.isBoardElementFree(self._currentX, self._currentY + 1):
      moveDict['DOWN'] = self._tb.reachableTiles(self._currentX, self._currentY + 1)
    
    print >> sys.stderr, "moveDict: %s" % moveDict
    
    # Return the key for the largest value
    v=list(moveDict.values())
    k=list(moveDict.keys())
    return k[v.index(max(v))]

tai = None

while 1:
    # Read information from standard input
    #line = raw_input()
    (n,p) = map(int, raw_input().split())
    print >> sys.stderr, "n,p: %s,%s" % (n,p)
    if not tai:
      tai = TronAI(p)
    
    for index,line in enumerate(xrange(n)):
      (x0,y0,x1,y1) = map(int, raw_input().split())
      print >> sys.stderr, "[%s] x0,y0,x1,y1: %s,%s,%s,%s" % (index,x0,y0,x1,y1)
      # Determine if a player died
      if x0 == -1:
        print >> sys.stderr, "*** Removing player: %s from board" % index
        tai._tb.removeAllBoardElementsForPlayer(index)
      # Make sure we capture the starting index of others
      # in case we aren't player 0
      tai.updateBoard(x0, y0, index)
      tai.updateBoard(x1, y1, index)
    tai._tb.printBoard()

    print >> sys.stderr, "tai.getNextMove(): %s" % tai.getNextMove()
    print tai.getNextMove()
    
    