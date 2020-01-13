# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:11:08 2020

@author: sagar
"""

from flask import Flask,render_template,request
import tweepy

#---------------------------------------------------------------------------
consumer_key = "8s67OREQ7SfMeMuLNEf1GiQAT"
consumer_secret = "qqJrqXaLjJRzZ9Z8wkP8FkVosNa9iv2ppi9ECAZhDE4GbITv4H"
access_token = "389504787-eOmVCmDB4IXOydQij49afAfku3jK8o9DnZ5s9AAg"
access_token_secret = "IMeSUn7oGiaM4KR3vBXhVIcAVnI4CK41UeNkJNTN0xTEJ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def twitter(searchTerm, NoOfTerms):
    import tweepy
    from textblob import TextBlob
    import re

    consumer_key = "8s67OREQ7SfMeMuLNEf1GiQAT"
    consumer_secret = "qqJrqXaLjJRzZ9Z8wkP8FkVosNa9iv2ppi9ECAZhDE4GbITv4H"
    access_token = "389504787-eOmVCmDB4IXOydQij49afAfku3jK8o9DnZ5s9AAg"
    access_token_secret = "IMeSUn7oGiaM4KR3vBXhVIcAVnI4CK41UeNkJNTN0xTEJ"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    
    # searching for Tweets
    tweets = api.search(searchTerm, count = NoOfTerms, lang = 'en')
    
    def clean_tweet(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())
    
    positive = 0; negative = 0; neutral = 0; 
    polarity = 0
    
    for tweet in tweets:
        analysis = TextBlob(clean_tweet(tweet.text))
        polarity += analysis.sentiment.polarity
        if(analysis.sentiment.polarity == 0):
            neutral += 1
        elif(analysis.sentiment.polarity > 0):
            positive += 1
        elif(analysis.sentiment.polarity < 0):
            negative += 1
            
    def percentage(tweet_class, NoOfTerms):
        return format((100 * float(tweet_class)/float(NoOfTerms)), '.2f')
    
    positive = percentage(positive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)

    return (positive, negative, neutral, polarity)
#-------------------------------------------------------------------------

def plot_pie(positive, negative, neutral, search_tweet, num_tweet):
    import matplotlib.pyplot as plt
# plotting pie chart
    labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]','Negative [' + str(negative) + '%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen','lightgreen','red']  # , 'gold', 'red','lightsalmon','darkred'
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on ' + search_tweet + ' by analyzing ' + str(num_tweet) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('static/images/new_plot.png')
#-------------------------------------------------------------------------

def tweet_sentiment(polarity):
    if polarity == 0:
        sentiment = "Neutral"
    elif polarity < 0:
        sentiment = "Negetive"
    else:
        sentiment = "Positive"
    return sentiment


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predict",methods=["POST", "GET"])
def predict():
    if request.method == 'POST':
        search_tweet = request.form['message']
        num_tweet = request.form["num"]
    else:
        #search_tweet = r"Modi"
        #num_tweet = 10
        search_tweet = request.args.get("message")
        num_tweet = request.args.get("num")
        
    val = twitter(search_tweet, num_tweet)
    positive, negative, neutral, polarity = val
    
    #return render_template('index.html', hash_tag = search_tweet, num_tweet = num_tweet, result = val)
    sentiment = tweet_sentiment(polarity)
    return render_template('index.html', 
                result = """Latest {} tweets  on "{}" \n is showing {} sentiment""".format(num_tweet, search_tweet,  sentiment))


@app.route('/plot',methods=["POST"])
def plot():
    if request.method == 'POST':
        search_tweet = request.form['message']
        num_tweet = request.form["num"]
    else:
        search_tweet = request.args.get("message")
        num_tweet = request.args.get("num")
    
    val = twitter(search_tweet, num_tweet)
    
    positive, negative, neutral, polarity = val
    plot_pie(positive, negative, neutral, search_tweet, num_tweet)
    
    sentiment = tweet_sentiment(polarity)
    
    return render_template('result.html',  url ='/static/images/new_plot.png', 
            result = """Latest {} tweets  on "{}" \n is showing {} sentiment""".format(num_tweet, search_tweet,  sentiment))

if __name__ == "__main__":
    app.run(debug=True)

#app.run()


