import scrapper
from scrapper import IMDBPage
import pandas as pd
import json
from tqdm import tqdm

def main():
    page = IMDBPage()
    movielens_df = pd.read_csv('movielens_poster.csv')

    movielens = movielens_df.to_dict('records')
    for i, row in enumerate(movielens[:10]):
        result = page.get_details(row['movie_url'])
        row['description'] = result['description']
        movielens[i] = row
    print(movielens[:12])

    # movielens['description'] = movielens['movie_url'].progress_apply(lambda x: page.get_description(x))
    # movielens.to_csv('movielens100k_details.csv', index=False)
    # movielens.to_json('movielens100k_details.json', index=False)
        

if __name__=='__main__':
    main()
