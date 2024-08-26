import ujson as json
from collections import Counter
from typing import List, Tuple
import multiprocessing as mp
import heapq

def process_line_time(line):
    try:
        tweet = json.loads(line)
        mentioned_users = tweet.get('mentionedUsers', [])
        if mentioned_users is None:  # Manejar el caso en el que mentionedUsers sea None
            mentioned_users = []
        return [user['username'] for user in mentioned_users]
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Error al procesar la línea: {str(e)}")

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    num_processes = mp.cpu_count()  # Usa todos los núcleos disponibles
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Procesamiento paralelo para extraer menciones de usuarios
    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(process_line_time, lines)

    mention_counter = Counter()

    # Actualiza el contador de menciones con los resultados
    for mentioned_users in results:
        if mentioned_users:
            mention_counter.update(mentioned_users)
    
    # Usa heapq para encontrar los 10 usuarios más mencionados
    top_10_users = heapq.nlargest(10, mention_counter.items(), key=lambda x: x[1])

    return top_10_users