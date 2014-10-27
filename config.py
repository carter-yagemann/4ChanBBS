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

    ## OFFLINE DEVELOPMENT MODE
    ##-----------------------------------
    offline_mode = False
