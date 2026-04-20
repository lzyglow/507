class Game:
    def __init__(self, data):
        """
        Initialize a Game object from RAWG API data, a dictionary from RAWG including game name, if, tags, genres, rating, releasing, platform.
        """
        self.id = data['id']
        self.name = data['name']
        self.genres = {g['name'] for g in data.get('genres', [])}
        self.tags = {g['name'] for g in data.get('tags', [])}
        if data.get('released'):
            self.release_year = int(data['released'][:4])
        else: 
            self.release_year = None
        self.rating = data['rating']
        self.platforms = {g['platform']['name'] for g in data.get('parent_platforms', [])}
        # above are placeholders for publisher and developers that are not included in this version of my implementation
        self.developers = set()
        self.publishers = set()
    def print_info(self):
        """
        Print out basic informations of a Game object.
        """
        print(f"{self.name}(ID: {self.id})")
        print(f"{'=' * 30}")
        print(f"Rating: {self.rating}")
        print(f"Release Year: {self.release_year if self.release_year else 'Unknown'}")
    
        print(f"Genres: {', '.join(self.genres) if self.genres else 'None'}")
        print(f"Tags: {', '.join(list(self.tags)[:10])}{'...' if len(self.tags) > 10 else ''}")  # limit to 10 tags
        print(f"Platforms: {', '.join(self.platforms) if self.platforms else 'None'}")
        
        if self.developers:
            print(f"Developers: {', '.join(self.developers)}")
        if self.publishers:
            print(f"Publishers: {', '.join(self.publishers)}")

        
def similarity(g1, g2): 
    '''
    function that calculate the similarity between two games, g1 and g2. 
    Args:
        g1 (Game): First game.
        g2 (Game): Second game.
    
    Returns:
        score(int): Similarity score.
    '''
    shared_genres = len(g1.genres & g2.genres)
    shared_tags = len(g1.tags & g2.tags)
    shared_platforms = len(g1.platforms & g2.platforms)
    same_dev = 1 if g1.developers & g2.developers else 0
    same_pub = 1 if g1.publishers & g2.publishers else 0
    if g1.release_year and g2.release_year and abs(g1.release_year - g2.release_year) <= 5:
        same_era = 1
    else:
        same_era = 0

    score = 1 * shared_genres + 1 * shared_tags + 1 * shared_platforms + same_dev + same_pub + same_era

    return score

