import sys
import json
from GameGraph import GameGraph
from Game import Game, similarity

class GameCLI:
    def __init__(self, graph):
        """
        Initialize CLI with a GameGraph.
        
        Args:
            graph (GameGraph): The game graph to explore.
        """
        self.graph = graph
        self.running = True
    
    def run(self):
        """
        Start running the CLI.
        """
        print("Welcome to game graph explorer! ")

        while self.running:
            self.print_menu()
            choice = self.get_choice()
            self.handle_choice(choice)
        print("Thank you for using game graph explorer.")
    
    def print_menu(self):
        """
        Print manu.
        """
        print("\n" + "="*40)
        print("1. Search for a game infomation")
        print("2. Recommend similar games")
        print("3. Find shortest path between two games")
        print("4. Show rankings")
        print("5. Quit")
    
    def get_choice(self):
        """
        Get user choice of menu.
        """
        while True:
            try:
                choice = int(input("Enter Your Choice Number: "))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("Please enter a number between 1 to 5")
            except ValueError:
                print("Invalid input, enter a number instead.")
    
    def handle_choice(self, choice):
        """
        Handle user choice with different functions.

        Args:
            choice(int): number 1-4.
        """
        if choice == 1:
            self.search_game_info()
        elif choice == 2:
            self.recommend_similar()
        elif choice == 3:
            self.shortest_path()
        elif choice == 4:
            self.rankings()
        else:
            self.running = False

    def find_game_with_suggestions(self, user_input): #try to find a game by exact name, offer partial matches if not found.
        """
        Locate a game by exact name or offer partial match suggestions.
        
        Args:
            user_input (str): Name entered by user.
        
        Returns:
            Game or None: Game object if found or suggested, else None.
        """
       
        if user_input in self.graph.games:
            return self.graph.games[user_input]
        matches = [name for name in self.graph.games.keys() if user_input.lower() in name.lower()]
        if matches:
            print("We did not find the exactly game you type. Do you mean one of these?")
            for i, j in enumerate(matches[:5], 1):
                print(f" {i}. {j}")
            choice = input("Enter number to choose game, or anything else to cancel:").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(matches[:5]):
                return self.graph.games[matches[int(choice)-1]]
            else:
                print("Cancelled.")
                return None
        else:
            print(f"Game '{user_input}' not found in dataset. Please check your typing.")
            return None
        

    
    def search_game_info(self):
        """
        Prompt for a game name and display its details.
        """
        
        name = input("\nEnter game name you want to search:").strip()
        game = self.find_game_with_suggestions(name) #something should be done here
        if game:
            game.print_info()
    
    def recommend_similar(self):
        """
        Prompt for a game name and num of recommendation, and then recommend using graph.recommend.
        """
        name = input("\nEnter game name: ").strip()
        game = self.find_game_with_suggestions(name)
        if game is None:
            print(f"Game {name} not found.")
            return
        try:
            n = int(input("How many recommendations? (default is 5)"))
        except ValueError:
            n = 5
        
        game_name = game.name
        reco = self.graph.recommend(game_name, n)
        if reco:
            print(f"top {n} similar games to '{game_name}'are:")
            for nei, wei in reco:
                print(f"   {nei} (similarity: {wei})")
        else:
            print(f"No similar games found for {game_name}")
    
    def shortest_path(self):
        """
        Prompt for two game names and compute the shortest path between them.
        """
        start = input("Enter your start game").strip()
        start_game = self.find_game_with_suggestions(start)
        if start_game is None:
            print(f"Game {start} not found.")
            return
        end = input("Enter your end game").strip()
        end_game = self.find_game_with_suggestions(end)
        if end_game is None:
            print(f"Game {end} not found.")
            return

        path, distance = self.graph.shortest_path(start_game.name, end_game.name)
        if path:
            print(" -> ".join(path))
            print(f"Total distance: {distance:.4f}")
        else:
            print("No connection found")


    def rankings(self):
        """
        Display sub-menu for various ranking options (most connected, highest rated, etc).
        """
        while True:
            print("Rankings Sub-Menu:")
            print("1. Most connected games")
            print("2. Strongest connected games")
            print("3. Highest rated games in a genre")
            print("4. Highest rated games by tag")
            print("5. Back to main menu")
            sub_choice = input("Enter your choice: ").strip()
            if sub_choice == "1":
                self.show_most_connected()
            elif sub_choice == "2":
                self.show_games_of_highest_similarity_sum()
            elif sub_choice == "3":
                self.show_highest_rated_in_genre()
            elif sub_choice == "4":
                self.show_highest_rated_by_tag()
            elif sub_choice == "5":
                break
            else:
                print("Invalid choice. Please enter 1-5.")
    
    def show_most_connected(self):
        """
        Prompt for n, and show top n connected games in graph.
        """
        try:
            n = int(input("How many top connected games to show?"))
        except ValueError:
            n = 10 #default
        most_conneted_games = self.graph.most_connected_game(n)
        print(f"Top {n} most connected games:")
        for name, degree in most_conneted_games:
            print(f" {name}: {degree} connections")

    def show_games_of_highest_similarity_sum(self):
        """
        Prompt for n, and show top n similarity sum games in graph.
        """
        try:
            n = int(input("How many top similarity sum games to show?"))
        except ValueError:
            n = 10 #default
        highest_sum_of_similarity = self.graph.most_strong_connection(n)
        print(f"Top {n} strongest connected game in the graph are:")
        for name, sum_similarity in highest_sum_of_similarity:
            print(f" {name} with sum of similarity: {sum_similarity}.")
        
    def show_highest_rated_in_genre(self):
        """
        Prompt for n and genre name, and show top n rated games of that genre.
        """
        genre = input("Enter the genre name:").strip()
        found_genre = None
        for g in self.graph.games.values():
            for genre_name in g.genres:
                if genre_name.lower() == genre.lower():
                    found_genre = genre_name
                    break
            if found_genre:
                break
        if not found_genre:
            print(f"Genre {genre} not found in dataset. Please check your spelling.")
            return
        
        try:
            n = int(input(f"How many top rated {genre} games to show?"))
        except ValueError:
            n = 5 #default
        
        best_games = self.graph.highest_rating_game_in_genre(found_genre, n)
        print(f"\nTop {len(best_games)} highest rated {found_genre} games are:")
        for i, (name, rating) in enumerate(best_games, 1):
            print(f"  {i}. {name} (rating: {rating})")

    def show_highest_rated_by_tag(self):
        """
        Prompt for n and tag name, and show top n rated games of that tag.
        """
        tag = input("Enter the tag name:").strip()
        found_tag = None
        for g in self.graph.games.values():
            for tag_name in g.tags:
                if tag_name.lower() == tag.lower():
                    found_tag = tag_name
                    break
            if found_tag:
                break
        if not found_tag:
            print(f"Genre {tag} not found in dataset. Please check your spelling.")
            return
        
        try:
            n = int(input(f"How many top rated {tag} games to show?"))
        except ValueError:
            n = 5 #default
        
        best_games = self.graph.highest_rating_game_by_tag(found_tag, n)
        print(f"\nTop {len(best_games)} highest rated {found_tag} games are:")
        for i, (name, rating) in enumerate(best_games, 1):
            print(f"  {i}. {name} (rating: {rating})")


if __name__ == "__main__":
    with open("games_raw_1500.json", "r", encoding = "utf-8") as f:
        game_data = json.load(f)
    game_objects = []
    for data in game_data:
        try:
            game_objects.append(Game(data))
        except Exception as e:
            print(f"skip game {data.get('name', 'unknown')}: {e}")
    graph = GameGraph(game_objects)
    cli = GameCLI(graph)
    cli.run()


        



        