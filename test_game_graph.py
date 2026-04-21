import unittest
import json
from Game import Game, similarity
from GameGraph import GameGraph
import io
import sys

class TestGame(unittest.TestCase):
    def setUp(self):
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
        game = Game(self.sample_data3)
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
    def setUp(self):
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
        
        self.games = [Game(self.sample_data1), Game(self.sample_data2), Game(self.sample_data3)]
        self.graph = GameGraph(self.games)

    def test_graph_node(self):
        self.assertEqual(len(self.graph.games), 3)
        self.assertIn("Test Game 1", self.graph.games)
        self.assertIn("Test Game 2", self.graph.games)
        self.assertIn("Test Game 3", self.graph.games)
    
    def test_graph_edge_with_large_threshold(self):
        total_edges_sum = sum(len(nei) for nei in self.graph.graph.values()) // 2
        self.assertEqual(total_edges_sum, 0)

    def test_graph_edge_with_low_threshold(self):
        self.graph.build_graph(threshold = 3)
        total_edges_sum = sum(len(nei) for nei in self.graph.graph.values()) // 2
        self.assertEqual(total_edges_sum, 1)
        self.assertIn("Test Game 2", self.graph.graph["Test Game 1"])

    def test_recommend(self):
        self.graph.build_graph(threshold = 3)
        recommendation = self.graph.recommend("Test Game 1", n = 2)
        self.assertEqual(len(recommendation), 1)
        self.assertEqual(recommendation[0][0], "Test Game 2")
        self.assertEqual(recommendation[0][1], 4)
        #isolate game
        recommendation = self.graph.recommend("Test Game 3", n = 2)
        self.assertEqual(len(recommendation), 0)
    
    def test_shortest_path_same_game(self):
        path, dist = self.graph.shortest_path("Test Game 1", "Test Game 1")
        self.assertEqual(dist, 0)
        self.assertEqual(path, ["Test Game 1"])

    def test_shortest_path_no_path(self):
        path, dist = self.graph.shortest_path("Test Game 1", "Test Game 3")
        self.assertEqual(dist, float('inf'))
        self.assertIsNone(path)
    
    def test_shortest_path_no_game(self):
        path, dist = self.graph.shortest_path("Test Game 1", "Not Exist Game")
        self.assertEqual(dist, float('inf'))
        self.assertIsNone(path)
    
    def test_shortest_path_indirect_better_than_direct(self):
        """
        Creat 3 games, where similarity of AC is 1 (dist = 0.5)
        similarity of AB is 5 (dist = 0.16667)
        similarity of AC is 5 (dist = 0.16667)
        Indirect ABC total cost = 2 * 0.16667 < 0.5 AC
        """
        data_A = {
            "id": 1, "name": "A",
            "genres": [{"name": "Action"}],
            "tags": [{"name": "Tag1"}, {"name": "Tag2"}, {"name": "Tag3"}, {"name": "Tag4"}, {"name": "Tag5"}],  
            "released": "2020", "rating": 4.0,
            "parent_platforms": [{"platform": {"name": "PC"}}]
        }
        data_B = {
            "id": 2, "name": "B",
            "genres": [{"name": "Shooting"}],
            "tags": [{"name": "Tag1"}, {"name": "Tag2"}, {"name": "Tag3"}, {"name": "Tag4"}, {"name": "Tag5"},{"name": "C1"}, {"name": "C2"}, {"name": "C3"}, {"name": "C4"}, {"name": "C5"}],  
            "released": "2010", "rating": 4.0,
            "parent_platforms": [{"platform": {"name": "Xbox"}}]
        }
        data_C = {
            "id": 3, "name": "C",
            "genres": [{"name": "Action"}], #same as A
            "tags": [{"name": "C1"}, {"name": "C2"}, {"name": "C3"}, {"name": "C4"}, {"name": "C5"}],  
            "released": "2000", "rating": 4.0,
            "parent_platforms": [{"platform": {"name": "Switch"}}]
        }
        game_a = Game(data_A)
        game_b = Game(data_B)
        game_c = Game(data_C)
        
        ab = similarity(game_a, game_b)  # 5 tag
        bc = similarity(game_b, game_c)  # 5 tag
        ac = similarity(game_a, game_c)  # 1 genre
        
        self.assertEqual(ab, 5)
        self.assertEqual(bc, 5)
        self.assertEqual(ac, 1)

        graph = GameGraph([game_a, game_b, game_c])
        graph.build_graph(threshold=0)
        
        path, distance = graph.shortest_path("A", "C")
        
        self.assertEqual(path, ["A", "B", "C"])
        
        expected_dist = 2 * (1 / 6)
        self.assertAlmostEqual(distance, expected_dist, places=5)
    
    def test_most_connected_game(self):
        self.graph.build_graph(threshold=3)
        top = self.graph.most_connected_game(1)
        #Test Game 1 and 2 have degree 1; Test Game 3 has 0 degree
        self.assertEqual(top[0][1], 1)
        self.assertIn(top[0][0], ["Test Game 1", "Test Game 2"])

    def test_highest_rating_in_genre(self):
        best = self.graph.highest_rating_game_in_genre("Casual", 1)
        self.assertEqual(best[0][0], "Test Game 2")
        self.assertEqual(best[0][1], 4.2)
    
    def test_highest_rating_by_tag(self):
        best = self.graph.highest_rating_game_by_tag("Singleplayer", 2)
        self.assertEqual(len(best), 2)
        self.assertEqual(best[0][0], "Test Game 1")
        self.assertEqual(best[1][0], "Test Game 2")
    
    def most_strong_connection(self):
        data_A = {
            "id": 1, "name": "A",
            "genres": [{"name": "Action"}],
            "tags": [{"name": "Tag1"}, {"name": "Tag2"}, {"name": "Tag3"}, {"name": "Tag4"}, {"name": "Tag5"}],  
            "released": "2020", "rating": 4.0,
            "parent_platforms": [{"platform": {"name": "PC"}}]
        }
        data_B = {
            "id": 2, "name": "B",
            "genres": [{"name": "Shooting"}],
            "tags": [{"name": "Tag1"}, {"name": "Tag2"}, {"name": "Tag3"}, {"name": "Tag4"}, {"name": "Tag5"},{"name": "C1"}, {"name": "C2"}, {"name": "C3"}, {"name": "C4"}, {"name": "C5"}],  
            "released": "2010", "rating": 4.0,
            "parent_platforms": [{"platform": {"name": "Xbox"}}]
        }
        data_C = {
            "id": 3, "name": "C",
            "genres": [{"name": "Action"}], #same as A
            "tags": [{"name": "C1"}, {"name": "C2"}, {"name": "C3"}, {"name": "C4"}, {"name": "C5"}],  
            "released": "2000", "rating": 4.0,
            "parent_platforms": [{"platform": {"name": "Switch"}}]
        }
        game_a = Game(data_A)
        game_b = Game(data_B)
        game_c = Game(data_C)

        graph = GameGraph([game_a, game_b, game_c])
        graph.build_graph(threshold=0)

        top = graph.most_strong_connection(1)
        self.assertEqual(top[0][1], 10)   # 10 tags
        self.assertIn(top[0][0], ["B"])




if __name__ == "__main__":
    unittest.main()
    
