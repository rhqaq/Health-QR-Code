import json
import pandas as pd
from tqdm import tqdm


def get_author_href(all_weibo):
    author_list = []
    for weibo in tqdm(all_weibo):
        if weibo['author_href'] in author_list:
            continue
        else:
            author_list.append(weibo['author_href'])
    print(len(author_list))
    df_author = pd.DataFrame({'author_href':author_list})
    df_author.to_csv('author_href.csv', encoding='utf-8')
    return author_list


if __name__ == "__main__":
    with open('all_weibo.json', 'r', encoding='utf-8') as fp:
        weibo_list = json.load(fp)
    a = get_author_href(weibo_list)