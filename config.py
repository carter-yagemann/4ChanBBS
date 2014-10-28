#
#    4Chan BBS
#    Configuration - config.py
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

import logging

class config:

    ## Stock Messages
    ##-----------------------------------
    welcome_message = '''\x1b[31;1m
 __          __  _                            _             
 \ \        / / | |                          | |            
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___       
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \      
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | _ _ 
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___(_|_|_) \x1b[0m
\x1b[32;1m
                                                            .-. .-.
  _  _    _____ _                 ____  ____   _____       (   |   )
 | || |  / ____| |               |  _ \|  _ \ / ____|    .-.:  |  ;,-.
 | || |_| |    | |__   __ _ _ __ | |_) | |_) | (___     (_ __`.|.'__ _)
 |__   _| |    | '_ \ / _` | '_ \|  _ <|  _ < \___ \    (    .'|`.    )
    | | | |____| | | | (_| | | | | |_) | |_) |____) |    `-'/  |  \`-'
    |_|  \_____|_| |_|\__,_|_| |_|____/|____/|_____/       (   !   )
                                                            `-' `-'\\
                                                                    \\
                                                                     )
\x1b[0m
New to the server? Here's a quick guide:
	lb                      - List all the available boards
	lt <boardID>            - List the threads for a board
        ei/di                   - Enable/Disable the showing of images

If you need additional help or examples, try help <command>.
'''
    prompt = "4ChanBBS> "
    continue_prompt = "Press any key to continue..."


    ## Server Configuration
    ##-----------------------------------
    server = "0.0.0.0"
    port = 5000
    loggingLevel = logging.INFO

    ## OFFLINE DEVELOPMENT MODE
    ##-----------------------------------
    offline_mode = False
