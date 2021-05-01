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


def initial_movie_display(movies_from_genres):
    movies = []
    titles = []
    for genre in movies_from_genres:
        for movie in movies_from_genres[genre]:
            if movie[1] not in titles:
                movies += [[genre] + movie]
                titles += [movie[1]]
    return movies

def get_names_from_movies(movies):
    movielist = []
    for m in movies:
        movielist += [m[2]]
    return movielist

def test():
    # get list of all genres
    genres = get_genres()
    # get 3 movies from each genre
    movie_genre_list = movies_from_genres(genres,3)
    # create one list of movies from those genres for display, with format [genre, ID, title]
    return initial_movie_display(movie_genre_list)
            


def default_movies_for_user(genrescore,services, multFactor):
    """takes in list of genrescore from user, users services, and a multFactor and builds up a list of possible movies that are on
        the users services. The number of movies from each genre is the multFactor * their genrescore for that genre"""
    
    movies = []
    
    for genre in genrescore:
   
        if genre[0] > 0:
            movies_in_genre = []
            i = 1
            while len(movies_in_genre) < multFactor * genre[0]:
                movie = movies_from_genres([genre[1]],i)
                actual_movie = [movie[genre[1][1]][-1]]
                if actual_movie[0] not in movies:
                    movies_in_genre += actual_movie
                i += 1
        movies += movies_in_genre
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
        data = response.json()['results']['US']['flatrate']
        services = []
        for source in data:
            services.append(source['provider_name'])
        return services
    else:
        raise Exception('TMDB API gave status code  {}'.format(response.status_code))


        


