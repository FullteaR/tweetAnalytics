import tweepy
from keys import consumerKey,consumerSecret,myAccessToken,myAccessTokenSecret

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(myAccessToken, myAccessTokenSecret)

api = tweepy.API(auth)

def getAllTweet(id):
    i=0
    while True:
        tweets = api.user_timeline(id=self.id, page=i)
        for tweet in tweets:
            yield tweet
        i+=1

#api.get_user(id)

print(api.get_user("b1115_s"))
