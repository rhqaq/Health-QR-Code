import json
import pandas as pd
from tqdm import tqdm


# 去除重复项微博
def remove_duplicated_profile(profiles):
    href_list_for_remove = []
    removed_profiles = []
    for profile in tqdm(profiles):

        if profile['content'] == 'dead':
            continue
        elif str(profile['href']) in href_list_for_remove:

            continue
        else:
            href_list_for_remove.append(str(profile['href']))
            removed_profiles.append(profile)
    return removed_profiles

# 打开用户信息文件
with open('user_info.json', 'r', encoding='utf-8') as fp:
    user_list = json.load(fp)


href_list = []

finish_user_list = []
number = 0
gover_num = 0

with open('dead_author.json', 'r', encoding='utf-8') as fp:
    finish_href_list = json.load(fp)

print('总信息数')
# 读取个人用户的信息
for single_user in tqdm(user_list):
    if len(single_user.keys())<17:

        try:
            href_list.append(single_user["href"])

        except:
            number += 1
            # print(single_user)
    else:
        if single_user["昵称"]=="":
            gover_num += 1
        finish_user_list.append(single_user)
        # finish_href_list.append(single_user["href"])

all_user_profile =finish_user_list

print('用户profie数量')
print(len(all_user_profile))

user_profiles = remove_duplicated_profile(all_user_profile)

for user_profile in user_profiles:
    finish_href_list.append(user_profile["href"])
print(len(user_profiles))

print(len(finish_href_list))
with open('combined_profiles.json','w',encoding='utf-8') as fp:
    json.dump(user_profiles, fp, indent=4, ensure_ascii=False)

df_hrefs = pd.read_csv('author_href.csv')
hrefs = []

print(df_hrefs.shape[0])
for index, row in df_hrefs.iterrows():
    if row['author_href'] not in finish_href_list:
        hrefs.append(row['author_href'])

print(len(hrefs))
with open('author_href_ongoing.json', 'w', encoding='utf-8') as fp:
    json.dump(hrefs, fp, indent=4, ensure_ascii=False)