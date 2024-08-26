import ujson as json
from collections import Counter
from typing import List, Tuple
import heapq

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    mention_counter = Counter()
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                tweet = json.loads(line)
                mentioned_users = tweet.get('mentionedUsers', [])
                
                if mentioned_users is None:  # Manejar el caso en el que mentionedUsers sea None
                    mentioned_users = []
                
                # Actualiza el contador de menciones directamente
                for user in mentioned_users:
                    mention_counter[user['username']] += 1
            
            except (KeyError, ValueError, json.JSONDecodeError) as e:
                print(f"Error al procesar la línea: {str(e)}")
    
    # Usa heapq para encontrar los 10 usuarios más mencionados
    top_10_users = heapq.nlargest(10, mention_counter.items(), key=lambda x: x[1])

    return top_10_users