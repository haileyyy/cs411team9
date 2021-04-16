import requests
from secrets import SECRETS

imdb_api_key = SECRETS['imdb_api_key']
base_url = 'https://imdb-api.com/en/API/SearchTitle/{}/'.format(imdb_api_key)

def get_imdb_movie(movie_name):
  response = requests.get(base_url + movie_name)
  
  if response.status_code == 200:
    data = response.json()

    movies = []
    for movie in data['results']:
      movies.append({
        'title': movie['title'],
        'description': movie['description'],
        'id': movie['id']
      })

    return movies

  else:
    raise Exception('IMDB API gave status code {}'.format(response.status_code))
