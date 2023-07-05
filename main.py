import random
import json

file_path = "movies.dat"
output_file = "movie_titles.json"

# Read movie titles from the file
movie_titles = []
with open(file_path, "r") as file:
    for line in file:
        movie_data = line.strip().split("::")
        title_with_year = movie_data[1]
        title = title_with_year.split(" (")[0]  # Remove year and parentheses
        movie_titles.append(title)

# Select 10 random movie titles
random_titles = random.sample(movie_titles, 10)

# Write the titles to a JSON file
data = {"movie_titles": random_titles}

with open(output_file, "w") as file:
    json.dump(data, file, indent=4)

print("Movie titles saved to", output_file)
