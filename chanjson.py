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
import json
import logging

import requests

import ascii_image
from config import config

if config.offline_mode:
    import test_data


class ChanServer:

    def __init__(self) -> None:
        self._boards = None
        self._session = requests.Session()

        self._boards = self.getBoards()

    def close_session(self) -> None:
        self._session.close()

    # Gets all the boards
    def getBoards(self):

        if self._boards:
            return self._boards

        if config.offline_mode:
            return json.loads(test_data.boards_list)
        
        response = self._session.get(url='https://a.4cdn.org/boards.json')
        data = json.loads(response.text)
        return data

    # Get a page of threads from a board
    def getThreads(self, board, page):
        if config.offline_mode:
            return json.loads(test_data.threads_list)
        try:
            response = self._session.get(
                url='https://a.4cdn.org/' + str(board) + '/' + str(page) + '.json')
            data = json.loads(response.text)
            return data
        except:
            self._logger.error('Error: Failed to process getThreads()')
            return ''

    # Get posts for a particular thread
    def getReplies(self, board, thread):
        if config.offline_mode:
            return json.loads(test_data.replies_list)
        try:
            response = self._session.get(
                url='https://a.4cdn.org/' + str(board) + '/thread/' + str(thread) + '.json')
            data = json.loads(response.text)
            return data
        except:
            self._logger.error('Error: Failed to process getReplies()')
            return ''

    # Get thumbnail for a post
    def getThumbNail(self, board, imgID):
        if config.offline_mode:
            return '**********\n**********'

        try:
            url = 'https://i.4cdn.org/' + \
                str(board) + '/' + str(imgID) + 's.jpg'

            content = (self._session.get(url)).content
            file = ascii_image.open_img(content)
            img = ascii_image.convert_image(img=file, x=config.img_width, y=config.img_hight)

            return img
        except:
            request = str(board) + ' => ' + str(imgID)
            self._logger.error('Error: Failed to get image for %s', request)
            return

    @property
    def _logger(self):
        """Adds the class name to log messages by instantating
        logger to the class it is used in

        Returns:
            logger: this classes logger
        """
        return logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def __str__(self) -> str:
        return str(self.__class__.__name__)
