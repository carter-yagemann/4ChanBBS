#
#    4Chan BBS
#    Server - Server.py
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
##----------------------------------------------
import SocketServer
import logging
from telnetsrv.threaded import TelnetHandler, command
from config import config
import chanjson
from htmlcleaner import strip_tags

## Logging Configuration
##----------------------------------------------
FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT)

## Telnet Server
##----------------------------------------------
class MyTelnetHandler(TelnetHandler):

    showImages = True

    WELCOME = config.welcome_message
    PROMPT = config.prompt
    CONTINUE_PROMPT = config.continue_prompt

    def session_start(self):
        logger = logging.getLogger('')
        logger.info('Connections: A user has connected.')
        if (config.offline_mode):
            self.writeresponse('\n\x1b[31;1m** OFFLINE MODE IS CURRENTLY ENABLED! **\x1b[0m\n')

    def session_end(self):
        logger = logging.getLogger('')
        logger.info('Connections: A user has disconnected.')

    @command(['listboards', 'lb'])
    def command_listboards(self, params):
        '''
        Lists available boards.
        
        '''
        server = chanjson.ChanServer()
        data = server.getBoards()
        self.writeresponse('*------*-------------------------*')
        self.writeresponse('| ID   | Name                    |')
        self.writeresponse('*------*-------------------------*')
        for board in data['boards']:
            try:
                line = '| ' + str(board['board'])
                for x in range(len(line), 7):
                    line = line + ' '
                line = line + '| ' + str(board['title'])
                for x in range(len(line), 33):
                    line = line + ' '
                line = line + '|'
                self.writeresponse(line)
                self.writeresponse('*------*-------------------------*')
            except:
                logger = logging.getLogger('')
                logger.error('Error: Failed to print board name')

    @command(['listthreads', 'lt'])
    def command_listthreads(self, params):
        '''<boardID>
        Lists the threads in a given board.
        Lists the threads in a given board.
        Use listboards command to get the board's ID.
        Example: 'lt a' will list all the treads on /a/.
        '''
        if (len(params) == 0):
            self.writeerror('Missing argument.')
            return

        server = chanjson.ChanServer()
        try:
            boards = server.getBoards()['boards']
            for board in boards:
                if (params[0] == board['board']):
                    board_info = board
            pages = board_info['pages']
        except:
            logger = logging.getLogger('')
            logger.error('Error: Failed to get board info: %s', str(params[0]))
            self.writeerror('Communication error or invalid board ID...')
            return

        for page in range(1, pages - 1):
            threads = server.getThreads(params[0], page)['threads']
            for thread in threads:
                op = thread['posts'][0]
                self.writeresponse(' ')
                self.writeresponse('\x1b[34m*-------------------------------*\x1b[0m')
                header = str(op['no']) + ' - \x1b[31;1m' + str(op['name']) + '\x1b[0m'
                if 'sub' in op.keys():
                    header = header + ' - ' + str(op['sub'])
                try:
                    self.writeresponse(header)
                except:
                    pass

                if 'tim' in op.keys() and self.showImages:
                    self.writeresponse(' ')
                    img = server.getThumbNail(params[0], op['tim'])
                    self.writeresponse(img)
                    self.writeresponse(' ')

                if 'com' in op.keys():
                    try:
                        self.writeresponse(strip_tags(op['com']))
                    except:
                        pass

                self.writeresponse('replies: ' + str(op['replies']))
                self.writeresponse('\x1b[34m*-------------------------------*\x1b[0m\n')

                response = self.readline(prompt='Enter - Next Thread | o - Open Thread | q - Quit: ')
                if (response.lower() == 'q'):
                    return
                elif (response.lower() == 'o'):
                    self.command_getreplies([params[0], op['no']])
                    return


    @command(['getreplies', 'gr'])
    def command_getreplies(self, params):
        '''<boardID> <threadID>
        Lists the replies for a thread.
        Lists the replies for a thread.
        Use listboards and listthreads to get the IDs.
        Example: 'gr a 1' will list the replies for the thread on /a/ with ID 1.
        '''
        if (len(params) < 2):
            self.writeerror('Missing arguments.')
            return

        server = chanjson.ChanServer()
        try:
            posts = server.getReplies(params[0], params[1])['posts']
        except:
            self.writeerror('Communication error or invalid board ID...')
            return

        for post in posts:
            self.writeresponse(' ')
            self.writeresponse('\x1b[34m*-------------------------------*\x1b[0m')
            header = str(post['no']) + ' - \x1b[31;1m' + str(post['name']) + '\x1b[0m'
            try:
                self.writeresponse(header)
            except:
                pass

            if 'tim' in post.keys() and self.showImages:
                self.writeresponse(' ')
                img = server.getThumbNail(params[0], post['tim'])
                self.writeresponse(img)
                self.writeresponse(' ')

            if 'com' in post.keys():
                    try:
                        self.writeresponse(strip_tags(post['com']))
                    except:
                        pass
            self.writeresponse('\x1b[34m*-------------------------------*\x1b[0m\n')

            response = self.readline(prompt='Enter - Next Reply | q - Quit: ')
            if (response.lower() == 'q'):
                return

    @command(['enableimages', 'ei'])
    def command_enableimages(self, params):
        '''
        Enables showing images in posts.

        '''
        self.writeresponse("Images have been enabled.")
        self.showImages = True

    @command(['disableimages', 'di'])
    def command_disableimages(self, params):
        '''
        Disables showing images in posts.

        '''
        self.writeresponse("Images have been disabled.")
        self.showImages = False


## TCP Server
##----------------------------------------------
class TelnetServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


## Main
##----------------------------------------------
logger = logging.getLogger('')
logger.setLevel(config.loggingLevel)
logger.info("Starting server on port %d", config.port)
tcpserver = TelnetServer((config.server, config.port), MyTelnetHandler)
logger.info("Server running.")
try:
    tcpserver.serve_forever()
except KeyboardInterrupt:
    logger.info("Server shutting down.")
