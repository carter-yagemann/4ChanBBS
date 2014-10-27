## Imports
##----------------------------------------------
import SocketServer
from telnetsrv.threaded import TelnetHandler, command
from config import config
import chanjson
from htmlcleaner import strip_tags

## Telnet Server
##----------------------------------------------
class MyTelnetHandler(TelnetHandler):


    WELCOME = config.welcome_message
    PROMPT = config.prompt
    CONTINUE_PROMPT = config.continue_prompt


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
                line = '| ' + board['board']
                for x in range(len(line), 7):
                    line = line + ' '
                line = line + '| ' + board['title']
                for x in range(len(line), 33):
                    line = line + ' '
                line = line + '|'
                self.writeresponse(line)
                self.writeresponse('*------*-------------------------*')
            except:
                print 'Error: Failed to print board name'

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
            print 'Error: Failed to get board info: ', params[0]
            self.writeerror('Communication error or invalid board ID...')
            return

        for page in range(1, pages):
            threads = server.getThreads(params[0], page)['threads']
            for thread in threads:
                op = thread['posts'][0]
                header = str(op['no']) + ' - ' + op['name']
                if 'sub' in op.keys():
                    header = header + ' - ' + op['sub']
                try:
                    self.writeresponse(header)
                except:
                    pass

                if 'com' in op.keys():
                    try:
                        self.writeresponse(strip_tags(op['com']))
                    except:
                        pass

                self.writeresponse('replies: ' + str(op['replies']))
                self.writeresponse('---\n')

            if (page == (pages - 1)):
                return
            response = self.readline(prompt='Load next page? [y/n] ')
            if (response.lower() == 'n'):
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

        post_count = 0
        for post in posts:
            header = str(post['no']) + ' - ' + post['name']
            try:
                self.writeresponse(header)
            except:
                pass

            if 'com' in post.keys():
                    try:
                        self.writeresponse(strip_tags(post['com']))
                    except:
                        pass
            self.writeresponse('---\n')

            post_count = post_count + 1
            if (post_count > 10):
                post_count = 0
                response = self.readline(prompt='Load more replies? [y/n] ')
                if (response.lower() == 'n'):
                    return


## TCP Server
##----------------------------------------------
class TelnetServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


## Main
##----------------------------------------------
tcpserver = TelnetServer((config.server, config.port), MyTelnetHandler)
tcpserver.serve_forever()
