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

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *


# Creates the pathnetwork as a list of lines between all pathnodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent=None):
	lines = []
	### YOUR CODE GOES BELOW HERE ###

	# get agent's size
	size = agent.getMaxRadius()

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

	# store all possible lines into lines
	for i in range(len(pathnodes)):
		for j in range(i+1,len(pathnodes)):
			lines.append((pathnodes[i],pathnodes[j]))


	# delete the lines which are intersected with obstacles

	trash_lines_1 = []

	for line in lines:
		for obstacleslines in obstacles_lines:
			if rayTraceWorld(line[0],line[1],obstacleslines) != None:
				trash_lines_1.append(line)

	newlines = list(set(lines)-set(trash_lines_1))

	# delete the lines which don't have sufficient space on either side of the edge

	trash_lines_2 = []

	for corners in obstacles_corners:
		for i in range(len(corners)):
			for line in lines:
				if minimumDistance(line,corners[i]) < size:
					trash_lines_2.append(line)

	newestlines = list(set(newlines)-set(trash_lines_2))

	# store the refined lines into lines

	lines = newestlines

	### YOUR CODE GOES ABOVE HERE ###
	return lines


