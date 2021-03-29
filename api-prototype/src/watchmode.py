import requests
import json
from  secrets import SECRETS

watchmode_api_key = SECRETS['watchmode_api_key']


def watchmodeID_from_imdbID(imdbID):
    """
    Takes in imdbID as string, returns watchmode ID as string
    """
    response = requests.get("https://api.watchmode.com/v1/search/?apiKey=" + watchmode_api_key + "&search_field=imdb_id&search_value=" + imdbID)

    if response.status_code == 200:
        data = response.json()
        if len(data.get('title_results')) > 0:
            return str((data.get('title_results')[0].get('id')))
        else:
            return "Not found in Watchmode database"
    else:
        raise Exception('Watchmode API gave status code {}'.format(response.status_code))

def sources_from_watchmodeID(watchmodeID):
    """
    Takes in imdbID as string, returns dictionary of sources (source_id, type, region, ios_url, android_url, web_url, format, price, seasons, episodes)
    """
    response = requests.get("https://api.watchmode.com/v1/title/" + watchmodeID + "/sources/?apiKey=" + watchmode_api_key)

    if response.status_code == 200:
        data = response.json()
        services = []
        for source in data:
            # can change web_url to any of the parameters in the doc string
            services.append(source['web_url'])
        return services
    else:
        raise Exception('Watchmode API gave status code  {}'.format(response.status_code))

def known_sources(watchmodeSources):
    sources = []
    for source in watchmodeSources:
        if 'netflix' in source and 'Netflix' not in sources:
            sources.append('Netflix')
        elif 'amazon' in source and 'Amazon' not in sources:
            sources.append('Amazon')
        elif 'hulu' in source and 'Hulu' not in sources:
            sources.append('Hulu')
    return sources
        


