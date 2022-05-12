# import os
# import json
import requests
from bs4 import BeautifulSoup
import re

""" Obtiene una url y extrae los audios y los texto de las etiquetas que creemos que contienen los audios
    Crea un archivo Json a partir de esto
"""


def get_tranlate(term, from_lg, to_lg ):    

    traduccion = ".Q4iAWc"
    sinonimos = ".Dwvecf"


    get_tags = 'i, b , audio'
    # leer cualquier web
    website = f'https://translate.google.com/?sl={from_lg}&tl={to_lg}&text={term}&op=translate'
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    # tags = soup.select('#result_box span')
    print(soup.select(get_tags))
    print(website)

    # # Obtenemos los audios y los textos en una lista
    # """ Extre las etiquetas que creemos que tiene el contenido importante"""
    # get_data = re.compile(r'(?<=src=").*?(?=")|(?<=>").*?(?="<)')
    # """ extrae la url de las etiquetas y el texto de una etiqueta"""
    # resultado = get_data.findall(str(tags))

    # # Agregamos los textos y audios a un dict
    # lista = []
    # objeto = {
    #     "url": False
    # }
    # for i in resultado:
    #     """ si es una url agrega 1 elemento a un dic luego agrega ese dict a la lista"""
    #     if i.startswith("http") == True:
    #         if objeto["url"]:
    #             pass
    #         else:
    #             objeto["url"] = i
    #     else:
    #         if i.endswith(".ogg") == True:
    #             pass
    #         else:
    #             objeto["text"] = i
    #             lista.insert(len(lista), objeto)
    #             objeto.clear
    #             objeto = {"url": False}
