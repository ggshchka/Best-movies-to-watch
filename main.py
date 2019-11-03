import requests
from bs4 import BeautifulSoup

def parse_name_with_imdb():
    url = 'https://kinoteatr.ru/kinoafisha/'
    page = requests.get(url)
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.text, "html.parser")
    dict = {}
    for each in soup.findAll('div', {'class': 'col-md-2 col-sm-6 col-xs-12 movie_card'}):

        names = each.find('span', {'class': 'movie_card_header title'})
        imdb = each.find('span', {'class': 'movie_card_stars'})
        if imdb is not None:
            dict[names.text.strip()] = imdb.text
    return dict

def choose_movies(dict, my_imdb):
    my_dict = {}
    for key, value in dict.items():
        if float(value) >= my_imdb:
            my_dict[key] = value
    return my_dict




if __name__ == '__main__':
    print(choose_movies(parse_name_with_imdb(), 8))