## Imports
##------------------------------------------------------
import json, requests
import ascii_image
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
            response = requests.get(url='https://a.4cdn.org/' + str(board) + '/' + str(page) + '.json')
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
            response = requests.get(url='https://a.4cdn.org/' + str(board) + '/thread/' + str(thread) + '.json')
            data = json.loads(response.text)
            return data
        except:
            print 'Failed to process getReplies()'
            return ''

    # Get thumbnail for a post
    def getThumbNail(self, board, imgID):
        if (config.offline_mode):
            return '**********\n**********'

        try:
            url = 'https://0.t.4cdn.org/' + str(board) + '/' + str(imgID) + 's.jpg'
            file = ascii_image.open_url(url)
            img = ascii_image.convert_image(file, 60, 40)
            return img
        except:
            print 'Failed to get image for ', board, ' ', imgID
            return
