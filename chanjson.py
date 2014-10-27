## Imports
##------------------------------------------------------
import json, requests
from config import config
if (config.offline_mode):
    import test_data

class ChanServer:
    
    # Gets all the boards
    def getBoards(self):
        if (config.offline_mode):
            return json.loads(test_data.boards_list)
        response = requests.get(url='https://a.4cdn.org/boards.json')
        data = json.loads(response.text)
        return data

    # Get a page of threads from a board
    def getThreads(self, board, page):
        if (config.offline_mode):
            return json.loads(test_data.threads_list)
        try:
            response = requests.get(url='https://a.4cdn.org/' + board + '/' + str(page) + '.json')
            data = json.loads(response.text)
            return data
        except:
            print 'Failed to process getThreads()'
            return ''

    # Get posts for a particular thread
    def getReplies(self, board, thread):
        if (config.offline_mode):
            return json.loads(test_data.replies_list)
        try:
            response = requests.get(url='https://a.4cdn.org/' + board + '/thread/' + str(thread) + '.json')
            data = json.loads(response.text)
            return data
        except:
            print 'Failed to process getReplies()'
            return ''
