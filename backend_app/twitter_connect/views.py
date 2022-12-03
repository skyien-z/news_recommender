from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.models import User #####

import newspaper
import re  # for regex parsing
import requests
from newspaper import Article
from newsapi import NewsApiClient
import tweepy

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAGcZjwEAAAAA%2BCnFuw%2FosXOB1eC22p9gM2wsMN0%3DEMKVdVmfbiyDb6jsqbSynpD4AByBynhuXgyre4BwgPLgpxP9L1'
tweepy_client = tweepy.Client(BEARER_TOKEN)

NEWS_API_KEY = '52653260d37b4c7d9efd3731ac9156e3'
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def getBasicKeywords(url):
    # Access the HTML of the url and scrape the data we need
    article = Article(url)
    article.download()
    article.parse()
    
    # clean the string of the article text and return
    article.nlp()
    return article.keywords

def getUrlFromTweet(tweet_txt):
    '''
    Return first URL from tweet text string
    '''
    list_of_urls = re.findall(r'(https?://[^\s]+)', tweet_txt)
    if list_of_urls == []:
        return "empty"

    return list_of_urls[0]

def getArticlesUsingNLPBasicKeywords(url):
    keywords_list = getBasicKeywords(url)
    query_str = ""
    for i in range(len(keywords_list)):
        query_str += "+" + keywords_list[i]
        if i != len(keywords_list) - 1:
            query_str += " OR "

    headlines = newsapi.get_everything(q=query_str[0:len(query_str) - 1], sort_by='relevancy',
                                      language='en')
    return headlines

def get_news_articles(request):
    tweet_id = request.GET.get('tweet_id', None)
    tweet_request = tweepy_client.get_tweet(tweet_id)
    tweet_txt = tweet_request.data.text

    url = getUrlFromTweet(tweet_txt)

    if url == "empty":
        # background.js will check for this title and log a console.error instead of trying
        # to generate a notification
        return JsonResponse({"title": "There are no news articles in this tweet"})

    articles_dict = getArticlesUsingNLPBasicKeywords(url)

    # makes sure to return a unique article
    if articles_dict['articles'][0]['url'] == url:
        return JsonResponse(articles_dict['articles'][1])
    else:
        return JsonResponse(articles_dict['articles'][0])