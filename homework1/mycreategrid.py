'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *


# Creates a grid as a 2D array of True/False values (True = traversable). Also returns the dimensions of the grid as a (columns, rows) list.
def myCreateGrid(world, cellsize):
    grid = None
    dimensions = (0, 0)
    ### YOUR CODE GOES BELOW HERE ###

    # get dimensions
    dim = world.getDimensions()
    dimensions = (int(math.floor(dim[0]/cellsize)),int(math.floor(dim[1]/cellsize)))

    # first set all grid to be True
    grid = [[True for x in range(dimensions[1])] for y in range(dimensions[0])]

    # get information of obstacles
    obstacles = world.getObstacles()
    obstacles_corners = []
    obstacles_lines = []

    # store points' coordinates into obstacles_corners
    for i in obstacles:
        obstacles_corners.append(i.getPoints())


    # store all lines of obstacles into obstacles_lines
    for i in obstacles:
        obstacles_lines.append(i.getLines())


    # check 4 corners of each cell in the obstacles or not
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            for corners in obstacles_corners:
                if pointInsidePolygonPoints((i*cellsize,j*cellsize), corners) == True:
                    grid[i][j] = False
                elif pointInsidePolygonPoints(((i+1)*cellsize,j*cellsize), corners) == True:
                    grid[i][j] = False
                elif pointInsidePolygonPoints((i*cellsize,(j+1)*cellsize), corners) == True:
                    grid[i][j] = False
                elif pointInsidePolygonPoints(((i+1)*cellsize,(j+1)*cellsize), corners) == True:
                    grid[i][j] = False

    # check 4 lines of each cell intersected with obstacles or not
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            for lines in obstacles_lines:
                if rayTraceWorld((i*cellsize,j*cellsize),((i+1)*cellsize,j*cellsize),lines) != None:
                    grid[i][j] = False
                if rayTraceWorld((i*cellsize,j*cellsize),(i*cellsize,(j+1)*cellsize),lines) != None:
                    grid[i][j] = False
                if rayTraceWorld(((i+1)*cellsize,j*cellsize),((i+1)*cellsize,(j+1)*cellsize),lines) != None:
                    grid[i][j] = False
                if rayTraceWorld((i*cellsize,(j+1)*cellsize),((i+1)*cellsize,(j+1)*cellsize),lines) != None:
                    grid[i][j] = False

    # check all the corners of obstacles not in any cell
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            x1 = i*cellsize
            y1 = j*cellsize
            x2 = (i+1)*cellsize
            y2 = (j+1)*cellsize
            grid_corners = [(x1,y1),(x1,y2),(x2,y1),(x2,y2)]
            for corners in obstacles_corners:
                for points in corners:
                    if pointInsidePolygonPoints(points, grid_corners) == True:
                        grid[i][j] = False


    ### YOUR CODE GOES ABOVE HERE ###
    return grid, dimensions



