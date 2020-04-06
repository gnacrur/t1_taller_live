from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def home_view(request):
    response = requests.get('https://integracion-rick-morty-api.herokuapp.com/api/episode')
    data = response.json()
    url_next = data["info"]["next"]
    while url_next != "":
        response2 = requests.get(url_next)
        data2 = response2.json()
        data["results"].extend(data2["results"])
        url_next = data2["info"]["next"]
    return render(request, "home.html", data)


def capitulo_view(request, num = 1):
    response = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/episode/{num}')
    data = response.json()
    links = data["characters"]
    characters = []
    for link in links:
        characters.append(int(link.split('/')[-1]))
    response2 = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/character/{characters}')
    data2 = response2.json()
    lista_personajes = []
    for perso in data2:
        personaje = dict()
        personaje["id"] = perso["id"]
        personaje["nombre"] = perso["name"]
        lista_personajes.append(personaje)
    data["lista_personajes"] = lista_personajes
    return render(request, "capitulo.html", data)

def personaje_view(request, num = 1):
    response = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/character/{num}')
    data = response.json()
    links = data["episode"]
    capitulos = []
    for link in links:
        capitulos.append(int(link.split('/')[-1]))
    response2 = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/episode/{capitulos}')
    data2 = response2.json()
    lista_capitulos = []
    for cap in data2:
        capitulo = dict()
        capitulo["id"] = cap["id"]
        capitulo["nombre"] = cap["name"]
        lista_capitulos.append(capitulo)
    data["lista_capitulos"] = lista_capitulos

    id_personaje = data["location"]["url"].split('/')[-1]
    data["location"]["id"]= id_personaje

    return render(request, "personaje.html", data)

def lugar_view(request, num = 1):
    response = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/location/{num}')
    data = response.json()
    links = data["residents"]
    characters = []
    for link in links:
        characters.append(int(link.split('/')[-1]))
    response2 = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/character/{characters}')
    data2 = response2.json()
    lista_personajes = []
    for perso in data2:
        personaje = dict()
        personaje["id"] = perso["id"]
        personaje["nombre"] = perso["name"]
        lista_personajes.append(personaje)
    data["lista_personajes"] = lista_personajes
    return render(request, "lugar.html", data)

def busqueda_view(request):
    if request.method == 'GET': # If the form is submitted
        search_query = request.GET.get('search_box', None)
    response_personajes = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/character/?name={search_query}')
    data_personajes = response_personajes.json()
    response_lugares = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/location/?name={search_query}')
    data_lugares = response_lugares.json()
    response_capitulos = requests.get(f'https://integracion-rick-morty-api.herokuapp.com/api/episode/?name={search_query}')
    data_capitulos = response_capitulos.json()
    data = dict()
    if "info" in data_personajes.keys():
        url_next_personajes = data_personajes["info"]["next"]
        while url_next_personajes != "":
            response2 = requests.get(url_next_personajes)
            data2 = response2.json()
            data_personajes["results"].extend(data2["results"])
            url_next_personajes = data2["info"]["next"]
        data["results_personajes"] = data_personajes["results"]

    if "info" in data_lugares.keys():
        url_next_lugares = data_lugares["info"]["next"]
        while url_next_lugares != "":
            response2 = requests.get(url_next_lugares)
            data2 = response2.json()
            data_lugares["results"].extend(data2["results"])
            url_next_lugares = data2["info"]["next"]
        data["results_lugares"] = data_lugares["results"]

    if "info" in data_capitulos.keys():
        url_next_capitulos = data_capitulos["info"]["next"]
        while url_next_capitulos != "":
            response2 = requests.get(url_next_capitulos)
            data2 = response2.json()
            data_capitulos["results"].extend(data2["results"])
            url_next_capitulos = data2["info"]["next"]
        data["results_capitulos"] = data_capitulos["results"]
    return render(request, "busqueda.html", data)
