# your_app/tasks.py

from datetime import datetime, timedelta
from celery import shared_task
import requests
import traceback
from decouple import config
import json
import hashlib
from news.models import News
from country.models import Country
import math
import logging
import celery.signals


@celery.signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass


logger = logging.getLogger("celery.task")


@shared_task()
def get_today_top_headlines():
    countries = Country.objects.all()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=15)
    for country in countries:
        while start_date != end_date:
            get_news(country,start_date)
            start_date = start_date + timedelta(days=1)        


def get_news(country,  current_date=None, max_page_no=None, page=1):
    try:
        SECRET_API_KEY = config('SECRET_API_KEY', default=None)
        if SECRET_API_KEY:
            if current_date is None:
                end_date = datetime.now()
            if max_page_no is None or page <= max_page_no:
                # current_date = datetime.now().strftime("%Y-%m-%d")
                print(f"start date {current_date} end_date {current_date}")
                logger.info(f"start date {current_date} end_date {current_date}")
                start_date_string = current_date.strftime("%Y-%m-%d")
                end_date_string = current_date.strftime("%Y-%m-%d")
                news_url = f"https://newsapi.org/v2/top-headlines?country={country.country_code}&from={start_date_string}&to={end_date_string}&sortBy=publishedAt&apiKey={SECRET_API_KEY}&page={page}"
                response = requests.get(news_url)
                if response.status_code == 200:
                    logger.info(
                        f"api called successed  response status code is {str(response.status_code)}: response:{response.text}")
                    if response.text:
                        news_json = json.loads(response.text)
                        get_articles = news_json.get("articles", [])
                        for get_article in get_articles:
                            data = {
                                "title": get_article.get("title", None),
                                "description": get_article.get("description", None),
                                "publisher_date": get_article.get("publishedAt", None),
                                "content": get_article.get("content", None),
                                "news_url": get_article.get("url", None),
                                "image_url": get_article.get("urlToImage", None),
                                "author": get_article.get("author", None),
                                "country": country
                            }
                            combined_string = data["title"] + \
                                data["publisher_date"]
                            sha256_hash = hashlib.sha256()
                            sha256_hash.update(combined_string.encode('utf-8'))
                            hash_value = sha256_hash.hexdigest()
                            is_old_news = News.objects.filter(
                                hashvalue=hash_value).first()
                            if not is_old_news:
                                logger.info(
                                    f"old news not found {str(get_article)}")
                                article = News.objects.create(**data)
                                logger.info(
                                    f"article created successfully {str(article.__dict__)}")
                        if page == 1:
                            totalresults = news_json.get("totalResults", None)
                            logger.info(f"total news are str({totalresults}")
                            if totalresults and totalresults > 20:
                                max_page_no = math.ceil(totalresults / 20)
                        if max_page_no and max_page_no > page:
                            print(
                                f"curent page is {page} and max_page_no are {max_page_no}")
                            page += 1
                            get_news(country, current_date, max_page_no, page)

                else:
                    logger.info(
                        f"api called failed  response status code is {str(response.status_code)}: response:{response.text}")

    except Exception as e:
        print(str(e), traceback.format_stack())
        logger.error(
            f"errorr occured while get news from news api", exc_info=True)
