# twitter_django_app
This is a sentiment analysis project on Twitter.

## Setup
```
cd twitter_django_app
[sudo] pip install virtualenv
mkdir venvs
virtualenv venvs
source venvs/bin/activate
pip install django
pip install Twython
pip install neo4django
```
## Requirements
You need to have basics of
- django
- neo4j graph database
  - cypher query language

## Description
The project intend at first level to collect tweets from tag using TwitterSearch API, therefore, we'll use **twitter_django_app/twitter_app/twitter_search/twitter_search.py** to gather tweets from different events. Thus, we need to do the following:
- edit the **twitter_search.py** to:
   -  extract the tweet with its content
      -  the number of retweets
         -  the different replies
	    -  the user with its localization
These values should be in **json** format
