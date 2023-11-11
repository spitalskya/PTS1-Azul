from __future__ import annotations
from typing import List, Optional
from azul.interfaces import FinalPointsCalculationInterface
from azul.simple_types import Tile, Points


class FinalPointsCalculation(FinalPointsCalculationInterface):

    def __init__(self, component: FinalPointsCalculationInterface) -> None:
        self._component = component

    def getPoints(self, wall: List[List[Optional[Tile]]]) -> Points:
        return self._component.getPoints(wall)
    

class WallPointsCalculation(FinalPointsCalculationInterface):
    
    def __init__(self, horizontal: HorizontalRowPointsCalculation, vertical: VerticalColumnPointsCalculation, color: ColorPointsCalculation) -> None:
        self._horizontal = horizontal
        self._vertical = vertical
        self._color = color

    def getPoints(self, wall: List[List[Optional[Tile]]]) -> Points:
        return self._horizontal.getPoints(wall) + self._vertical.getPoints(wall) + self._color.getPoints(wall)


class HorizontalRowPointsCalculation(FinalPointsCalculationInterface):

    def getPoints(self, wall: List[List[Optional[Tile]]]) -> Points:
        for row in wall:
            if None not in row:
                return 2

        return 0


class VerticalColumnPointsCalculation(FinalPointsCalculationInterface):

    def getPoints(self, wall: List[List[Optional[Tile]]]) -> Points:
        points = 0
        for column in range(5):
            if None not in [row[column] for row in wall]:
                points += 7
            
        return points


class ColorPointsCalculation(FinalPointsCalculationInterface):
    
    def getPoints(self, wall: List[List[Optional[Tile]]]) -> Points:
        points = 0
        for i in range(5):
            if None not in [row[(i + j) % 5] for j, row in enumerate(wall)]:
                points += 10

        return points
