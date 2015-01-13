#! /usr/bin/env python

import sys
import pygame
import csv
import re
import signal
from enum import Enum

sys.path.insert(0,"../..")

# Python 3+ raw_input shim
if sys.version_info[0] >= 3:
  raw_input = input

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize pygame, fonts, etc.
pygame.init()
font = pygame.font.SysFont("monospace", 16)
screen = pygame.display.set_mode([400,240])

def clearScreen():
  screen.fill(WHITE)
  pygame.display.flip()

clearScreen()

def getNextArg(string):
  # Strip leading whitespace
  string = string.lstrip()

  # Find the first space
  spacePosition = string.find(' ')
  if (spacePosition < 0):
    return {'argument': string, 'remainingArgs': ''}

  # Return a tuple of argument and the remaining args
  return {'argument': string[:spacePosition], 'remainingArgs': string[spacePosition:].lstrip()}

def parseFile(inputPath):
  fileDesc = open(inputPath, 'r')
  for line in fileDesc:
    parsePrompt(line)

def parsePrompt(inputString):
  command = None
  commandType = None
  parsedArgs = []

  # Will probably mess up for ill formatted input but should be more performant
  # on large scripts than a regex search
  parsedString = getNextArg(inputString)
  command = parsedString['argument']

  parsedString = getNextArg(parsedString['remainingArgs'])
  subcommand = parsedString['argument']

  parsedCSVArgs = csv.reader([parsedString['remainingArgs']], skipinitialspace=True).next()

  process(command, subcommand, parsedCSVArgs)

def process(command, commandType, argList):
  if (command == 'draw'):
    if (commandType == 'pixel' and len(argList) == 3 ):
      x = int(argList[0])
      y = int(argList[1])
      color = bitToColor(int(argList[2]))
      drawPixel(x, y, color)
    elif( commandType == 'line' and len(argList) == 5):
      pygame.draw.line( screen, BLACK if int(argList[4]) > 0 else WHITE, (int(argList[0]), int(argList[1])), (int(argList[2]), int(argList[3])) )
    elif( commandType == 'rect' and len(argList) == 5):
      pygame.draw.rect( screen,BLACK if int(argList[4])> 0 else WHITE,(int(argList[0]),int(argList[1]), int(argList[2]), int(argList[3]) ),1 )
    elif( commandType == 'circle' and len(argList) == 4):
      pygame.draw.circle(screen,BLACK if int(argList[3])> 0 else WHITE, (int(argList[0]),int(argList[1])), int(argList[2]), 1)
    elif( commandType == 'bitmap' and len(argList) == 6):
      image = pygame.image.load(argList[2])
      image = pygame.transform.scale(image, (int(argList[3]), int(argList[4])))
      screen.blit(image, (int(argList[0]), int(argList[1])) )
    elif( commandType == 'text' and len(argList) == 4 ):
      x = int(argList[0])
      y = int(argList[1])
      text = argList[2]
      color = bitToColor(int(argList[3]))
      drawText(x, y, text, color)
  elif( command == 'fill' ):
    if( commandType == 'rect' and len(argList) == 5):
      pygame.draw.rect( screen,BLACK if int(argList[4])> 0 else WHITE,(int(argList[0]),int(argList[1]), int(argList[2]), int(argList[3]) ) )
    elif( commandType == 'circle' and len(argList) == 4):
      pygame.draw.circle(screen,BLACK if int(argList[3])> 0 else WHITE, (int(argList[0]),int(argList[1])), int(argList[2]))
    elif( commandType == 'screen' and len(argList) == 1):
      screen.fill(BLACK if int(argList[0])> 0 else WHITE)
  elif( command == 'set'):
    if( commandType == 'font' and len(argList) == 2):
      font = pygame.font.Font(argList[0],int(argList[1]))
  elif( command == 'run'):
    if( commandType == 'script' and len(argList) == 1):
      parseFile( argList[0] )
  elif( command == 'save'):
    if( commandType == 'image' and len(argList) == 1):
      pygame.image.save( screen, argList[0]+".png" )
  elif(command == 'clear'):
    clearScreen()
  elif( command == 'exit'):
    exit(0)

  pygame.display.flip()

def signal_handler(signal, frame):
  print "Exiting"
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Helper methods
def bitToColor(bit):
  # If statements in lieu of switch case in Python
  if (bit == 0):
    return WHITE
  elif (bit == 1):
    return BLACK
  else:
    return None

def colorToBit(color):
  if (color == BLACK):
    return 1
  elif (color == WHITE):
    return 0
  else:
    return None

# API Functions
def drawPixel(x, y, color):
  screen.set_at((x, y), color)

def drawText(x, y, text, color):
  global font
  renderedText = font.render(text, False, color)
  screen.blit(renderedText, (x, y))

# Event callback handlers

if len(sys.argv) == 2:
    parseFile(sys.argv[1])

while 1:
    try:
        s = raw_input('test > ')
    except EOFError:
        break
    if not s: continue
    parsePrompt(s)
