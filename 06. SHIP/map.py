import pygame
from config import *

class MapLoader():
    def __init__(self) -> None:
        pass

    def load(self, path):
        coord = self.loadMapCoordinates(path)
        mapRects = self.generateMapRects(coord)
        return mapRects

    def loadMapCoordinates(self, path):
        coordinates = []
        with open(path) as file:
            for indexY, linha in enumerate(file):
                for indexX, coluna in enumerate(linha): 
                    if coluna == MAP_CHAR:
                        coordinates.append((indexX+1, indexY+1))
        return coordinates

    def generateMapRects(self, coords):
        rects = []
        for coord in coords:
            rects.append(
                pygame.Rect(coord[0]*MULTI_FACTOR, 
                            coord[1]*MULTI_FACTOR+OFFSET_Y, 
                            MAP_RECT_X*MULTI_FACTOR, 
                            MAP_RECT_Y*MULTI_FACTOR))
        return rects