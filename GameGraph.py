from Game import Game, similarity
import json
import heapq

class GameGraph:
    def __init__(self, games):
        '''
        Build graph from list of Game objects.
        
        Args:
            games: List of Game instances.
        '''
        self.games = {}
        for game in games:
            self.games[game.name] = game
        
        self.graph = {}
        self.build_graph()
        
    def build_graph(self, threshold = 14): # only add edge if similarity > threshold
        '''
        Compute pairwise similarity and create adjacency dictionary
        
        Args:
            threshold (int): Minimum similarity score to be considered an edge.
        '''
        game_list = list(self.games.values())
        n = len(game_list)

        for game in game_list:
            self.graph[game.name] = {}

        for i in range(n):
            g1 = game_list[i]
            for j in range(i+1, n):
                g2 = game_list[j]
                sim = similarity(g1, g2)
                if sim > threshold:
                    self.graph[g1.name][g2.name] = sim 
                    self.graph[g2.name][g1.name] = sim 
        print(f"build a graph with {n} nodes and {sum(len(nei) for nei in self.graph.values()) // 2} edges")

    '''
    def get_neighbors(self, game_name):
        if game_name not in self.graph:
            return {}
        return self.graph[game_name].copy()
    '''
    
    def recommend(self, game_name, n=5):
        '''
        Return top n most similar games to the given game.
        
        Args:
            game_name (str): Name of the source game.
            n (int): Number of recommendations to return.
        
        Returns:
            sort_neighbors_by_sim(list of tuple): [(neighbor_name, similarity_weight)...]. It's sorted descending by similarity weight.
        '''
        if game_name not in self.graph:
            print("sry, this game is not implemented yet.")
            return []
        neighbors = self.graph[game_name]
        sort_neighbors_by_sim = sorted(neighbors.items(), key = lambda x:x[1] , reverse=True)
        if len(sort_neighbors_by_sim) > n:
            return sort_neighbors_by_sim[:n]
        return sort_neighbors_by_sim

    def shortest_path(self, start_game, end_game):
        """
        Find shortest path between two games using Dijkstra's algo. Edge cost = 1 / (1 + similarity) → lower cost = higher similarity.
        
        Args:
            start_game (str): Name of start game.
            end_game (str): Name of end game.
        
        Returns:
            tuple: (list of game names(str) in path, total distance cost(int)).
        """
        if start_game not in self.games or end_game not in self.games:
            return None, float('inf')
        if start_game == end_game:
            return [start_game], 0
        
        dist = {node: float('inf') for node in self.graph}
        dist[start_game] = 0
        prev = {node: None for node in self.graph}
        pq = [(0, start_game)]

        while pq:
            cur_dist, cur_node = heapq.heappop(pq)
            if cur_dist > dist[cur_node]:
                continue #continue if we found better trail to thsi node
            if cur_node == end_game:
                break
            for neighbor, similarity in self.graph[cur_node].items():
                cost = 1 / (1 + similarity)
                new_dist = cur_dist + cost
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = cur_node
                    heapq.heappush(pq, (new_dist, neighbor))
        if dist[end_game] == float('inf'):
            return None, float('inf')
        path = []
        node = end_game
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
        return path, dist[end_game]
    
    #rest are for rankings of different kinds
    def most_connected_game(self, num = 1):
        """
        Find games with the highest number of neighbors.
        
        Args:
            num (int): Number of top games to find.
        
        Returns:
            top_num(list of tuple): [(game_name, degree)...]. It's sorted descending by degree.
        """
        degree = [(name, len(neighbors)) for name, neighbors in self.graph.items()]
        degree_sorted = sorted(degree, key = lambda x: x[1], reverse = True)
        top_num = degree_sorted[:num]
        return top_num
    
    def highest_rating_game_in_genre(self, genre, num = 1):
        """
        Find num games with the highest rating in genre given.
        
        Args:
            genre(str): Genre name.
            num (int): Number of top games to find.
        
        Returns:
            cand_sort(list of tuple): [(game_name, rating)...]. It's sorted descending by rating.
        """
        genre = genre.strip()
        cand = []
        for name, game in self.games.items():
            #print(genre, game.genres)
            if genre in game.genres:
                cand.append((name, game.rating))
        cand_sort = sorted(cand, key = lambda x: x[1], reverse = True)
        return cand_sort[:num]
    
    def highest_rating_game_by_tag(self, tag, num = 1):
        """
        Find num games with the highest rating by tag given.
        
        Args:
            tag (str): Tag name.
            num (int): Number of top games to find.
        
        Returns:
            cand_sort(list of tuple): [(game_name, rating)...]. It's sorted descending by rating.
        """
        tag = tag.strip()
        cand = []
        for name, game in self.games.items():
            #print(genre, game.genres)
            if tag in game.tags:
                cand.append((name, game.rating))
        cand_sort = sorted(cand, key = lambda x: x[1], reverse = True)
        return cand_sort[:num]

    
    def most_strong_connection(self, num = 1):
        """
        Find num games with the highest sum in neighbor similarities.
        
        Args:
            num (int): Number of top games to find.
        
        Returns:
            total_sum_sorted(list of tuple): [(game_name, sum_of_similarity)...]. It's sorted descending by sum_of_similarity.
        """
        total_sum = [(name, sum(neighbors.values())) for name, neighbors in self.graph.items()]
        total_sum_sorted = sorted(total_sum, key = lambda x: x[1], reverse = True)
        return total_sum_sorted[:num]
    
    def get_all_edges(self):
        pass



'''
with open("games_raw_300.json", "r", encoding = "utf-8") as f:
    game_data = json.load(f)

game_objects = []
for data in game_data:
    try:
        game_objects.append(Game(data))
    except Exception as e:
        print(f"skip game {data.get('name', 'unknown')}: {e}")

graph = GameGraph(game_objects)

#test recommend games
input_game_name = "Persona 5 Royal"
recommendations = graph.recommend(input_game_name, n=5)

print(f"top 5 similar games to '{input_game_name}'are:")
for nei, wei in recommendations:
    print(f"   {nei} (similarity: {wei})")

#test shortest path
path, distance = graph.shortest_path("The Elder Scrolls VI", "No Case Should Remain Unsolved")
if path:
    print(" -> ".join(path))
    print(f"Total distance: {distance:.4f}")
else:
    print("No connection found")

#test print game info
target_name = "The Elder Scrolls VI"
game_obj = None

for game in game_objects:
    if game.name == target_name:
        game_obj = game
        break

if game_obj:
    game_obj.print_info()
else:
    print(f"Game '{target_name}' not found in dataset. Please check your typeing.")

#test ranking
most_conneted_games = graph.most_connected_game(5)
print("Top 5 most connected games:")
for name, degree in most_conneted_games:
    print(f" {name}: {degree} connections")

best_rpg = graph.highest_rating_game_in_genre("RPG", 1)[0]
print(f" Highest rated RPG: {best_rpg[0]} with rating: {best_rpg[1]}")

highest_sum_of_similarity = graph.most_strong_connection(1)[0]
print(f" Strongest connected game in the graph is: {highest_sum_of_similarity[0]} with sum of similarity: {highest_sum_of_similarity[1]}")
'''