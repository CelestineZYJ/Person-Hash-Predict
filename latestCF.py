import re
import random
import pandas as pd
import tqdm

dataPath = 't'
classifierPath = 'CF'


def get_hashtag(content):
    hashtag = re.findall(r"['\'](.*?)['\']", str(content))
    return hashtag


def get_str(content):
    Str = str(content)
    return Str


with open('./'+dataPath+'Data/userList.txt', "r") as f:
    x = f.readlines()[0]
    user_list = get_hashtag(x)
    print(user_list)


train_df = pd.read_table('./'+dataPath+'Data/train.csv')
test_df = pd.read_table('./'+dataPath+'Data/test.csv')

train_df['user_id'] = train_df['user_id'].apply(get_str)
test_df['user_id'] = test_df['user_id'].apply(get_str)


def sort_train_user_tag():
    train_df['hashtag'] = train_df['hashtag'].apply(get_hashtag)

    qid_user_tag_dict = {}
    for user in user_list:
        spe_user_df = train_df.loc[train_df['user_id'] == user]
        spe_user_tag_list = list(set(spe_user_df['hashtag'].explode('hashtag').tolist()))
        qid_user_tag_dict[user] = spe_user_tag_list

    return qid_user_tag_dict


def rank_input_test(qid_user_tag_dict):
    test_df['hashtag'] = test_df['hashtag'].apply(get_hashtag)
    test_tag_list = list(set(test_df['hashtag'].explode('hashtag').tolist()))
    for user_num, user in enumerate(user_list):
        print(user_num)
        f = open('./'+dataPath+classifierPath+'/'+classifierPath+'.dat', 'a')
        preF = open('./'+dataPath+classifierPath+'/pre'+classifierPath+'.txt', 'a')
        f.write(f"# query {user_num + 1}\n")
        test_spe_user_df = test_df.loc[test_df['user_id'] == str(user)]
        print(test_spe_user_df)
        positive_tag_list = list(set(test_spe_user_df['hashtag'].explode('hashtag').tolist()))
        for tag in positive_tag_list:  # positive samples
            x = 1
            Str = f"{x} {'qid'}:{user_num + 1}\n"
            f.write(Str)
            if tag in qid_user_tag_dict[user]:
                preF.write("1\n")
            else:
                preF.write("0\n")

        temp_tag_list = list(set(test_tag_list) - set(positive_tag_list))
        try:
            negative_tag_list = random.sample(temp_tag_list, 1000)
        except:
            negative_tag_list = temp_tag_list
        for tag in negative_tag_list:  # negative samples
            x = 0
            Str = f"{x} {'qid'}:{user_num + 1}\n"
            f.write(Str)
            if tag in qid_user_tag_dict[user]:
                preF.write("1\n")
            else:
                preF.write("0\n")

        f.close()
        preF.close()


rank_input_test(sort_train_user_tag())


