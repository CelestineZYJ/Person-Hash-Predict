#  -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re
import json
import random


def get_hashtag(content):
    hashtag = re.findall(r"['\'](.*?)['\']", str(content))
    return hashtag


def get_user(content):
    user = re.split(r"[\[\],]", str(content))
    return user[1:-1]


def get_str(content):
    Str = str(content)
    return Str


def content_embedding(content, con_emb_dict):
    #try:
        return con_emb_dict[content]
    #except:
        #return [0]*768


def average_user_tweet(user_list, content_user_df, con_emb_dict):
    user_arr_dict = {}
    for user in user_list:
        embed_list = []
        x = content_user_df['content'].loc[(content_user_df['user_id']) == user].tolist()
        #print(x)
        content_list = x[0]

        for content in content_list:
            embed_list.append(content_embedding(content, con_emb_dict))
        embed_list = np.mean(np.array(embed_list), axis=0)
        user_arr_dict[user] = embed_list

    print(user_arr_dict)
    print("function: average_user_tweet()")
    return user_arr_dict


def average_hashtag_tweet(tag_list, content_tag_df, con_emb_dict):
    tag_arr_dict = {}
    print(len(tag_list))
    for index, tag in enumerate(tag_list):
        print(str(index)+tag)
        embed_list = []
        content_list = content_tag_df['content'].loc[(content_tag_df['hashtag']) == tag].tolist()[0]

        for content in content_list:
            embed_list.append(content_embedding(content, con_emb_dict))
        embed_list = np.mean(np.array(embed_list), axis=0)
        tag_arr_dict[tag] = embed_list
        #print(tag_arr_dict[tag])

    #print(tag_arr_dict)
    print("function: average_hashtag_tweet()")
    return tag_arr_dict


def rank_input_train(user_list, train_tag_list, user_arr_dict, tag_arr_dict, qid_train_dict):
    f = open('./tBert/trainBert.dat', "a")
    for user_num, user in enumerate(user_list):
        print('train_user_num: ' + str(user_num))
        user_arr = user_arr_dict[user]
        f.write(f"# query {user_num + 1}")
        positive_tag_list = qid_train_dict[user]
        for tag in positive_tag_list: # positive samples
            tag_arr = tag_arr_dict[tag]
            user_tag_arr = np.concatenate((user_arr, tag_arr), axis=None)
            x = 1
            Str = f"\n{x} {'qid'}:{user_num + 1}"
            for index, value in enumerate(user_tag_arr):
                Str += f" {index + 1}:{value}"
            f.write(Str)

        temp_tag_list = list(set(train_tag_list)-set(positive_tag_list))
        negative_tag_list = random.sample(temp_tag_list, 5*len(positive_tag_list))
        for tag in negative_tag_list: # negative samples
            tag_arr = tag_arr_dict[tag]
            user_tag_arr = np.concatenate((user_arr, tag_arr), axis=None)
            x = 0
            Str = f"\n{x} {'qid'}:{user_num + 1}"
            for index, value in enumerate(user_tag_arr):
                Str += f" {index + 1}:{value}"
            f.write(Str)
        f.write("\n")


def rank_input_test(user_list, test_tag_list, user_arr_dict, tag_arr_dict, qid_test_dict):
    f = open('./tBert/testBert.dat', "a")
    #tagF = open('./tBert/tagList.txt', "a", encoding="utf-8")

    for user_num, user in enumerate(user_list):
        print('test_user_num: ' + str(user_num))
        user_arr = user_arr_dict[user]
        f.write(f"# query {user_num + 1}")
        #tagF.write(f"# query {user_num + 1}\n")
        positive_tag_list = qid_test_dict[user]
        for tag in positive_tag_list:  # positive samples
            tag_arr = tag_arr_dict[tag]
            '''
            print("user_arr: "+str(type(user_arr)))
            print("tag_arr: "+str(type(tag_arr)))
            print(user_arr)
            print(tag_arr)
            '''
            user_tag_arr = np.concatenate((user_arr, tag_arr), axis=None)
            x = 1
            Str = f"\n{x} {'qid'}:{user_num + 1}"
            #tagF.write(f"{tag}\n")
            for index, value in enumerate(user_tag_arr):
                Str += f" {index + 1}:{value}"
            f.write(Str)
            '''
            try:
                tag_arr = tag_arr_dict[tag]
                user_tag_arr = np.concatenate((user_arr, tag_arr), axis=None)
                x = 1
                Str = f"\n{x} {'qid'}:{user_num + 1}"
                tagF.write(f"{tag}\n")
                for index, value in enumerate(user_tag_arr):
                    Str += f" {index + 1}:{value}"
                f.write(Str)
            except:
                print(tag)
            '''
        negative_tag_list = list(set(test_tag_list) - set(positive_tag_list))
        for tag in negative_tag_list:  # negative samples
            tag_arr = tag_arr_dict[tag]
            '''
            print("user_arr: "+str(type(user_arr)))
            print("tag_arr: "+str(type(tag_arr)))
            print(user_arr)
            print(tag_arr)
            '''
            user_tag_arr = np.concatenate((user_arr, tag_arr), axis=None)
            x = 0
            Str = f"\n{x} {'qid'}:{user_num + 1}"
            #tagF.write(f"{tag}\n")
            for index, value in enumerate(user_tag_arr):
                Str += f" {index + 1}:{value}"
            f.write(Str)
        f.write("\n")
        '''
            try:
                tag_arr = tag_arr_dict[tag]
                user_tag_arr = np.concatenate((user_arr, tag_arr), axis=None)
                x = 0
                Str = f"\n{x} {'qid'}:{user_num + 1}"
                tagF.write(f"{tag}\n")
                for index, value in enumerate(user_tag_arr):
                    Str += f" {index + 1}:{value}"
                f.write(Str)
            except:
                print(tag)
        f.write("\n")
        '''


def sort_train_user_tag(user_list, train_df):
    train_df['hashtag'] = train_df['hashtag'].apply(get_hashtag)
    train_tag_list = list(set(train_df['hashtag'].explode('hashtag').tolist()))
    qid_user_tag_dict = {}
    for user in user_list:
        spe_user_df = train_df.loc[train_df['user_id'] == user]
        spe_user_tag_list = list(set(spe_user_df['hashtag'].explode('hashtag').tolist()))
        qid_user_tag_dict[user] = spe_user_tag_list

    print(qid_user_tag_dict)
    return train_tag_list, qid_user_tag_dict


def sort_test_user_tag(user_list, test_df):
    test_df['hashtag'] = test_df['hashtag'].apply(get_hashtag)
    test_tag_list = list(set(test_df['hashtag'].explode('hashtag').tolist()))
    qid_user_tag_dict = {}
    for user in user_list:
        spe_user_df = test_df.loc[test_df['user_id'] == user]
        spe_user_tag_list = list(set(spe_user_df['hashtag'].explode('hashtag').tolist()))
        qid_user_tag_dict[user] = spe_user_tag_list

    print(qid_user_tag_dict)
    return test_tag_list, qid_user_tag_dict


def read_embedding(content_df, test_df):
    # 写userList
    '''
    user_list = list(set(test_df['user_id'].tolist()))
    f = open("wData/userList.txt", "w")
    f.write(str(user_list))
    f.close()

    # 读userlist，要灵活调换写与读以保持与其他实验的统一
    '''
    with open("tData/userList.txt", "r") as f:
        x = f.readlines()[0]
        print(x)
        user_list = get_hashtag(x)
        print(user_list)

    content_user_df = content_df.groupby(['user_id'], as_index=False).agg({'content': lambda x: list(x)})
    content_tag_df = content_df.explode('hashtag').groupby(['hashtag'], as_index=False).agg({'content': lambda x: list(x)})
    tag_list = list(set(content_tag_df['hashtag'].tolist()))
    emb_para_list = [user_list, content_user_df, tag_list, content_tag_df]
    '''
    train_df = pd.read_table('./data/trainSet.csv')
    train_df['hashtag'] = train_df['hashtag'].apply(get_hashtag)
    train_tag_list = list(set(train_df['hashtag'].explode('hashtag').tolist()))
    print(train_tag_list)
    print(tag_list)


    for tag in train_tag_list:
        if tag not in tag_list:
            print(tag)
    '''
    print("user_num: " + str(len(user_list)))
    print("tag_num: " + str(len(tag_list)))
    return emb_para_list


if __name__ == '__main__':
    train_df = pd.read_table('./tData/train.csv')
    test_df = pd.read_table('./tData/test.csv')

    # 这几个get_str是为了应对中文数据集经常读出来非str的问题，跑trec的时候注释掉这几句，不然会报错，原因待调查

    train_df['user_id'] = train_df['user_id'].apply(get_str)
    test_df['user_id'] = test_df['user_id'].apply(get_str)
    train_df['content'] = train_df['content'].apply(get_str)
    test_df['content'] = test_df['content'].apply(get_str)

    with open('./tData/embeddings.json', 'r') as f:
        con_emb_dict = json.load(f)

    embedSet = pd.read_table('./tData/embed.csv')
    # 这几个get_str是为了应对中文数据集经常读出来非str的问题，跑trec的时候注释掉这几句，不然会报错，原因待调查
    embedSet['user_id'] = embedSet['user_id'].apply(get_str)
    embedSet['content'] = embedSet['content'].apply(get_str)
    embedSet['hashtag'] = embedSet['hashtag'].apply(get_hashtag)
    emb_para_list = read_embedding(embedSet, test_df)

    emb_para_list.append(con_emb_dict)

    user_arr_dict = average_user_tweet(emb_para_list[0], emb_para_list[1], emb_para_list[4])
    tag_arr_dict = average_hashtag_tweet(emb_para_list[2], emb_para_list[3], emb_para_list[4])

    train_tag_df, qid_train_dict = sort_train_user_tag(emb_para_list[0], train_df)
    test_tag_df, qid_test_dict = sort_test_user_tag(emb_para_list[0], test_df)

    rank_input_train(emb_para_list[0], train_tag_df, user_arr_dict, tag_arr_dict, qid_train_dict)
    rank_input_test(emb_para_list[0], test_tag_df, user_arr_dict, tag_arr_dict, qid_test_dict)