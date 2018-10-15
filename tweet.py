import tweepy
from keys import consumerKey,consumerSecret,myAccessToken,myAccessTokenSecret
import sys
import matplotlib.pyplot as plt
import datetime


auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(myAccessToken, myAccessTokenSecret)

api = tweepy.API(auth)

def getAllTweet(id):
    i=0
    while True:
        tweets = api.user_timeline(id=id, page=i)
        for tweet in tweets:
            print(tweet.text)
            yield tweet
        i+=1
        if len(tweets)==0:
            return

def weatherRT(tweet):#あまり良くない実装なのは気がついているよ
    try:
        id = tweet.retweeted_status.author.screen_name
        return True
    except:
        return False

def weatherReply(tweet):#簡易実装
    if tweet.text[0]=="@":
        return True
    return False


def analytics(id):
    """
    ツイート頻度をグラフ化します。
    本プログラムは法律、条例等に違反しない範囲でご利用ください。
    """
    t=[]
    m=10**10
    M=0
    tweet=[]
    RT=[]
    reply=[]

    try:
        for t in getAllTweet(id):
            stamp=int(t.created_at.timestamp())
            day=stamp//(24*60*60)
            if weatherRT(t):
                RT.append(day)
            elif weatherReply(t):
                reply.append(day)
            else:
                tweet.append(day)
    except:
        pass
    m=min(min(tweet),min(RT),min(reply))
    M=max(max(tweet),max(RT),max(reply))
    t=[datetime.datetime.fromtimestamp(i*24*60*60) for i in range(m,M+1)]

    y_tweet=[0 for i in range(len(t))]
    y_RT=[0 for i in range(len(t))]
    y_reply=[0 for i in range(len(t))]
    y_total=[0 for i in range(len(t))]


    for d in tweet:
        y_tweet[d-m]+=1
        y_total[d-m]+=1
    for d in reply:
        y_reply[d-m]+=1
        y_total[d-m]+=1
    for d in RT:
        y_RT[d-m]+=1
        y_total[d-m]+=1


    plt.title(id)
    plt.figure(1)
    plt.subplot(211)
    plt.xlabel("day")
    plt.ylabel("tweet")
    plt.scatter(t,y_tweet,label="tweet")
    plt.scatter(t,y_RT,label="RT")
    plt.scatter(t,y_reply,label="reply")
    plt.scatter(t,y_total,label="total")
    plt.legend()

    y_tweet=[sum(y_tweet[:i:]) for i in range(len(y_tweet))]
    y_reply=[sum(y_reply[:i:]) for i in range(len(y_reply))]
    y_RT=[sum(y_RT[:i:]) for i in range(len(y_RT))]
    y_total=[sum(y_total[:i:]) for i in range(len(y_total))]

    plt.subplot(212)
    plt.xlabel("day")
    plt.ylabel("tweet")
    plt.plot(t,y_tweet,label="tweet")
    plt.plot(t,y_RT,label="RT")
    plt.plot(t,y_reply,label="reply")
    plt.plot(t,y_total,label="total")
    plt.legend()

    plt.tight_layout()
    plt.show()
