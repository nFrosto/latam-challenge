import ujson as json
from collections import Counter
from typing import List, Tuple
import regex
import heapq


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    def emoji_process(emoji_counts: Counter) -> Counter:

        """
        Función para procesar y combinar componentes de emojis, especialmente los que forman
        banderas, en emojis completos. También maneja otros tipos de emojis, excluyendo 
        modificadores de tono de piel.
        """

        combined = Counter()
        flag_components = {}
        for emoji, count in emoji_counts.items():
             # Detecta y combina los componentes individuales de las banderas (letras de país)
            if len(emoji) == 1 and '\U0001F1E6' <= emoji <= '\U0001F1FF':
                if flag_components:
                    prev_emoji = list(flag_components.keys())[0]
                    combined_emoji = prev_emoji + emoji
                     # Combina los componentes en un solo emoji de bandera
                    combined[combined_emoji] = min(count, emoji_counts[prev_emoji])
                    flag_components.clear()
                else:
                    flag_components[emoji] = count
            elif emoji not in ['\U0001F3FB', '\U0001F3FC', '\U0001F3FD', '\U0001F3FE', '\U0001F3FF']:  # Excluir modificadores de tono de piel
                combined[emoji] = count

        combined.update(flag_components) # Agrega cualquier componente de bandera que quedó sin combinar
        
        return combined

    emoji_counter = Counter()
    emoji_pattern = regex.compile(r'\p{Emoji_Presentation}|\p{Emoji}\uFE0F')
    heap = []
    tweets_processed = 0
    tweets_with_emojis = 0
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                tweet = json.loads(line)
                content = tweet.get('content', '')
                
                if not content:
                    continue
                
                emojis = emoji_pattern.findall(content)
                
                if emojis:
                    tweets_with_emojis += 1
                    for emoji in emojis:
                        emoji_counter[emoji] += 1
                        
                        # Actualizar el heap para mantener solo el top 10 emojis
                        if len(heap) < 10:
                            heapq.heappush(heap, (emoji_counter[emoji], emoji))
                        else:
                            heapq.heappushpop(heap, (emoji_counter[emoji], emoji))
            
            except json.JSONDecodeError:
                print(f"Error al decodificar JSON en la línea {tweets_processed}")
            except Exception as e:
                print(f"Error inesperado en la línea {tweets_processed}: {str(e)}")
    
    combined_counter = emoji_process(emoji_counter)
    
    # Obtener los top 10 emojis más frecuentes desde el heap
    top_10_emojis = heapq.nlargest(10, combined_counter.items(), key=lambda x: x[1])
    
    return top_10_emojis