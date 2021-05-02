import requests
import json
from  secrets import SECRETS

watchmode_api_key = SECRETS['watchmode_api_key']
TMDB_api_key = SECRETS['TMDB_api_key']


def get_genres():
    """ Finds genres on themoviedb api"""
    response = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=" + TMDB_api_key + "&language=en-US")
    
    if response.status_code == 200:
        data = response.json()
        genres = []
        for genre in data['genres']:
            genres += [[str(genre.get("id")), genre.get('name')]]
        return genres
    else:
        raise Exception('TMDB API gave status code {}'.format(response.status_code))

def movies_from_genres(genres,num):
    """Returns num movies from each listed genre"""
    movies = {}
    for genre in genres:
        
        if genre[0] != 'None':
            response = requests.get("https://api.themoviedb.org/3/genre/" + genre[0] + '/movies?api_key=' + TMDB_api_key)
            
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
    genrescore = {}
    for genre in genres:
       genrescore[genre[0]] = 0.05 
    services = []
    num_movies = 30
    watched_movies = []
    return default_movies_for_user(genrescore,services, num_movies, watched_movies)


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
            


def default_movies_for_user(genrescore,services, num_movies, watched_movies):
    """takes in list of genrescore from user, users services, and a multFactor and builds up a list of possible movies that are on
        the users services. The number of movies from each genre is the multFactor * their genrescore for that genre"""
    
    movies = {}

    
    for genre in genrescore:
        genrescore[genre] = int((genrescore[genre] * num_movies) // 1)

        moviessofar =  0
        services_string = ','.join(services)
        watchprovidersstring = "&with_watch_providers=" + services_string + "&watch_region=US"
        if services == []:
            watchprovidersstring = ''
        page = 1
        while moviessofar < genrescore[genre]:
            response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + TMDB_api_key +
                                    "&language=en-US&region=US&sort_by=popularity.desc&include_adult=false&include_video=false&page=" + str(page) + "&with_genres=" +
                                    genre + watchprovidersstring + "&with_watch_monetization_types=flatrate")
            data = response.json()['results']

            for result in data:
                if result['title'] not in movies and result['title'] not in watched_movies and moviessofar < genrescore[genre]:
                    movie = {}
                    movie['id'] = result['id']
                    movie['genre_ids'] = result['genre_ids']
                    sources = sources_from_tmdbID(movie['id'])
                    if sources != 'None':
                        sources_with_service = [sources[x] for x in sources if str(sources[x]) in services] 
                        movie['source'] = sources_with_service
                        movies[result['title']] = movie
                        moviessofar += 1
            page += 1
            
            
    return movies


def tmdbID_from_imdbID(imdbID):
    """
    Takes in imdbID as string, returns TMDB ID as string
    """
    response = requests.get("https://api.themoviedb.org/3/find/" + imdbID + "?api_key=" + TMDB_api_key + '&language=en-US&external_source=imdb_id')

    if response.status_code == 200:
        data = response.json()
        if len(data.get('movie_results')) > 0:
            return str((data.get('movie_results')[0].get('id')))
        else:
            return "Not found in That Movie database"
    else:
        raise Exception('TMDB API gave status code {}'.format(response.status_code))

def sources_from_tmdbID(tmdbID):
    """
    Takes in tmdbID as string, returns dictionary of sources 
    """
    response = requests.get("https://api.themoviedb.org/3/movie/" + str(tmdbID) + '/watch/providers?api_key=' + TMDB_api_key)

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
        raise Exception('TMDB API gave status code  {}'.format(response.status_code))


        


