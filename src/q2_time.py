import ujson
from collections import Counter
from typing import List, Tuple
import heapq
import regex
import multiprocessing as mp

def process_line(line):

    try:
        tweet = ujson.loads(line)  
        content = tweet.get('content', '')
        emojis = regex.findall(r'\p{Emoji_Presentation}|\p{Emoji}\uFE0F', content)
        return emojis if emojis else None  
    except (KeyError, ValueError, ujson.JSONDecodeError) as e:
        print(f"Error al procesar la línea: {str(e)}")
        return None

def process_and_combine_emojis(emoji_counts: Counter) -> Counter:
    """
    Función para procesar y combinar componentes de emojis, especialmente los que forman
    banderas, en emojis completos. También maneja otros tipos de emojis, excluyendo 
    modificadores de tono de piel.
    """
    combined = Counter()
    flag_components = {}
    try:
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
            elif emoji not in ['\U0001F3FB', '\U0001F3FC', '\U0001F3FD', '\U0001F3FE', '\U0001F3FF']: # Excluir modificadores de tono de piel
                combined[emoji] = count

        combined.update(flag_components) # Agrega cualquier componente de bandera que quedó sin combinar
    except Exception as e:
        print(f"Error al procesar y combinar emojis: {str(e)}")
    
    return combined

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    num_processes = mp.cpu_count()  # Obtiene el número de núcleos de CPU disponibles
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  

        # Procesamiento paralelo para acelerar la extracción de emojis
        with mp.Pool(processes=num_processes) as pool:
            results = pool.map(process_line, lines)

        emoji_counter = Counter()
        for emojis in results:
            if emojis:
                emoji_counter.update(emojis)  

        combined_counter = process_and_combine_emojis(emoji_counter)
        
        # Usa heapq para encontrar los 10 emojis más comunes
        top_10_emojis = heapq.nlargest(10, combined_counter.items(), key=lambda x: x[1])
        
        return top_10_emojis

    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {str(e)}")
    except IOError as e:
        print(f"Error de I/O al procesar el archivo: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
    
    return []