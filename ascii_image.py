#
#    4Chan BBS
#    ASCII Image - ascii_image.py
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

from PIL import Image
import urllib, cStringIO

def convert_image(img, x, y): 
    color = ' .,:;irsXA253hMHGS#9B&@'
 
    img = img.resize((x, y))
    pixel = img.load()

    string = ""    
    for h in xrange(y):
        for w in xrange(x):
            rgb = pixel[w, h]
            string += color[int(sum(rgb) / 3.0 / 256.0 * 23)]
        string += "\n"

    return string

def open_url(URL):
    try:
        file = cStringIO.StringIO(urllib.urlopen(URL).read())
        img = Image.open(file)
        return img
    except:
        print('Error: Failed to open image at ', URL)
        return
