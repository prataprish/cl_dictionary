import requests
import auth
import json


def fetch(word):

    lang = 'en'
    url_meaning = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + lang + '/' + word.lower()
    url_syn = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + lang + '/' + word.lower() + '/synonyms'
    headers = {
        'app_id':auth.app_id,
        'app_key':auth.app_key
    }

    result_meaning = requests.get(url_meaning, headers = headers)
    result_syn = requests.get(url_syn, headers = headers)

    meaning = None
    synonyms = None

    if result_meaning.status_code == 200:
        result = result_meaning.json()
        result = result['results'][0]
        result = result['lexicalEntries'][0]
        result = result['entries'][0]
        result = result['senses'][0]
        meaning = result['definitions'][0]
    else:
        print("No Match Found!!!")
        return

    if result_syn.status_code == 200:
        result = result_syn.json()
        result = result['results'][0]
        result = result['lexicalEntries'][0]
        result = result['entries'][0]
        result = result['senses'][0]
        synonyms = [synonym['id'] for synonym in result['synonyms']]

    return {'meaning':meaning,'synonyms':synonyms}
