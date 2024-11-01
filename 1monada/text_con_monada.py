#!/usr/bin/env python3

import string
from collections import Counter
from functools import reduce
import os

""" le pregunte a ChatGPT como implemetar una monada y me mostro la clase TextMonad"""
# Monada para encapsular operaciones en un texto o una lista de caracteres

class TextMonad:
    
    # definimos el contructor de la clase TextMonad 
    
    def __init__(self, value):
        
        #El valor inicial puede ser un texto o una lista de tokens
        
        self.value = value  

    # Esta funcion permite aplicar funciones secuenciales sobre ese valor, encadena operaciones
    # y maneja errores que puedan surgir
        
    def bind(self, func):
        try:
            result = func(self.value)
            
            # Retorna una nueva instancia de TextMonad con el resultado de aplicar la función
            
            return TextMonad(result) 
        
        except Exception as e:
            print(f"Error: {e}")
            
            # En caso de error, retorna un valor nulo
            
            return TextMonad(None)  

    # Obtiene y retorna el valor interno de la monada
    
    def get_value(self):
        return self.value  

# Función para leer el archivo speech.txt que se encuentra en el mismo directorio
# y lo retorna como una cadena de texto

def read_file(file_path: str) -> str:
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    # Excepcion en caso de que no se encuentre el archivo en el directorio
    except FileNotFoundError:
        print(f"Error: el archivo {file_path} no se existe.")
        return ""
    
    # Excepcion en caso de que no se pueda leer el archivo
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return ""

# Función para leer el archivo keywords.txt que se encuentra en el mismo directorio
# y retorna una lista de palabras clave

def read_keywords(file_path: str) -> list:
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            
            # El metodo .strip() elimina todos los caracteres iniciales y finales de la lista
            # El metodo .lower() los convierte a minusculas
            # El metodo .readline lee cada linea del archivo y la regresa en la lista
            keywords = [line.strip().lower() for line in file.readlines()]
            return keywords
    
    # Excepcion en caso de que no se encuentre el archivo en el directorio
    except FileNotFoundError:
        print(f"Error: el archivo {file_path} no se encontró.")
        return []
    
    # Excepcion en caso de que no se pueda leer el archivo
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

# Función para tokenizar el texto

def tokenize(text: str) -> list:
    
    # El metodo .maketrans() convierte un texto en una lista de tokens (palabras)
    # El metodo string.punctation elimina los signos de puntuación
    # El metodo .lower() convierte la cadena de caracteres a minúsculas.
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    
    #El metodo .split() divide la cadena de caracteres
    tokens = text.split()
    return tokens

# Función para contar las palabras clave filtrando los tokens del texto analizado
# Para conservar solo las palabras que están en la lista de palabras clave del archivo keywords.txt

def count_keywords(tokens: list, keywords: list) -> Counter:
    
    #filter (HOF) funcion de alto orden para filtrar las palabras clave 
    filtered_tokens = filter(lambda word: word in keywords, tokens)
    
    #Funcion Counter() para almacenar la cantidad de veces que se repiten
    return Counter(filtered_tokens)

# Función para calcular el promedio del largo de las palabras del archivo speech.txt

def avg_word_length(tokens: list) -> float:
    
    #reduce() (HOF) funcion de alto orden para almacenar el largo de cada palabra
    total_length = reduce(lambda total, word: total + len(word), tokens, 0)
    return total_length / len(tokens) if tokens else 0

# Función que encuentra las 10 palabras más comunes asi como la frecuencia con que se repiten

def most_common_words(frequency: Counter, num_words: int = 10) -> list:
        
    #Retorna las palabras más comunes y su frecuencia
    return frequency.most_common(num_words)

# Función que devuelve las 50 palabras más repetidas en el archivo speech.txt

def top_50_words(frequency: Counter) -> list:
    
    # sorted() (HOF) funcion de alto orden con el parametro key=len, que ordenar las palabras 
    # primero por longitud (descendente) y luego por frecuencia (descendente)
    sorted_by_length_and_frequency = sorted(frequency.items(), key=lambda x: (len(x[0]), x[1]), reverse=True)
    
    #Retorna las 50 primeras palabras mas repetidas dentro del archivo speech.txt
    return sorted_by_length_and_frequency[:50]

# Función principal para analizar el texto y mostrar resultados basados en las palabras clave

def analyze_text(text: str, keywords: list) -> None:
        
    # se encapsula el procesamiento del texto en la monada
    monad = TextMonad(text)

    # Tokenizamos el texto y se obtiene el valor resultante
    tokens = (monad.bind(tokenize)    
                   .get_value())      

    # Se cuentan las palabras clave
    keyword_counts = count_keywords(tokens, keywords)  
    
    # Se calcula el largo promedio de las palabras
    word_length = avg_word_length(tokens)  
    
    # Se encuentran las palabras más comunes
    common_words = most_common_words(keyword_counts)  
    
    #Se imprimen los resultados:
    print(f"Total de palabras: {len(tokens)}")
    print(f"Promedio de largo de las palabras: {word_length:.2f}")
    print("Palabras clave más comunes: ")
    for word, freq in common_words:
        print(f"   {word}: {freq}")
    
    # Se Llama a la función top_50_words para mostrar las 50 palabras más repetidas
    top_words = top_50_words(Counter(tokens))
    
    # Se imprimen la 50 palabras mas repetidas
    print("\nLas 50 palabras más repetidas del archivo son:")
    for word, freq in top_words:
        print(f"   {word}: {freq} veces, {len(word)} caracteres")

# Punto de entrada del programa.

if __name__ == '__main__':
    
    # Se solicita al usuario el nombre del archivo de texto a analizar
    file_path = input("Introduce el nombre o la ruta del archivo de texto a analizar:\n ")
    
    # Se solicita al usuario el nombre del archivo de texto con las palabras clave.
    keywords_file = input("Introduce el nombre o la ruta del archivo de texto de palabras clave:\n ")

    # os.path.isfile() verifica si ambos archivos existen
    if os.path.isfile(file_path) and os.path.isfile(keywords_file):
        
        # Lee el archivo de texto principal
        sample_text = read_file(file_path)
        
        # Lee el archivo de palabras clave
        keywords = read_keywords(keywords_file)
        
        if not keywords:
            print("El archivo de palabras clave está vacío o no se encontraron palabras clave.")
        
        else:
            
            # Analizar el contenido del archivo con las palabras clave
            analyze_text(sample_text, keywords)
    else:
        print("Uno o ambos archivos no existen. Verifica las rutas e intenta de nuevo.")
