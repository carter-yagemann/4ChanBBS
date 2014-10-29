4Chan BBS
=========

About
-----

4Chan BBS is a Python project which allows users to browse the popular image board 
4Chan through a telnet connection and command line interface.

Why?
----

Do you remember the good old days of networked computing before GUI browsers existed?

I don't, I'm too young.

Regardless, I think it's time for old-school telnet BBS server to make a comeback. So 
with that in mind, I made a BBS server for the popular image board 4Chan! The server 
back-end communicates through 4Chan's API to provide real boards, threads, and posts 
in real time and presents this data to the user through a command line interface. No 
more pesky GUIs!

4Chan BBS even supports images by converting them into a more CLI friendly ASCII string format!

Installation
------------

The easiest way to setup 4Chan BBS is to install Python 2.7 and PIP. Run 
`pip install -r requirements.txt` to get all the required libraries and then 
start the server using `python Server.py`.

If you get an error while trying to install Pillow, you may have to download some additonal
libraries using a command like `sudo apt-get build-dep python-imaging`.

Configuration
-------------

`config.py` includes all the configuration settings for the server.

License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <http://www.gnu.org/licenses/> for the full license.