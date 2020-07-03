import requests
import datetime
import os
from pocket import Pocket

def get_best_daily_stories():
    top_stories = []

    stories = requests.get('https://hacker-news.firebaseio.com/v0/beststories.json').json()

    for story in stories:
        item = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story}.json').json()
        item_date = datetime.datetime.fromtimestamp(item.get('time'))

        yesterday = datetime.datetime.today() - datetime.timedelta(1)

        if item_date.date() == yesterday.date():
            top_stories.append(item)

    return top_stories[:10]

def send_stories_to_pocket():
    stories = get_best_daily_stories()

    consumer_key = os.getenv('CONSUMER_KEY')
    access_token = os.getenv('ACCESS_TOKEN')

    pocket = Pocket(consumer_key, access_token)

    for story in stories:
        url = story.get('url')
        title = story.get('title')
        print(f'{title} - {url}')

        try:
            pocket.add(url, tags='hacker-news-app')
        except Exception:
            pass

if __name__ == '__main__':
    send_stories_to_pocket()
