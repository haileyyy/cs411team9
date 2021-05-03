import requests
import json
import math
import random
from  secrets import SECRETS

watchmode_api_key = SECRETS['watchmode_api_key']
tmdb_api_key = SECRETS['tmdb_api_key']


def movie_from_id(movieid):
    response = requests.get("https://api.themoviedb.org/3/movie/" + str(movieid) + "?api_key=" + tmdb_api_key + "&language=en-US")
    if response.status_code == 200:
        data = response.json()
        movie = {}
        movie['id'] = str(movieid)
        genres = data['genres']
        list_genres = []
        for genre in genres:
            list_genres.append(genre['id'])
        movie['genre_ids'] = list_genres
        movie['title'] = data['title']
        movie['image'] = 'https://image.tmdb.org/t/p/w500' + data['poster_path']
        sources = sources_from_tmdbID(movieid)
        list_sources = []
        for source in sources:
            list_sources.append(str(sources[source]))
        movie['source'] = list_sources
        return movie
    else:
        return 'No movie found'

def clean_genres(genrelist):
    genrescores = {}
    for genreinput in genrelist:
        genreinput = genreinput.replace('[','')
        genreinput = genreinput.replace(']','')
        genreinput = genreinput.replace(' ','')
        genreinput = genreinput.split(',')
        for genre in genreinput:
            if genre not in genrescores:
                genrescores[genre] = 1
            else:
                genrescores[genre] += 1
    return genrescores

def update_userscores(userscore, genrescores):
    for genre in genrescores:
        for x in range(genrescores[genre]):
            userscore[genre] += 1
    return userscore


def get_genres():
    """ Finds genres on themoviedb api"""
    response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=" + tmdb_api_key + "&language=en-US")
    
    if response.status_code == 200:
        data = response.json()
        genres = []
        for genre in data['genres']:
            genres += [[str(genre.get("id")), genre.get('name')]]
        return genres
    else:
        raise Exception('tmdb API gave status code {}'.format(response.status_code))

def movies_from_genres(genres,num):
    """Returns num movies from each listed genre"""
    movies = {}
    for genre in genres:
        
        if genre[0] != 'None':
            response = requests.get("https://api.themoviedb.org/3/genre/" + genre[0] + '/movies?api_key=' + tmdb_api_key)
            
            if response.status_code == 200:
                data = response.json()['results']
                for i in range(num):
                    if i == 0:
                        movies[genre[1]] = [[data[i]['id'],data[i]['title']]]
                    else:
                        movies[genre[1]] += [[data[i]['id'],data[i]['title']]]
    return movies


def initial_movie_display():
    genres = get_genres()
    userscore = {}
    for genre in genres:
       userscore[genre[0]] = 5
    services = []
    num_movies = 30
    watched_movies = []
    return default_movies_for_user(userscore,services, num_movies, watched_movies)


def get_names_from_movies(movies):
    movielist = []
    for m in movies:
        movielist += [m[2]]
    return movielist

def test():
    gscore ={}
    gscore['28'] = 0.2
    services = ['384']
    watched_movies = ['Iron man']
    gscore['12'] = 0.5
    print(default_movies_for_user(gscore,services,10,watched_movies))
            


def default_movies_for_user(userscore, services, num_movies, watched_movies):
    """takes in list of genrescore from user, users services, and a multFactor and builds up a list of possible movies that are on
        the users services. The number of movies from each genre is the multFactor * their genrescore for that genre"""
    
    movies = []
    alreadyseen = []
    total = 0
    genrescore = userscore.copy()
    for genre in genrescore:
        total += genrescore[genre]

    for genre in genrescore:
        genrescore[genre] = genrescore[genre] / total

    for genre in genrescore:
        genrescore[genre] = math.ceil(genrescore[genre] * num_movies)

        moviessofar =  0
        services_string = ','.join(services)
        watchprovidersstring = "&with_watch_providers=" + services_string + "&watch_region=US"
        if services == []:
            watchprovidersstring = ''
        page = 1
        while moviessofar < genrescore[genre]:
            
            response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + tmdb_api_key +
                                    "&language=en-US&region=US&sort_by=popularity.desc&include_adult=false&include_video=false&page=" + str(page) + "&with_genres=" +
                                    genre + watchprovidersstring + "&with_watch_monetization_types=flatrate")
            data = response.json()['results']
            for result in data:
                if result['title'] not in alreadyseen and result['id'] not in watched_movies and moviessofar < genrescore[genre]:
                    movie = {}
                    movie['id'] = result['id']
                    movie['title'] = result['title']
                    movie['genre_ids'] = result['genre_ids']
                    movie['image'] = 'https://image.tmdb.org/t/p/w500' + result['poster_path']
                    sources = sources_from_tmdbID(movie['id'])
                    if sources != 'None':
                        sources_with_service = [sources[x] for x in sources if str(sources[x]) in services] 
                        movie['source'] = sources_with_service
                        movies.append(movie)
                        alreadyseen.append(result['title'])
                        moviessofar += 1
            page += 1

    random.shuffle(movies)
    if len(movies) - num_movies > 0:
        return movies[:-(len(movies) - num_movies)]
    return movies


def tmdbID_from_imdbID(imdbID):
    """
    Takes in imdbID as string, returns tmdb ID as string
    """
    response = requests.get("https://api.themoviedb.org/3/find/" + imdbID + "?api_key=" + tmdb_api_key + '&language=en-US&external_source=imdb_id')

    if response.status_code == 200:
        data = response.json()
        if len(data.get('movie_results')) > 0:
            return str((data.get('movie_results')[0].get('id')))
        else:
            return "Not found in That Movie database"
    else:
        raise Exception('tmdb API gave status code {}'.format(response.status_code))

def sources_from_tmdbID(tmdbID):
    """
    Takes in tmdbID as string, returns dictionary of sources 
    """
    response = requests.get("https://api.themoviedb.org/3/movie/" + str(tmdbID) + '/watch/providers?api_key=' + tmdb_api_key)

    if response.status_code == 200:
        data = response.json()
        if 'US' not in data['results']:
            return "None"
        if 'flatrate' not in data['results']['US']:
            return "None"
        if data['results']['US']['flatrate'] == {}:
            return "None"
        data = data['results']['US']['flatrate']
        services = {}
        for source in data:
            services[source['provider_name']] = source['provider_id']
        return services
    else:
        raise Exception('tmdb API gave status code  {}'.format(response.status_code))


        


