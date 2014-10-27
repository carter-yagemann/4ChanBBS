## Imports
##------------------------------------------------------
import json, requests

class ChanServer:
    
    # Gets all the boards
    def getBoards(self):
        response = requests.get(url='https://a.4cdn.org/boards.json')
        data = json.loads(response.text)
        return data

    # Get a page of threads from a board
    def getThreads(self, board, page):
        try:
            response = requests.get(url='https://a.4cdn.org/' + board + '/' + str(page) + '.json')
            data = json.loads(response.text)
            return data
        except:
            print 'Failed to process getThreads()'
            return ''

    # Get posts for a particular thread
    def getReplies(self, board, thread):
        try:
            response = requests.get(url='https://a.4cdn.org/' + board + '/thread/' + str(thread) + '.json')
            data = json.loads(response.text)
            return data
        except:
            print 'Failed to process getReplies()'
            return ''
