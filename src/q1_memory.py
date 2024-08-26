import ujson as json
from collections import defaultdict, Counter
from datetime import datetime
from typing import List, Tuple
import heapq

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_tweet_counts = Counter()  # Contador de tweets por fecha
    date_user_counts = defaultdict(Counter)  # Contador de tweets por usuario por fecha

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                tweet = json.loads(line)
                date = datetime.fromisoformat(tweet['date'].replace('Z', '+00:00')).date()
                username = tweet['user']['username']
                
                date_tweet_counts[date] += 1
                date_user_counts[date][username] += 1
            except (KeyError, ValueError, json.JSONDecodeError) as e:
                print(f"Error al procesar la línea: {str(e)}")
    
    # Obtener las 10 fechas con más tweets
    top_10_dates = heapq.nlargest(10, date_tweet_counts.items(), key=lambda x: x[1])

    result = [(date, max(date_user_counts[date], key=date_user_counts[date].get)) for _, date in top_10_dates]
    
    return result