import ujson
from collections import defaultdict
from datetime import datetime
from typing import List, Tuple
import heapq

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_tweet_counts = defaultdict(int)
    date_user_counts = defaultdict(lambda: defaultdict(int))
    top_dates = []

    def update_top_dates(date):
        if len(top_dates) < 10:
            heapq.heappush(top_dates, (date_tweet_counts[date], date))
        elif date_tweet_counts[date] > top_dates[0][0]:
            heapq.heapreplace(top_dates, (date_tweet_counts[date], date))

    def process_line(line):
        tweet = ujson.loads(line)
        date = datetime.fromisoformat(tweet['date'].replace('Z', '+00:00')).date()
        username = tweet['user']['username']
        
        date_tweet_counts[date] += 1
        date_user_counts[date][username] += 1
        update_top_dates(date)

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            process_line(line)

    result = []
    for _, date in sorted(top_dates, reverse=True):
        top_user = max(date_user_counts[date], key=date_user_counts[date].get)
        result.append((date, top_user))
        # Liberar memoria
        del date_user_counts[date]

    # Liberar memoria
    del date_tweet_counts
    del date_user_counts

    return result