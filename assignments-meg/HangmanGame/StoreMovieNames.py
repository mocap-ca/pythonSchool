import json

"""Creates a JSON file for storing the questions for the Hangman game"""
movies = {'Hulk': 'Hulk.jpg',
          'Mary Poppins': 'MaryPoppins.jpg',
          'Spirited Away': 'SpiritedAway.jpg',
          'Toy Story': 'ToyStory.jpg'}
try:
    with open('Database/MoviesDatabase.json', 'w') as data_file:
        json.dump(movies, data_file)
except ValueError as write_error:
    print("Database could not be created.\n", write_error)
