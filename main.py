import scrapper
from scrapper import IMDBPage
import pandas as pd
import json
from tqdm import tqdm
import json


def main():
    page = IMDBPage()
    movielens_df = pd.read_csv('movielens_poster.csv')

    movielens = movielens_df.to_dict('records')

    batch_size = 50 
    n_batch = (len(movielens_df) // batch_size) + 1

    for batch in tqdm(range(n_batch), position=0):
        movielens_batch = []

        for i, row in enumerate(tqdm(movielens[batch * batch_size: (batch + 1) * batch_size], position=1, leave=False)):
        # try:
            result = page.get_details(row['movie_url'])
            row = dict(row) 
            row.update(result)
            movielens_batch.append(row)
        # except Exception as e:
            # print('{} - caught on main: {}'.format(batch * batch_size + i,e))

        # with open('json/movielens100k_details_batch_{}.json'.format(batch), 'w') as f:
        #     json.dump(movielens_batch, f)

        # movielens_batch_df = pd.DataFrame(movielens_batch)
        # movielens_batch_df.to_csv('csv/movielens100k_details_batch_{}.csv'.format(batch))

if __name__=='__main__':
    main()
