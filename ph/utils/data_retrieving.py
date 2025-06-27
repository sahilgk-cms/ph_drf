import os
import logging
from mongoengine.connection import get_db
from typing import List
import requests
from newspaper import Article
from ph_drf.config import TIMESPAN_DICT, SERP_API_KEY
from ph.utils.date_formatting import convert_iso_date_into_ddmmyyyy

def get_previous_data(duration: str = "this week") -> List[dict]:
    '''
    This function fetches previous data from MOngoDB
    Args:
        duration (str)
    Returns:
        list of data for the given duration
    '''
    db = get_db()
    collection = db["processed_data"]

    match_stage = {}
    start_date = TIMESPAN_DICT.get(duration)
    match_stage["$expr"] = {
            "$gte": [
                {
                    "$dateFromString":{
                        "dateString": "$date",
                        "format": "%d/%m/%Y",
                        "onError": None,
                        "onNull": None
                    }
                },
                start_date
            ]
        }

    results = list(
        collection.find(match_stage,
                            {"date", "title", "text"})
        .sort("date", -1)
    )
    return results


def search_articles_in_database(entities: dict):
    '''
    This function searches articles in MOngoDB based on entities
    Args:
        entities (dict)
    Returns:
        list of data for the given entities
    '''
    db = get_db()
    collection = db["processed_data"]
    query = {
        "$or": [
                {"matched_disease": {"$regex": entities["disease"], "$options": "i"}},
                {"matching_word": {"$regex": entities["disease"], "$options": "i"}},
                ],
        "locations": {
            "$regex": entities["location"],
            "$options": "i"
        }
    }
    results = list(collection.find(query, {"date":1, "title": 1, "text":1, "article_links": 1, "scraped_from": 1}))
    return results


def search_articles_on_web(entities: dict):
    '''
    This function searches articles on web google news using SerpAPI based on entities
    Args:
        entities (dict)
    Returns:
        list of data for the given entities searched from Google News
    '''
    #Using SerpAPI to get links
    disease = entities["disease"]
    location = entities["location"]
    url = f"https://serpapi.com/search.json?engine=google_news&q={disease}+in+{location}&gl=in&hl=en&api_key={SERP_API_KEY}"
    results = requests.get(url)
    #search = serpapi.GoogleSearch(params)
    #results = search.get_dict()
    results = results.json()
    news_results = results["news_results"]

    #Using Newspaper 3K to get text
    all_articles = []
    for i in range(0, len(news_results)):
        try:
            a = Article(news_results[i]["link"])
            a.download()
            a.parse()
            text = a.text
            date = convert_iso_date_into_ddmmyyyy(news_results[i]["date"])
            article = {
                "date": date,
                "title": news_results[i]["title"],
                "text": text,
                "scraped_from": news_results[i]["source"]["name"],
                "article_links": news_results[i]["link"],
            }
            all_articles.append(article)
        except Exception as e:
            logging.error(f"Error in article: {i}: {e}")
            continue

    logging.info(f"Total articles: {len(all_articles)}")

    #once again filtering articles to get relevant results
    filtered_articles = [
        article for article in all_articles
        if entities["disease"].lower() in article["text"].lower()
        and entities["location"].lower() in article["text"].lower()
        ]
    logging.info(f"Filtered articles: {len(filtered_articles)}")

    return filtered_articles


def get_articles_for_assessment(entities: dict, min_required: int = 5) ->List[dict]:
    '''
    This function combines the above two functions.
    only sreaches Google News if less than min_required articles are found in database
    Args:
        entities (dict), min_required (int)
    Returns:
        list of data for the given entities from database as well as Google News
    '''
    logging.info(f"Searching database for {entities}...")
    database_articles = search_articles_in_database(entities)
    logging.info(f"Found {len(database_articles)} in database")

    if len(database_articles) >= min_required:
        return database_articles

    logging.info(f"Not enough data in database. Searching web...")
    web_articles = search_articles_on_web(entities)
    logging.info(f"Found {len(web_articles)} on web")

    combined = database_articles + web_articles
    return combined
