import unittest
import json
from Game import Game, similarity
from GameGraph import GameGraph
import io
import sys

class TestGame(unittest.TestCase):
    def setup(self):
        """
        Sample game data for testing
        """
        self.sample_data1 = {
            "id" : 1,
            "name" : "Test Game 1",
            "genres" : [{"name": "Action"}, {"name": "RPG"}],
            "tags" : [{"name": "Singleplayer"}, {"name": "Open World"}],
            "released" : "2020",
            "rating" : 4.6,
            "parent_platforms" : [{"platform" : {"name": "PC"}}, {"platform" : {"name": "PlayStation"}}] 
        }
        self.sample_data2 = {
            "id" : 2,
            "name" : "Test Game 2",
            "genres" : [{"name": "Action"}, {"name": "Casual"}],
            "tags" : [{"name": "Singleplayer"}, {"name": "Fantasy"}],
            "released" : "2022",
            "rating" : 4.2,
            "parent_platforms" : [{"platform" : {"name": "PC"}}, {"platform" : {"name": "Xbox"}}] 
        }
        #no released year
        self.sample_data3 = {
            "id" : 3,
            "name" : "Test Game 3",
            "genres" : [{"name": "Strategy"}, {"name": "Adventure"}],
            "tags" : [{"name": "Multiplayer"}],
            "released" : None,
            "rating" : 3.8,
            "parent_platforms" : [{"platform" : {"name": "Nintendo Switch"}}] 
        }
        #same as self.sample_data1
        self.sample_data4 = {
            "id" : 1,
            "name" : "Test Game 1",
            "genres" : [{"name": "Action"}, {"name": "RPG"}],
            "tags" : [{"name": "Singleplayer"}, {"name": "Open World"}],
            "released" : "2020",
            "rating" : 4.6,
            "parent_platforms" : [{"platform" : {"name": "PC"}}, {"platform" : {"name": "PlayStation"}}] 
        }

    def test_game_init(self):
        game = Game(self.sample_data1)
        self.assertEqual(game.id, 1)
        self.assertEqual(game.name, "Test Game 1")
        self.assertEqual(game.genres, {"Action", "RPG"})
        self.assertEqual(game.tags, {"Singleplayer", "Open World"})
        self.assertEqual(game.release_year, 2020)
        self.assertEqual(game.rating, 4.6)
        self.assertEqual(game.platforms, {"PC", "PlayStation"})
    
    def test_game_release_year_none(self): 
        """
        There are certain unreleased games in the dataset
        """
        game = Game(self.sample_data1)
        self.assertIsNone(game.release_year)

    def test_similarity_identical(self):
        game1 = Game(self.sample_data1)
        game4 = Game(self.sample_data4)
        score = similarity(game1, game4)
        # 2 genres + 2 tags + 2 platforms + same_era (1) = 7
        self.assertEqual(score, 7)
    
    def test_similarity_partial_same(self):
        game1 = Game(self.sample_data1)
        game2 = Game(self.sample_data2)
        score = similarity(game1, game2)
        # 1 genre + 1 tags + 1 platforms + same era (1) = 4
        self.assertEqual(score, 4)

    def test_similarity_no_similar(self):
        game1 = Game(self.sample_data1)
        game3 = Game(self.sample_data3)
        score = similarity(game1, game3)
        # 0 genre + 0 tags + 0 platforms + not same era (0) = 0
        self.assertEqual(score, 0)
    
    class TestGameGraph(unittest.TestCase):
        def setup(self):
            """
            Sample game data for testing
            """
            self.sample_data1 = {
                "id" : 1,
                "name" : "Test Game 1",
                "genres" : [{"name": "Action"}, {"name": "RPG"}],
                "tags" : [{"name": "Singleplayer"}, {"name": "Open World"}],
                "released" : "2020",
                "rating" : 4.6,
                "parent_platforms" : [{"platform" : {"name": "PC"}}, {"platform" : {"name": "PlayStation"}}] 
            }
            self.sample_data2 = {
                "id" : 2,
                "name" : "Test Game 2",
                "genres" : [{"name": "Action"}, {"name": "Casual"}],
                "tags" : [{"name": "Singleplayer"}, {"name": "Fantasy"}],
                "released" : "2022",
                "rating" : 4.2,
                "parent_platforms" : [{"platform" : {"name": "PC"}}, {"platform" : {"name": "Xbox"}}] 
            }
            #no released year
            self.sample_data3 = {
                "id" : 3,
                "name" : "Test Game 3",
                "genres" : [{"name": "Strategy"}, {"name": "Adventure"}],
                "tags" : [{"name": "Multiplayer"}],
                "released" : None,
                "rating" : 3.8,
                "parent_platforms" : [{"platform" : {"name": "Nintendo Switch"}}] 
            }
            
            self.games = [Game(self.sample_data1), Game(self.sample_data2), Game(), Game(self.sample_data3)]
            self.graph = GameGraph(self.games)


if __name__ == "__main__":
    unittest.main()
    
