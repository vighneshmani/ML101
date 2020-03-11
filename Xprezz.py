import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def percentage(self, part, whole):
        return 100 * float(part)/float(whole)

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def DownloadData(self):

        consumerKey = "olD7jKIxvcnbpdtd9SBGmqqeA"
        consumerSecret = "33eoudaTgfgrsLMYyTyDj786ObUf9DCJsSvK84RNscDth0BweG"
        accessToken = "1016016867796742145-kO8bRUby0SvA197d1FBjXm1VpJn4Ao"
        accessTokenSecret = "IncdcuxnYukvpd9vSAzHlql8rs3e2bXPlcCkPjmt0RyCO"
        auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret) #set_access_token is a function used to get access token from auth object that we defined
        api = tweepy.API(auth)

        searchTerm = input("Enter the keyword/hashtags to search = ")
        noOfSearchTerms = int(input("Enter the number of tweets to analyze = "))

        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang="English").items(noOfSearchTerms)


        positive = 0
        negative = 0
        neutral  = 0
        polarity = 0

        for tweet in self.tweets:
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            print(tweet.text)
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity

            if analysis.sentiment.polarity == 0:
                neutral += 1
            if analysis.sentiment.polarity < 0:
                negative += 1
            if analysis.sentiment.polarity > 0:
                positive += 1

        positive = self.percentage(positive, noOfSearchTerms) #Percentage of positive tweets
        negative = self.percentage(negative, noOfSearchTerms) #Percentage of negative tweets
        neutral = self.percentage(neutral, noOfSearchTerms) #Percentage of neutral tweets

        positive = float(format(positive, '.2f'))
        negative = float(format(negative, '.2f'))
        neutral = float(format(neutral, '.2f'))

        print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfSearchTerms) + " tweets.")


        if polarity == 0:
            print("Neutral")
        elif polarity < 0:
            print("Negative")
        elif polarity > 0:
            print("Positive")

        label = ['Positive ['+ str(positive)+'%]','Neutral ['+ str(neutral)+'%]','Negative ['+ str(negative)+'%]']
        sizes = [positive,neutral,negative]
        colors =['green','yellow','red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, label, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()