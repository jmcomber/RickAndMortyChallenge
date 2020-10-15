'''
Author: 
Date: 
...
'''

from collections import defaultdict
import time
import re
import requests


class RickAndMortyConsumer:
    
    def __init__(self):
        self._baseURL = 'https://rickandmortyapi.com/api/'
        self._chars = None

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
    
    def _getPaginatedResults(self, resource):
        results = {}
        responseDict = self._redundantGetter(self._baseURL + resource)
        results.update({result['url']: result for result in responseDict['results']})
        while responseDict['info']['next'] is not None:
            responseDict = self._redundantGetter(responseDict['info']['next'])
            results.update({result['url']: result for result in responseDict['results']})
        if resource == 'character':
            self._chars = results
        return results

    def _getCounts(self, letter, results):
        return sum(len(re.findall(rf'({letter.lower()}|{letter.upper()})', result['name'])) for result in results.values())

    def _letterCounterInResource(self, letter, resource):
        results = self._getPaginatedResults(resource)
        count = self._getCounts(letter, results)
        return count

    def countCharsQueried(self, queries):
        start = time.time()
        results = {}
        for letter, resource in queries:
            count = self._letterCounterInResource(letter, resource)
            # print(f'Letter {letter} in resource {resource} was found {count} times')
            results[(letter, resource)] = count
        end = time.time()
        # print(f'Time elapsed: {round(end - start, 2)} seconds')
        return end - start, results

    def getLocationsFromEpisodes(self):
        start = time.time()
        episodes = self._getPaginatedResults('episode')
        if self._chars is None:
            self._getPaginatedResults('character')
        locationsPerEpisode = defaultdict(set)
        for episodeURL in episodes:
            episode = episodes[episodeURL]
            episodeChars = episode['characters']
            for char in episodeChars:
                locationsPerEpisode[episode['name']].add(self._chars[char]['origin']['name'])
        end = time.time()
        return end - start, locationsPerEpisode

    def prettyPrintCharCount(self, results):
        for (letter, resource) in results:
            print(f'Letter {letter} in resource {resource} was found {results[(letter, resource)]} times.')

    def prettyPrintLocationsFromEpisodes(self, locationsPerEpisode):
        for episode in locationsPerEpisode:
            print(f'Episode {episode} had {len(locationsPerEpisode[episode])} locations: {locationsPerEpisode[episode]}')

if __name__ == '__main__':
    rickAndMortyConsumer = RickAndMortyConsumer()
    executionTimeCharCount, charCounts = rickAndMortyConsumer.countCharsQueried([['l', 'location'],
                                            ['e', 'episode'],
                                            ['c', 'character']])
    print('\nPart 1\n')
    rickAndMortyConsumer.prettyPrintCharCount(charCounts)
    print(f'Execution time was {executionTimeCharCount} second')
    print('\nPart 2\n')
    executionTimeLocationsPerEpisode, locationsPerEpisode = rickAndMortyConsumer.getLocationsFromEpisodes()
    rickAndMortyConsumer.prettyPrintLocationsFromEpisodes(locationsPerEpisode)
    print(f'Execution time was {executionTimeLocationsPerEpisode} seconds')