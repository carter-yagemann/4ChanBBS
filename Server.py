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
import asyncio
import logging

import telnetlib3

import chanjson
from config import config
from htmlcleaner import strip_tags

# Logging Configuration
# ----------------------------------------------
FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT)

# ========================== async ========================

class Client():

    def __init__(self) -> None:
        self._reader: telnetlib3.TelnetReaderUnicode = None
        self._writer: telnetlib3.TelnetWriterUnicode = None
        self._params: list = None
        self._server: chanjson.ChanServer = chanjson.ChanServer()
        self._show_images: bool = config.showImages
        self._img_size: tuple = None
        self._logger.info("Server is ready for connections")

    @property
    def img_size(self) -> tuple:
        """returns size to make images as a tuple.
        Values are ints corrisponding to character values.

        Returns:
            tuple: (width: int, height: int)
        """
        img: tuple = ()
        if config.naws:
            # scale values to be roughly square.
            img = (min(self._img_size)*2, (min(self._img_size)))
        else:
            img = (config.img_width, config.img_hight)
        return img

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

    async def writeline(self, line: str = '') -> None:
        """writes line to client.  Replaces '\n' with CRLF.

        also adds newline to end of each line

        Args:
            line (str): string to send to client
        """

        # add a newline to the end if there isnt one already
        if line[:-1] != '\n':
            line += '\n'

        line = line.replace('\n', '\r\n')
        self._writer.write(line)
        await self._writer.drain()
          
    async def entry_point(self, reader, writer) -> None:
        """Entry point for client. Passes in objects and starts
        client session.

        Args:
            reader (stream_reader): stream reader object for client
            writer (stream_writer): stream writer object for client
        """
        self._reader = reader
        self._writer = writer
        self._writer.writeline = self.writeline

        await self.handler()

    async def command_listboards(self) -> None:
        """Sends a list of avalible boards to client

        Args:
            params (list): list of cmdline params from client
        """

        data = self._server.getBoards()

        await self._writer.writeline('*------*-------------------------*')
        await self._writer.writeline('| ID   | Name                    |')
        await self._writer.writeline('*------*-------------------------*')

        for board in data['boards']:
            try:
                line = '| ' + str(board['board'])
                for _ in range(len(line), 7):
                    line = line + ' '
                line = line + '| ' + str(board['title'])
                for _ in range(len(line), 33):
                    line = line + ' '
                line = line + '|'

                await self._writer.writeline(line)
                await self._writer.writeline('*------*-------------------------*')
            except KeyError:
                self._logger.error('Error: Failed to print board name')

        return

    async def command_listthreads(self) -> None:
        """List current threads in a given board.

        <boardID>
        Lists the threads in a given board.
        Lists the threads in a given board.
        Use listboards command to get the board's ID.
        Example: 'lt a' will list all the treads on /a/.

        """

        if len(self._params) == 0:
            await self._writer.writeline('Missing arguments')
            return

        try:
            boards = self._server.getBoards()['boards']

            for board in boards:
                if self._params[0] == board['board']:
                    board_info = board
                    break

            pages = board_info['pages']

        except KeyError:
            self._logger.error(
                'Error: Failed to get board info: %s', str(self._params[0]))
            await self._writer.writeline(
                'Communication error or invalid board ID...')
            return

        for page in range(1, pages - 1):
            threads = self._server.getThreads(self._params[0], page)['threads']

            for thread in threads:
                op = thread['posts'][0]

                await self._writer.writeline()
                await self._writer.writeline(
                    '\x1b[34m*-------------------------------*\x1b[0m')

                header = str(op['no']) + ' - \x1b[31;1m' + \
                    str(op['name']) + '\x1b[0m'

                if 'sub' in op.keys():
                    header = header + ' - ' + str(op['sub'])

                await self._writer.writeline(header)

                if 'tim' in op.keys() and self._show_images:
                    await self._writer.writeline()
                    img = self._server.getThumbNail(self._params[0], op['tim'], self.img_size)
                    await self._writer.writeline(img)
                    await self._writer.writeline()

                if 'com' in op.keys():
                    try:
                        await self._writer.writeline(strip_tags(op['com']))
                    except:
                        pass

                await self._writer.writeline('replies: ' + str(op['replies']))
                await self._writer.writeline(
                    '\x1b[34m*-------------------------------*\x1b[0m\n')

                self._writer.write(
                    'Enter - Next Thread | o - Open Thread | q - Quit: ')
                response = (await self._reader.readline()).strip()

                if response.lower() == 'q':
                    return
                elif response.lower() == 'o':
                    await self.command_getreplies([self._params[0], op['no']])
                    return

    async def command_getreplies(self, thread_id: list= None) -> None:
        """Cycles through the list of replies for a thread

            <boardID> <threadID>
            Lists the replies for a thread.
            Lists the replies for a thread.
            Use listboards and listthreads to get the IDs.
            Example: 'gr a 1' will list the replies for the thread on /a/ with ID 1.

        Args:
            thread_id (list): [<boardID>, <threadID>]
        """
        
        if not thread_id:
            thread_id = [self._params[0], self._params[1]]

        try:
            posts = self._server.getReplies(
                thread_id[0], thread_id[1])['posts']
        except:
            await self._writer.writeline(
                'Communication error or invalid board ID...')
            return

        for post in posts:
            await self._writer.writeline()
            await self._writer.writeline(
                '\n\x1b[34m*-------------------------------*\x1b[0m')

            header = str(post['no']) + ' - \x1b[31;1m' + \
                str(post['name']) + '\x1b[0m'

            await self._writer.writeline(header)

            if 'tim' in post.keys() and self._show_images:
                await self._writer.writeline()
                img = self._server.getThumbNail(thread_id[0], post['tim'], self.img_size)
                await self._writer.writeline(img)
                await self._writer.writeline()

            if 'com' in post.keys():
                try:
                    stripped = strip_tags(post['com'])
                    await self._writer.writeline(stripped)
                except:
                    pass
            await self._writer.writeline(
                '\x1b[34m*-------------------------------*\x1b[0m\n')

            self._writer.write('Enter - Next Reply | q - Quit: ')
            response = (await self._reader.readline()).strip()

            if response.lower() == 'q':
                return

    async def command_enableimages(self) -> None:
        """Enables images
        """
        await self._writer.writeline('Images have been enabled')
        self._show_images = True

    async def command_disableimages(self) -> None:
        """Disable images
        """
        await self._writer.writeline('Images have been disabled')
        self._show_images = False

    async def command_exit(self) -> bool:
        """Closes connection from server side

        Returns:
            bool: true when closed
        """
        self._server.close_session()
        await self._writer.writeline('good bye')
        await self._writer.drain()
        self._writer.close()
        return True
    
    async def command_help(self) -> None:
        """default help command
        """
        
        short_help = '''
        Usage: COMMAND {board} {thread}
        
            where COMMAND := {lb, lt, gr, di, ei, h, exit}
        '''
        
        long_help = '''Commands -> (<name>, <alias>): usage
        listboards, lb:
            list avalible boards.
                ex: lb
                
        listthreads, lt: 
            list the threads in a board. lt <board name>
                ex: lt b
                
        getreplies, gr: 
            list replies to a thread.  gr <board name> <threadID>
                ex: gr a 1
                
        disableimages, di:
            disables downloading of images. di
            
        enableimages, ei
            enables downloading of images. ei
            
        help, h:
            shows this message
            
        exit:
            asks server to close client connection'''
        
        help_msg = long_help if 'help' in self._cmd else short_help
        
        await self._writer.writeline(help_msg)
    
    
    async def command_bad_cmd(self) -> None:
        """default commmand not found method
        
        """
        await self._writer.writeline(f'cmd not found.  Try h or help for valid commands')
        self._logger.debug("bad command attempted")
        
    
    def handle_naws(self, width: int, height:int) -> None:
        """catches NAWS updates.  Negotiate About
        Window Size (naws) allows the client to advertize its 
        terminal window size to the server.

        Args:
            width (int): width in characters
            height (int): height in characters
        """
        self._img_size = (width, height)
        self._logger.debug(f"recived client term size change with naws: {self._img_size}")

    async def handler(self) -> None:
        """Handler method. Handles interactions with client.
        """

        commands = {
            'listboards': self.command_listboards,
            'listthreads': self.command_listthreads,
            'getreplies': self.command_getreplies,
            'enableimages': self.command_enableimages,
            'disableimages': self.command_disableimages,
            'exit': self.command_exit,
            'help': self.command_help
        }

        command_aliases = {
            'lb': commands['listboards'],
            'lt': commands['listthreads'],
            'gr': commands['getreplies'],
            'ei': commands['enableimages'],
            'di': commands['disableimages'],
            'h': self.command_help
        }

        commands.update(command_aliases)
        
        # tell the client to support echo if they want it
        self._writer.iac(telnetlib3.WONT, telnetlib3.ECHO)
        # tell the client to not use go ahead, this allows backspace
        self._writer.iac(telnetlib3.WONT, telnetlib3.SGA)
        # tell client to send terminal dimention changes with naws
        self._writer.iac(telnetlib3.DO, telnetlib3.NAWS)
        self._writer.set_ext_callback(telnetlib3.NAWS, self.handle_naws)
        
        # these are the values from inital conenction, 
        # changes will be handled using self.handle_naws
        self._img_size = (self._writer.get_extra_info('rows'),
                               self._writer.get_extra_info('cols'))


        await self._writer.writeline(config.welcome_message)
        stop = False

        while not stop:
            self._writer.write(f"\r\n{config.prompt}")
            req: str = await self._reader.readline()

            req: list = req.strip().split()

            if len(req) > 0:
                self._cmd = req[0]
                self._params = req[1:] # throw away cmd and keep only params
                stop = await commands.get(req[0], self.command_bad_cmd)()

        return


if __name__ == '__main__':
    logger = logging.getLogger('')
    logger.setLevel(config.loggingLevel)
    logger.info('Starting server on port %d', config.port)

    loop = asyncio.get_event_loop()
    coro = telnetlib3.create_server(
        host=config.server, port=config.port, shell=Client().entry_point)
    server = loop.run_until_complete(coro)
    loop.run_until_complete(server.wait_closed())
