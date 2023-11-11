from __future__ import annotations
from typing import List
import unittest
import unittest.mock
from azul.simple_types import Tile, STARTING_PLAYER, RED, BLUE, YELLOW, GREEN, BLACK, FinishRoundResult, NORMAL, \
    GAME_FINISHED, Points
from azul.board import Board
from azul.interfaces import GameFinishedInterface, FinalPointsCalculationInterface, UsedTilesGiveInterface


class FakeGameFinished(GameFinishedInterface):
    def gameFinished(self, wall) -> FinishRoundResult:
        return NORMAL


class FakeFinalPoints(FinalPointsCalculationInterface):
    def getPoints(self, wall) -> Points:
        return Points()


class TestBoard(unittest.TestCase):
    board: Board

    def setUp(self) -> None:
        game_finished: FakeGameFinished = FakeGameFinished()
        final_points_calc: FakeFinalPoints = FakeFinalPoints()
        used_tiles: UsedTilesGiveInterface = UsedTilesGiveInterface()
        self.board = Board(game_finished, final_points_calc, used_tiles)

    def test_put_correct_tiles_in(self) -> None:
        tiles: List[Tile] = [RED]
        self.board.put(1, tiles)
        self.assertEqual(self.board.pattern_lines[0].state(), "R")

        tiles: List[Tile] = [STARTING_PLAYER, BLUE]
        self.board.put(2, tiles)
        self.assertEqual(self.board.pattern_lines[1].state(), "B")
        self.assertEqual(self.board.floor.state(), "S")

        self.board.put(2, BLUE)
        self.assertEqual(self.board.pattern_lines[1].state(), "BB")

        tiles: List[Tile] = [BLACK] * 4
        self.board.put(3, tiles)
        self.assertEqual(self.board.pattern_lines[2].state(), "LLL")
        self.assertEqual(self.board.floor.state(), "L")

        tiles: List[Tile] = [YELLOW] * 5
        self.board.put(4, tiles)
        self.assertEqual(self.board.pattern_lines[3].state(), "YYYY")
        self.assertEqual(self.board.floor.state(), "LY")

        tiles: List[Tile] = [BLUE] * 5
        self.board.put(5, tiles)
        self.assertEqual(self.board.pattern_lines[4].state(), "BBBB")

    def test_put_incorrect_tiles_in(self) -> None:
        tiles: List[Tile] = [STARTING_PLAYER]
        with self.assertRaises(KeyError):
            self.board.put(1, tiles)

        tiles: List[Tile] = [GREEN, STARTING_PLAYER, BLUE]
        with self.assertRaises(KeyError):
            self.board.put(2, tiles)

        tiles: List[Tile] = [YELLOW]
        self.board.put(2, tiles)
        with self.assertRaises(KeyError):
            self.board.put(2, [BLUE])

        tiles: List[Tile] = [RED, BLUE]
        with self.assertRaises(KeyError):
            self.board.put(3, tiles)

        tiles: List[Tile] = [RED, RED, RED, RED, BLUE]
        with self.assertRaises(KeyError):
            self.board.put(4, tiles)

        tiles: List[Tile] = [RED, GREEN, BLUE, YELLOW, BLUE, BLACK]
        with self.assertRaises(KeyError):
            self.board.put(5, tiles)

    def test_finish_round(self) -> None:
        tiles: List[Tile] = [RED]
        self.board.put(1, tiles)
        self.board.floor.put([STARTING_PLAYER, BLUE])
        self.board.finishRound()

        self.assertEqual(self.board.pattern_lines[0].state(), "")
        self.assertEqual(self.board.wall_lines[0].get_tiles(), [None, None, RED, None, None])

        points_calc_mock = unittest.mock.Mock(return_value=Points(1))
        self.board.final_points.getPoints = points_calc_mock

        self.assertEqual(self.board.floor.state(), "")
        self.assertEqual(self.board.points, -1)

    def test_endGame(self) -> None:
        self.board.endGame()
        self.assertFalse(self.board.end_game)

        game_finished_mock = unittest.mock.Mock(return_value=GAME_FINISHED)
        self.board.game_finished.gameFinished = game_finished_mock
        self.assertTrue(self.board.end_game)


if __name__ == '__main__':
    unittest.main()
