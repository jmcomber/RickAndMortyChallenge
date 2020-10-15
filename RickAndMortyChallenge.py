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

    def _getCounts(self, letter, results):
        count = 0
        for result in results:
            count += result['name'].lower().count(letter)
        return count

    def _letterCounterInResource(self, letter, resource):
        responseDict = self._redundantGetter(self._baseURL + resource)
        count = self._getCounts(letter, responseDict['results'])
        while responseDict['info']['next'] is not None:
            responseDict = self._redundantGetter(responseDict['info']['next'])
            count += self._getCounts(letter, responseDict['results'])
            print('count ', count)
        return count

    def countCharsQueried(self, queries):
        start = time.time()
        for letter, resource in queries:
            count = self._letterCounterInResource(letter, resource)
            print(f'Letter {letter} in resource {resource} was found {count} times')
        end = time.time()
        print(f'Time elapsed: {round(end - start, 2)} seconds')

    def getLocationsFromEpisodes(self):
        episodes = self._redundantGetter(self._baseURL + 'episode')['results']
        print(len(episodes), episodes[0])


if __name__ == '__main__':
    rickAndMortyConsumer = RickAndMortyConsumer()
    rickAndMortyConsumer.countCharsQueried([['l', 'location'],
                                            ['e', 'episode'],
                                            ['c', 'character']])
    
    # rickAndMortyConsumer.getLocationsFromEpisodes()