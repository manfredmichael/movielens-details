import pandas as pd
import json
import os
import ast

# get genre in string format 
with open('genre.json') as f:
    genre_to_str = json.load(f)

full_csv = pd.DataFrame()
full_json = dict()

# merge all csv batches
for filename in os.listdir('csv'):
    filepath = os.path.join('csv', filename)
    batch_csv = pd.read_csv(filepath, index_col=0)
    full_csv = full_csv.append(batch_csv)

# add genre in string format
full_csv['movie_genres'] = full_csv['movie_genres'].apply(
    lambda genres: [int(i) for i in genres.replace('[','').replace(']','').split()]
)
full_csv['genre'] = full_csv['movie_genres'].apply(
    lambda genres: [genre_to_str[str(genre)] for genre in genres if genre in genre_to_str]
)

full_csv.to_csv('../movielens100k_details.csv', index=False)



full_csv = pd.DataFrame()

# merge all batches
for filename in os.listdir('csv'):
    filepath = os.path.join('csv', filename)
    batch_csv = pd.read_csv(filepath, index_col=0)
    full_csv = full_csv.append(batch_csv)

# add genre in string format
full_csv['movie_genres'] = full_csv['movie_genres'].apply(
    lambda genres: [int(i) for i in genres.replace('[','').replace(']','').split()]
)
full_csv['genre'] = full_csv['movie_genres'].apply(
    lambda genres: [genre_to_str[str(genre)] for genre in genres if genre in genre_to_str]
)

# save as csv
full_csv.to_csv('../movielens100k_details.csv', index=False)

# save as json
full_csv = full_csv.where(pd.notnull(full_csv), None)
with open('../movielens100k_details.json', 'w') as f:
    json.dump(full_csv.to_dict('records'), f)
