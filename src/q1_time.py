import ujson as json
from collections import Counter, defaultdict
from datetime import datetime
from typing import List, Tuple
import heapq
import multiprocessing as mp

def process_line(line):
    try:
        tweet = json.loads(line)
        date = datetime.fromisoformat(tweet['date'].replace('Z', '+00:00')).date()
        username = tweet['user']['username']
        return date, username
    except (KeyError, ValueError, json.JSONDecodeError):
        return None, None

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    num_processes = mp.cpu_count() # Obtiene el número de núcleos de CPU disponibles
    
    # Procesamiento paralelo para acelerar la extracción de emojis
    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(process_line, lines)

    date_tweet_counts = Counter()
    date_user_counts = defaultdict(Counter)

    for date, username in results:
        if date and username:
            date_tweet_counts[date] += 1
            date_user_counts[date][username] += 1

    # Obtener las 10 fechas con más tweets
    top_10_dates = heapq.nlargest(10, date_tweet_counts.items(), key=lambda x: x[1])

    result = [(date, max(date_user_counts[date], key=date_user_counts[date].get)) for _, date in top_10_dates]

    return result