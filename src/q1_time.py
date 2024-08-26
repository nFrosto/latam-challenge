import ujson
from collections import Counter
from datetime import datetime
from typing import List, Tuple
import heapq
import multiprocessing as mp

def process_line(line):
    try:
        tweet = ujson.loads(line)
        date = datetime.fromisoformat(tweet['date'].replace('Z', '+00:00')).date()
        username = tweet['user']['username']
        return date, username
    except (KeyError, ValueError, ujson.JSONDecodeError):
        return None, None

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    num_processes = mp.cpu_count()
    
    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(process_line, lines)

    date_tweet_counts = Counter()
    date_user_counts = {}

    for date, username in results:
        if date and username:
            date_tweet_counts[date] += 1
            if date not in date_user_counts:
                date_user_counts[date] = Counter()
            date_user_counts[date][username] += 1

    top_10_dates = heapq.nlargest(10, date_tweet_counts.items(), key=lambda x: x[1])

    result = []
    for date, _ in top_10_dates:
        top_user = date_user_counts[date].most_common(1)[0][0]
        result.append((date, top_user))

    return result