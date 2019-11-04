import requests
from bs4 import BeautifulSoup

def parse_name_with_imdb():
    url = 'https://kinoteatr.ru/kinoafisha/'
    page = requests.get(url)
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.text, "html.parser")
    #print(soup.find_all('a', {'class': 'movie_card_clickable_zone gtm-ec-list-item-movie'}))
    dict = {}
    for each in soup.findAll('div', {'class': 'col-md-2 col-sm-6 col-xs-12 movie_card'}):
        names = each.find('span', {'class': 'movie_card_header title'})
        imdb = each.find('span', {'class': 'movie_card_stars'})
        if imdb is not None:
            dict[names.text.strip()] = float(imdb.text)
    return dict

def choose_movies(dict, my_imdb):
    my_dict = {}
    for key, value in dict.items():
        if value >= my_imdb:
            my_dict[key] = value
    return my_dict

def choose_best_movie(dict):
    max_imdb = max(zip(dict.values(), dict.keys()))
    return max_imdb[1]

class My_cinema(object):
    def __init__(self, name, address, seances):
        self.name = name
        self.address = address
        self.seances = seances


def parse_cinema(name_of_film):
    url = 'https://kinoteatr.ru/kinoafisha/'
    page = requests.get(url)
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.text, "html.parser")
    t = soup.find(attrs={'data-gtm-ec-name': name_of_film}, href=True)
    link = t.attrs['href']
    my_page = requests.get(link)
    my_soup = BeautifulSoup(my_page.text, "html.parser")

    my_cinemas = []
    for each in my_soup.findAll('div', {'class': 'cinema'}):
        name_of_cinema = each.find('div', {'class': 'name'}).text.strip()
        address_of_cinema = each.find('p', {'class': 'text'}).text.strip()
        sncs = []
        for tmp in each.findAll('div', {'class': 'item buy_seance'}):
            snc = []
            time = tmp.find('div', {'class': 'time'}).text.strip().split()[0]
            price = tmp.find('p', {'class': 'price'}).text.strip()
            snc.append(time)
            snc.append(price)
            sncs.append(snc)
        my_cinemas.append(My_cinema(name_of_cinema, address_of_cinema, sncs))
    return my_cinemas


if __name__ == '__main__':
    for i in parse_cinema(choose_best_movie(parse_name_with_imdb())):
        print(i.name)
        print(i.address)
        print(i.seances)