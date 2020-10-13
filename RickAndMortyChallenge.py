'''
Author: 
Date: 
...
'''

from functools import reduce
import time
import requests


class RickAndMortyConsumer:
    
    def __init__(self):
        self._baseURL = 'https://rickandmortyapi.com/api/'

    def _redundantGetter(self, url):
        correctRequest = False
        counter = 0
        while not correctRequest:
            resp = requests.get(url)
            if resp.status_code < 300:
                return resp.json()
            if counter == 10:
                raise Exception('There seems to be a problem with the API')
            counter += 1

    def letterCounterInResource(self, letter, resource):
        responseDict = self._redundantGetter(self._baseURL + resource)
        count = reduce(lambda a, b: (a['name'].count(letter) if isinstance(a, dict) else a) + (b['name'].count(letter) if isinstance(b, dict) else b), responseDict['results'])
        return count

if __name__ == '__main__':
    rickAndMortyConsumer = RickAndMortyConsumer()
    print(rickAndMortyConsumer.letterCounterInResource('l', 'location'))
