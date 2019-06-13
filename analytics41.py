from utils import api, getAllTweet, whetherRT
from data import bot, accounts
import sys
import pandas as pd


# making test data
df_test = pd.DataFrame(columns=["id", "text", "reply", "created_at"])
for tweet in getAllTweet(bot, v=True):
    if whetherRT(tweet):
        continue
    id = tweet.id
    text = tweet.text
    created_at = tweet.created_at
    reply = tweet.in_reply_to_user_id
    df_test = df_test.append(pd.DataFrame([[id, text, reply, created_at]], columns=[
        "id", "text", "reply", "created_at"]), ignore_index=True)

df_test.to_excel("test.xlsx")


# making train data
df_train = pd.DataFrame(
    columns=["id", "text", "reply", "created_at", "user_id", "screen_name"])
for account in accounts:
    for tweet in getAllTweet(account, v=True):
        if whetherRT(tweet):
            continue
        id = tweet.id
        text = tweet.text
        created_at = tweet.created_at
        reply = tweet.in_reply_to_user_id
        user_id = tweet.user.id
        screen_name = tweet.user.screen_name
        df_train = df_train.append(pd.DataFrame([[id, text, reply, created_at, user_id, screen_name]], columns=[
            "id", "text", "reply", "created_at", "user_id", "screen_name"]), ignore_index=True)

df_train.to_excel("train.xlsx")
