from tweet import api, getAllTweet
from data import accounts, bot
import numpy as np
import sys
from tqdm import tqdm
import time
import tweepy
import datetime
from sklearn.linear_model import LinearRegression

def normarize(x):
    return x/np.linalg.norm(x)
    #return x/np.max(x)



def getTimeStamps(id,m=0,M=sys.maxsize):
    result=[]
    for t in getAllTweet(id,v=False):
        stamp = int(t.created_at.timestamp())
        _stamp=stamp
        stamp = stamp // (24 * 60 * 60)
        if (stamp>m and stamp<M):
            result.append(stamp)
            #result.append((_stamp-stamp*24*60*60)//3600)

        if stamp<m:
            break
    result=np.asarray(result)
    return result


stamps41=getTimeStamps(bot)
m=np.min(stamps41)
M=np.max(stamps41)
x41=[0 for i in range(m,M+1)]
#x41=[0 for i in range(0,25)]
for stamp in stamps41:
    x41[stamp-m]+=1


x41=np.asarray(x41,dtype="float32")
x41=normarize(x41)

print(x41)

phai=[]
for account in tqdm(accounts):
    tweets=np.zeros_like(x41)
    try:
        stamps=getTimeStamps(account,m=m)
        for stamp in stamps:
            tweets[stamp-m]+=1
        tweets=normarize(tweets)
        phai.append(tweets)
        #print("...zzzZZZ")
        #time.sleep(60)
    except tweepy.error.TweepError:
        print("some error may occured while getting tweets of {0}".format(account))


phai=np.asarray(phai)
phai=phai.T
phai[np.isnan(phai)]=0#nan対策。ここ1年くらいツイートしてない人とか、RTしかしないrom専アカウントとか。
print(phai)

a=LinearRegression().fit(phai,x41)


result={}
for account,_a in zip(accounts,a.coef_):
    result[account]=_a
result=sorted(result.items(),key=lambda x:-x[1])

for i in result:
    print("{0}\t{1}".format(i[0],i[1]))
