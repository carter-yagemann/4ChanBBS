#
#    4Chan BBS
#    Chan JSON - chanjson.py
#
#    Copyright Carter Yagemann 2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    See <http://www.gnu.org/licenses/> for a full copy of the license.
#

## Imports
##------------------------------------------------------
import json, requests
import ascii_image
import logging
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
            logger = logging.getLogger('')
            logger.error('Error: Failed to process getThreads()')
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
            logger = logging.getLogger('')
            logger.error('Error: Failed to process getReplies()')
            return ''

    # Get thumbnail for a post
    def getThumbNail(self, board, imgID):
        if (config.offline_mode):
            return '**********\n**********'

        try:
            url = 'https://i.4cdn.org/' + str(board) + '/' + str(imgID) + 's.jpg'
            file = ascii_image.open_url(url)
            img = ascii_image.convert_image(file, 60, 40)
            return img
        except:
            logger = logging.getLogger('')
            request = str(board) + ' => ' + str(imgID)
            logger.error('Error: Failed to get image for %s', request)
            return
