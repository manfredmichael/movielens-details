import scrapper
from scrapper import IMDBPage
import pandas as pd
import json
from tqdm import tqdm

tqdm.pandas()

def main():
    page = IMDBPage()
    movielens = pd.read_csv('movielens_poster.csv')
    movielens['description'] = movielens['movie_url'].progress_apply(lambda x: page.get_description(x))
    movielens.to_csv('movielens100k_details.csv', index=False)
    movielens.to_json('movielens100k_details.json', index=False)
        

if __name__=='__main__':
    main()
